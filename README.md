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

## Testing
- Navigate to the project directory
- Activate the virtual environment: `source venv/bin/activate`
- Run the tests: `PYTHONPATH=src pytest`

## Links for development

- Marvin-API: https://github.com/amazingmarvin/MarvinAPI/wiki
  - Mit der REST-API kann man nur sehr schwer die Time-Tracking-Informationen der (gefilterten, z.B. von heute etc.) Tasks besorgen
- CouchDB:
  - Da kann man sogar filtern und alles mögliche, siehe [find-Beispiel Python](https://couchdb-python.readthedocs.io/en/latest/client.html#couchdb.client.Database.find) und [Find-API bei CouchDB](https://docs.couchdb.org/en/stable/api/database/find.html) 
  - [Mit Marvin durch CouchDB anbinden - Beispiel mit Python](https://github.com/amazingmarvin/marvin-python/blob/master/marvin.py)
  - [Marvin Data Types](https://github.com/amazingmarvin/MarvinAPI/wiki/Marvin-Data-Types)
  - [Couchdb Docker](https://hub.docker.com/_/couchdb/)
