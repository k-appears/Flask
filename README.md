# Acceptance Criteria

### Request
Service with a REST Endpoint to search for movies using genre as input. The endpoint should have the following signature:

    GET /movies?genre=Animation&offset=0&limit=10

`genre`: Matches the genre of the movie. Only single genre is allowed.

`offset`: Provides the starting index for the search results. Default is 0, if not specified.

`limit`: Provides the number of results returned per page. Default is 10 if not specified.

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