import os
import tempfile
import unittest

from flask_testing import TestCase

import main
from main import app


class MoviesTest(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['LIVESERVER_PORT'] = 5001
        return app

    def test_wrong_path(self):
        response = self.client.get("/shubies?genre=Comedy")
        self.assert400(response)
        self.assertIsNotNone(response.json['errors'])
        self.assertEqual(len(response.json['errors']), 1)
        self.assertEqual(response.json['errors'][0]['errorCode'], 400)
        self.assertRegex(response.json['errors'][0]['message'], 'movies')

    def test_not_found_genre(self):
        response = self.client.get("/movies?genre=RandOm+Genre")
        self.assert400(response)
        self.assertIsNotNone(response.json['errors'])
        self.assertEqual(len(response.json['errors']), 1)
        self.assertEqual(response.json['errors'][0]['errorCode'], 400)
        self.assertEqual(response.json['errors'][0]['message'], 'Genre provided is not valid')

    def test_negative_offset(self):
        response = self.client.get("/movies?genre=Science+Fiction&offset=-1")
        self.assert200(response)
        self.assertIsNotNone(response.json['metadata'])
        self.assertEqual(response.json['metadata']['offset'], 0)

    def test_no_offset(self):
        response = self.client.get("/movies?genre=Science+Fiction")
        self.assert200(response)
        self.assertIsNotNone(response.json['metadata'])
        self.assertEqual(response.json['metadata']['offset'], 0)

    def test_negative_limit(self):
        response = self.client.get("/movies?genre=Science+Fiction&limit=-1")
        self.assert200(response)
        self.assertIsNotNone(response.json['metadata'], msg=f"Error in response {response}")
        self.assertGreaterEqual(response.json['metadata']['limit'], 0)

    def test_no_limit(self):
        response = self.client.get("/movies?genre=Science+Fiction")
        self.assert200(response)
        self.assertIsNotNone(response.json['metadata'], msg=f"Error in response {response}")
        self.assertEqual(response.json['metadata']['limit'], 10)

    def test_limit_bigger_than_size(self):
        response = self.client.get("/movies?genre=Science+Fiction&limit=90")
        self.assert200(response)
        self.assertIsNotNone(response.json['metadata'])
        self.assertEqual(response.json['metadata']['offset'], 0)
        self.assertEqual(response.json['metadata']['limit'], 80)

    def test_offset_bigger_than_limit(self):
        response = self.client.get("/movies?genre=Science+Fiction&limit=80&offset=100")
        self.assert200(response)
        self.assertIsNotNone(response.json['metadata'])
        self.assertEqual(response.json['metadata']['offset'], 79)
        self.assertEqual(response.json['metadata']['limit'], 1)


class MoviesTestErrorExternalServer(TestCase):
    tmp_server = main.MOVIES_SERVER_URL
    tmp_threshold = main.THRESHOLD_REQUEST

    def create_app(self):
        main.MOVIES_SERVER_URL = "http://localhost:8000/"
        main.THRESHOLD_REQUEST = 0
        app.config['TESTING'] = True
        app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = False
        app.config['LIVESERVER_PORT'] = 5001
        return app

    def test_server_error(self):
        response = self.client.get("/movies?genre=Science+Fiction")
        self.assert500(response)

    main.MOVIES_SERVER_URL = tmp_server
    main.THRESHOLD_REQUEST = tmp_threshold


class MoviesTestNotFoundGenreJson(TestCase):
    tmp = main.JSON_GENRE

    def create_app(self):
        main.JSON_GENRE = "notfound.json"
        app.config['TESTING'] = True
        app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = False
        app.config['LIVESERVER_PORT'] = 5001
        return app

    def test_genre_json_not_found(self):
        with self.assertLogs(app.logger, level='ERROR') as cm:
            response = self.client.get("/movies?genre=Science+Fiction")
            self.assert500(response)
            self.assertEqual(response.data.decode("utf-8"), "Internal error")
            self.assertRegex(cm.output[0], "FileNotFoundError")

    main.JSON_GENRE = tmp


class MoviesTestIncorrectGenreJson(TestCase):
    tmp = main.JSON_GENRE

    def create_app(self):
        app.config['TESTING'] = True
        app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = False
        app.config['LIVESERVER_PORT'] = 5001
        return app

    def test_genre_json_not_found(self):
        fd, path = tempfile.mkstemp("incorrect.json", dir=app.root_path, text=True)
        with os.fdopen(fd, 'w') as tmp:
            tmp.write('not a json')

        main.JSON_GENRE = path

        with self.assertLogs(app.logger, level='ERROR') as cm:
            response = self.client.get("/movies?genre=Science+Fiction")
            self.assert500(response)
            self.assertEqual(response.data.decode("utf-8"), "Internal error")
            self.assertRegex(cm.output[0], "JSONDecodeError")

        os.remove(path)

    main.JSON_GENRE = tmp


if __name__ == '__main__':
    unittest.main()
