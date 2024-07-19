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
* Configuration
* Flask SQLAlchemy Marshmallow CockroachDB
* SQLAlchemy cockroachdb run_transaction 
* Unit tests
* Local tests
* Build pipeline
* User and Tags models
* Boilerplate

## DONE: 
* Development workflow
* Version upgrades
* Platform agnostic UUID field
* Logging

## VS Code Extensions:
* Python
** Python Debugger
** Pylance
** Pylint
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
 