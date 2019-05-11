# Acceptance Criteria

### Request
Service with a REST Endpoint to search for movies using genre as query parameter, as:

    GET /movies?genre=Animation&offset=0&limit=10

`genre`: Genres are provided as a static resource in the genres.json file.

`offset`: Provides the starting index for the search results. Default is 0, if not specified.

`limit`: Provides the number of result returned per page. Default is 10 if not specified.

It it will query a service that runs in `localhost:3040`

### Response:

    {
        "data": {
            "movies": [
                { "id": "1111" }, ...
            ]
        },
        "metadata": {
            "offset": 0,
            "limit": 10,
            "total": 20
        }
    }
    
### How to run it
Python version used 3.7.2

1. Run `docker-compose up`
2. Recommended create a virtual environment, eg: `python3 -m venv ~/venv`
3. Activate virtual env, eg: `source ~/venv/bin/activate`
4. Install requirements `pip install -r requirements.txt`
5. Run app `python main.py`, app opened in http://localhost:5000
6. Run tests `python test_movies.py`


#### load testing
1. Activated virtual env
2. App running
3. `locust --host=http://localhost:5000 -f test_performance.py`
4. Open browser http://localhost:8089