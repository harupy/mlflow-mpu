# MLflow MPU (WIP)

A prototype for https://github.com/mlflow/mlflow/issues/9133. For faster iteration, FastAPI is used.

## Goals

- POC of the design.
- Find issues/challenges.

## Development

```sh
# installation
poetry install

# start app
poetry run uvicorn server:app --reload

# formatting
poetry run black .
poetry run ruff --fix .
```
