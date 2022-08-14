# simple-csv-api

[![run-tests](https://github.com/scrussell24/simple-csv-api/actions/workflows/main.yml/badge.svg)](https://github.com/scrussell24/simple-csv-api/actions/workflows/main.yml)

A simple web service for uploading csv data.

## Usage

This API provides a single endpoint to post CSV data. Custom headers are required to provide metadata needed to parse the csv body.

HTTP method: POST

path: /api/csv_files/

Content-Type: text/csv

Required Headers:
* X-Filename
* X-Delimiter
* X-Quotechar

### Example HTTP request

```
POST /api/csv_files/ HTTP/1.1
Host: 0.0.0.0:8000
X-Filename: example.csv
X-Delimiter: ,
X-Quotechar: 
Content-Type: text/csv
Content-Length: 294

Start Date,End Date,Tactic,Event Type,Pay Type,Attendance,Investment
2/1/2017,2/28/17,Events,Internal,Service,15,3567
2/1/2017,6/30/2017,Events,Internal,Sponsorship,65,3874
2/14/2017,10/31/2018,Events,Internal,Service,10,6474,
2/15/2017,5/17/2017,Events,External,Passive sponsorship,75,6622
```

### Example Repsonse

Status Code: 201
```
{
    "id": 49,
    "name": "example.csv",
    "path": "/home/scott/Projects/simple-csv-api/files/example-4d40280b-96eb-43ff-8d52-1ff066097c28.csv",
    "columns": [
        {
            "id": 331,
            "name": "Start Date",
            "column_datatype": "DATETIME"
        },
        {
            "id": 332,
            "name": "End Date",
            "column_datatype": "DATETIME"
        },
        {
            "id": 333,
            "name": "Tactic",
            "column_datatype": "TEXT"
        },
        {
            "id": 334,
            "name": "Event Type",
            "column_datatype": "TEXT"
        },
        {
            "id": 335,
            "name": "Pay Type",
            "column_datatype": "TEXT"
        },
        {
            "id": 336,
            "name": "Attendance",
            "column_datatype": "NUMBER"
        },
        {
            "id": 337,
            "name": "Investment",
            "column_datatype": "NUMBER"
        }
    ]
}
```

## Client

A cli client is included to interact with the API locally. Below is an example of how to call it (or get more information via the --help argument)

```
python client/core.py files post example.csv "$(cat resources/example.csv)"

or

./scripts/client_example.sh
```

## Install

### Prerequisties

* Python3.10

Clone this repository

```
git clone git@github.com:scrussell24/simple-csv-api.git
```

Install the required modules
```
pip install -r requirements-dev.txt
```

Run the DB migrations
```
./scripts/migrate.sh
```

## Run the application

```
./scripts/run.sh
```

## Run the tests

```
./scripts/test.sh
```