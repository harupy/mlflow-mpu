# MLflow MPU (WIP)

A prototype for https://github.com/mlflow/mlflow/issues/9133. For faster iteration, FastAPI is used. The goal is a POC of the design and find issues beforehand.

## Development

```sh
# start app
poetry run uvicorn server:app --reload

# formatting
poetry run black .
poetry run ruff --fix .
```
