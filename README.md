# Trading Simulator (Work in Progress)

This is a small stock trading simulator built with Python using the Flask framework with ReactJS on the front-end.
The project is currently a work in progress.

## Requirements
Docker
IEX API Key

### Configuring API Keys and DB Environment

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

## Running Development Environment

Build the Docker images and setup database tables by running the Alembic migrations.

`make build`
`make migrate-up`

If the `FLASK_ENV` is set to `development`, then the webpack-dev-server has to be running (`npm run start` in the /frontend static folder).

`make up`