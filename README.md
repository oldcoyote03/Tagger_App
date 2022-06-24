# Tagger_App

Set host IP address to make API reachable from host: [Flask Docker Error: Empty reply from server](https://www.youtube.com/watch?v=4uoWRXuYfJs)

Test API with cURL
```
curl -H "Content-Type: application/json" -X GET http://localhost:5000/hello
```

[Circular import issue & flask_sqlalchemy create_all()](https://stackoverflow.com/questions/22929839/circular-import-of-db-reference-using-flask-sqlalchemy-and-blueprints)

Options for created_at field:
1. In SQLAlchemy Column, use default=sqlalchemy.sql.func.current_date for injecting the date of the INSERT statement
2. In the CREATE TABLE operation, use CURRENT_TIME() function. 
Note: Since the CREATE TABLE operation occurs before the app is run, you cannot use the server_default=sqlalchemy.sql.func.current_date since this injects the CURRENT_DATE() function into the CREATE TABLE operation (which is done already).