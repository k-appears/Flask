import os
import time

import requests
from flask import Flask, json, request, jsonify
from requests import HTTPError

DEBUG = False
JSON_GENRE = "genres.json"
MOVIES_SERVER_URL = 'http://localhost:3040/'
THRESHOLD_REQUEST = 10

app = Flask(__name__)
app.config.from_object(__name__)


@app.errorhandler(Exception)
def all_exception_handler(error):
    app.logger.error('Internal error', exc_info=True)
    return "Internal error", 500


@app.route('/<path:path>', methods=['GET'])
def movies(path):
    errors = _url_errors(path)
    if errors:
        return jsonify({
            "errors": errors
        }), 400
    params = _add_limit_param_if_not()

    return _content_from_request(params, path)


def _content_from_request(params, path):
    # Alternative to non-well maintained circuitbreaker package
    tries = 0
    success = False
    while not success and tries <= THRESHOLD_REQUEST:
        try:
            rv = requests.get(MOVIES_SERVER_URL + path, params=params)
            rv.raise_for_status()
            success = True
        except (requests.exceptions.ConnectionError, HTTPError) as e:
            app.logger.error("Response error: '%s'", str(e))
            tries = tries + 1
            time.sleep(1)  # Throttling

    if not success or not rv:
        return f"Error accessing {rv.request} after '{THRESHOLD_REQUEST}' requests ", 500
    return jsonify(json.loads(rv.content))  # No need to check if json response is valid


def _url_errors(path):
    return list(filter(None, [_check_path(path), _check_genre_param()]))


def _check_path(path):
    if path != 'movies':
        return {
            "errorCode": 400,
            "message": f"path should be 'movies' found '{path}'"
        }


def _check_genre_param():
    with open(os.path.join(app.root_path, JSON_GENRE)) as file:
        genres_json = json.load(file)
        genre = {genre["name"] for genre in genres_json}
        if not request.args.get("genre") in genre:
            return {
                "errorCode": 400,
                "message": "Genre provided is not valid"
            }


def _add_limit_param_if_not():
    params = request.args.to_dict()
    if 'limit' not in params:
        params['limit'] = 10
    return params


if __name__ == "__main__":
    app.debug = DEBUG
    app.run()
