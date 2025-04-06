# Tagger_App

Set host IP address to make API reachable from host: [Flask Docker Error: Empty reply from server](https://www.youtube.com/watch?v=4uoWRXuYfJs)

Test API with cURL
```
curl -H "Content-Type: application/json" -X GET http://localhost:5000/test
```

Options for created_at field:
1. In SQLAlchemy Column, use default=sqlalchemy.sql.func.current_date for injecting the date of the INSERT statement
2. In the CREATE TABLE operation, use CURRENT_TIME() function. 
Note: Since the CREATE TABLE operation occurs before the app is run, you cannot use the server_default=sqlalchemy.sql.func.current_date since this injects the CURRENT_DATE() function into the CREATE TABLE operation (which is done already).

## TODO:
* Deploy to local docker environment
* User model
* User auth
* Flask SQLAlchemy Marshmallow CockroachDB
* Tags model
* Boilerplate
* Multi-branch build pipeline - Jenkins in the cloud
* Deploy to k8s environment hosted in the cloud

## DONE: 
* Development workflow
* Version upgrades
* Platform agnostic UUID field
* Logging
* Configuration
* Unit tests
* SQLAlchemy cockroachdb run_transaction
  * run_transaction logging decorator
  * All endpoints
* Local tests
* ModelView
* Dataclass / Mapped Column
* Multi-branch build pipeline

## VS Code Extensions:
* Python
  * Python Debugger
  * Pylance
  * Pylint
* Containerization
  * Docker
  * Dev Containers
* Cody AI


## NOTES ABOUT UUID TYPES:
Works with both cockroachdb and sqlite end-to-end
```
from sqlalchemy.types import Uuid
id = db.Column(Uuid(native_uuid=True), primary_key=True)
```

Works with cockroachdb end-to-end
Works sqlite when URI does not have ID
Does not work with sqlite when URI has ID
```
from sqlalchemy_utils.types.uuid import UUIDType
id = db.Column(UUIDType(), primary_key=True)
```

## NOTE ABOUT REQUIRED PACKAGES
```
Flask==3.0.3
Flask-SQLAlchemy==3.1.1
SQLAlchemy-Utils==0.41.2  # for UUID
psycopg2-binary==2.9.9
sqlalchemy-cockroachdb==2.0.2
flask-marshmallow==1.2.1
marshmallow_sqlalchemy==1.0.0
webargs==8.2.0
dynaconf==3.2.6  # for config
pytest-flask==1.3.0
pytest-mock==3.14.0
pytest-sqlalchemy-mock==0.1.7  # for mock db
pytest-cov==5.0.0  # for coverage
pylint==3.3.1  # for linting
```