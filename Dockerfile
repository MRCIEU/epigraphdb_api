FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

RUN apt update && apt install -y graphviz

COPY ./poetry.lock ./pyproject.toml ./
RUN pip install poetry
RUN poetry config virtualenvs.create false \
  && poetry install --no-dev

COPY ./ /app
