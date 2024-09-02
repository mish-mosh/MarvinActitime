# MarvinActitime

A CLI to manage synchronisation of time-tracking information from [Amazing Marvin](https://amazingmarvin.com/)
to [ActiTime](https://www.actitime.com/).

For this script `Python3.11` ist used.

> **Note:** this is in early development and will very likely change.

## Features
- *Time accounting for Amazing Marvin tasks:* Synchronise the time tracking information of tasks from Amazing Marvin to ActiTime
- *Time accounting for pinned tasks:* Export time durations of a predefined set of tasks to ActiTime
  Therefor you need to copy the file `pinned_tasks.template.yaml` to `pinned_tasks.yaml` and fill your pinned tasks.
- *Overtime tracking:* Track your daily overtime in CSV format and get your overtime balance

## Installation
- Make sure you have Python 3.11 installed.
- Make a virtual environment: `python3.11 -m venv venv`
- Activate the virtual environment: `source venv/bin/activate`
- Install the requirements: `pip install -r requirements.txt`
- Copy the file `.env.template` to `.env` and fill in your configs/credentials
- Copy the file `pinned_tasks.template.yaml` to `pinned_tasks.yaml` and fill in your pinned tasks

## Usage
- Navigate to the project directory
- Activate the virtual environment: `source venv/bin/activate`
- Navigate to the source directory: `cd src`
- Run the script: `PYTHONPATH=. python main.py`

### Mapping Marvin tasks to ActiTime tasks
I order to synchronise the tracked time from Amazing Marvin to ActiTime,
you need to place the following in the notes of the task in Amazing Marvin (replace the `URL` with the URL of the task in ActiTime):

Meta.yml
```
actitimeUri: URL
```

## Testing
- Navigate to the project directory
- Activate the virtual environment: `source venv/bin/activate`
- Run the tests: `PYTHONPATH=src pytest`

## Links for development

- Marvin-API: https://github.com/amazingmarvin/MarvinAPI/wiki
- CouchDB:
  - [Database find](https://couchdb-python.readthedocs.io/en/latest/client.html#couchdb.client.Database.find)
  - [Find-API](https://docs.couchdb.org/en/stable/api/database/find.html) 
  - [Amazing Marvin Python example](https://github.com/amazingmarvin/marvin-python/blob/master/marvin.py)
  - [Marvin Data Types](https://github.com/amazingmarvin/MarvinAPI/wiki/Marvin-Data-Types)
  - [Couchdb Docker](https://hub.docker.com/_/couchdb/)
