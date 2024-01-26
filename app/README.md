# Dynamic Cruisers Backend
## Flask server

This is the backend of the Dynamic Cruisers web application
It is a flask backend

### Setup

```sh
pipenv install && pipenv shell

cd app
# make sure you are in the app directory
# run the flask server
python3 app.py
# good to go, now fetch from client
```

There is some seeded data in the app.db

### Routes

Get dealership route:
`/dealerships`
Server output

```json
[
    {
        "id": 1,
        "name": "Nairobi cars",
        "address": "12345 Main St",
        "website": "www",
        "rating": "3"
    },
    {
        // second dealership
        // ...
    }
]
```

Get dealership by id route:
`/dealerships/1`
Server output

```json
{
    "id": 1,
    "name": "Nairobi cars",
    "address": "12345 Main St",
    "website": "www",
    "rating": "3"

}
```

Get dealership route:
`/dealerships`
Server output

```json
{
    "id": 1,
    "name": "Nairobi cars",
    "address": "12345 Main St",
    "website": "www",
    "rating": "3"

}
```