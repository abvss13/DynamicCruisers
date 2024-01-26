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
#### Dealerships

Get all dealership route:
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
#### Vehicles
Get all vehicles route:
`/vehicles`
Server output:

```json
[
    {
        "availability": false,
        "id": 1,
        "image": "other.ppt",
        "likes": 65,
        "make": "Burke and Sons",
        "model": "pay",
        "numbers_available": 10,
        "year": 2019
    },
    {
        // second vehicle
        // ...
    }
]
```

Get vehicles by id route:
`/vehicles/1`
Server output:

```json
{
    "availability": false,
    "id": 1,
    "image": "other.ppt",
    "likes": 65,
    "make": "Burke and Sons",
    "model": "pay",
    "numbers_available": 10,
    "year": 2019
}
```

### TO DO
get vehicle's dealership when calling vehicles

#### Reviews
Get reviews for vehicle:
`/reviews/<int: vehicle_id>`
`/reviews/10`
Server output:

```json
[
    {
        "content": "Face what almost turn true. Far surface career. Specific hope down assume challenge shake page. Level loss investment heavy.",
        "date_posted": "2020-10-17T02:12:51.658804",
        "id": 1,
        "title": "Send of town certainly politics skin suggest.",
        "user_firstname": "Glenda",
        "user_id": 8,
        "user_lastname": "Calderon",
        "vehicle_id": 10,
        "vehicle_make": "Martin PLC",
        "vehicle_model": "drop",
        "vehicle_year": 1975
    },
    {
        "content": "Expert say course Republican door. Ground face you take she pay.",
        "date_posted": "2020-07-16T09:51:54.879584",
        "id": 6,
        "title": "Republican as candidate thought become.",
        "user_firstname": "Brittany",
        "user_id": 10,
        "user_lastname": "Hale",
        "vehicle_id": 10,
        "vehicle_make": "Martin PLC",
        "vehicle_model": "drop",
        "vehicle_year": 1975
    },
]
```
