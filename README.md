# Trading Simulator (Work in Progress)

This is a small stock trading simulator built with Python using the Flask framework and React.JS on the front-end.
The documentation here is also still in progress.

## Requirements
* Docker

## Configuring API Keys and DB Environment

Docker gets the database configuration from an environment file `database.env` located in the root folder of the project.
It is not under source control.

Create a file `database.env` at the root of the project.
```
POSTGRES_USER=user
POSTGRES_PASSWORD=pass
POSTGRES_DB=db
```

In the root of the project, an `instance` folder has to be created as well, which will be used
as a module to get configuration values.

`instance/__init__.py` (Empty File)  
`instance/config.py`  
```
SECRET_KEY = 'key'
DATABASE_HOST = 'dbhost'
DATABASE_NAME = 'dbname'
DATABASE_USER = 'dbuser'
DATABASE_PASS = 'dbpass'
IEX_SECRET_TOKEN = 'token'
IEX_SB_SECRET_TOKEN = 'token'
```