# Ayble Health Coding Challenge API 

Before getting started, it is recommended that you create a virtual environment for installing all of the 
pip dependencies. This will prevent polluting your global python installation with project-specific dependencies.
Note: this is not required if you plan to run the application exclusively using `docker`.
## Create a virtual env
```bash
python -m venv venv
```

If you use `direnv` then activate the new virtual environment by running this command.
```bash
direnv allow .
```

Otherwise, if you do not use `direnv`, active the virtual environment manually using the following command.
```bash
source venv/bin/activate
```

## Poetry
Use the following poetry commands to install the pip dependencies and run the API server:
```bash
poetry install
poetry run python -m ayble_health_api
```

This will start the server on the configured host.

You can find swagger documentation at `http://localhost:8000/api/docs`.

## Docker
You can start the project with docker using this command:
```bash
docker-compose -f docker-compose.yml  up --build
```

If you want to develop in docker with autoreload add `-f docker-compose.dev.yml` to your docker command.
Like this:

```bash
docker-compose -f docker-compose.yml -f docker-compose.dev.yml  up --build
```

## Running tests

If you want to run it in docker, simply run:

```bash

docker-compose -f docker-compose.yml -f docker-compose.dev.yml build 
docker-compose -f docker-compose.yml -f docker-compose.dev.yml run api pytest -vv .
docker-compose -f docker-compose.yml -f docker-compose.dev.yml down
```

For running tests on your local machine, simply run the following command:
```bash
pytest -vv .
```


## Manual tests using example data 
Before trying to make any requests to the server, ensure 
that the API server is listening on localhost:8000 using one of the methods listed above.

Add a user:
```bash
curl -X POST http://localhost:8000/api/user -d "$(cat ./example_data/payload_add_user.json)" -H "Content-Type: application/json"

```

Add a meal:
```bash
curl -X POST http://localhost:8000/api/meal -d "$(cat ./example_data/payload_add_meal.json)" -H "Content-Type: application/json"
```

Update a meal portion:
```bash
curl -X PUT http://localhost:8000/api/meal-portion/1 -d "$(cat ./example_data/payload_update_portion.json)" -H "Content-Type: application/json"
```

NOTE: the example data assumes that the local database starts with initial auto increment identifiers of 1 
and that these operations are performed in order.

## linting
this project uses Ruff + and Mypy for linting and static type checking respectively.
run the `./lint.sh` to run all checks and apply any fixes that can be applied automatically.
