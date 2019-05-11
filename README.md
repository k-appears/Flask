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