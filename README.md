# MarvinActitime

A CLI to manage synchronisation of time-tracking information from [Amazing Marvin](https://amazingmarvin.com/)
to [ActiTime](https://www.actitime.com/).

For this script `Python3.11` ist used.

## Features
- *Time accounting for pinned tasks:* Export time durations of a predefined set of tasks to ActiTime
  Therefor you need to copy the file `pinned_tasks.template.yaml` to `pinned_tasks.yaml` and fill your pinned tasks.



## Links for development

- Marvin-API: https://github.com/amazingmarvin/MarvinAPI/wiki
  - Mit der REST-API kann man nur sehr schwer die Time-Tracking-Informationen der (gefilterten, z.B. von heute etc.) Tasks besorgen
- CouchDB:
  - Da kann man sogar filtern und alles mögliche, siehe [find-Beispiel Python](https://couchdb-python.readthedocs.io/en/latest/client.html#couchdb.client.Database.find) und [Find-API bei CouchDB](https://docs.couchdb.org/en/stable/api/database/find.html) 
  - [Mit Marvin durch CouchDB anbinden - Beispiel mit Python](https://github.com/amazingmarvin/marvin-python/blob/master/marvin.py)
  - [Marvin Data Types](https://github.com/amazingmarvin/MarvinAPI/wiki/Marvin-Data-Types)
  - [Couchdb Docker](https://hub.docker.com/_/couchdb/)
