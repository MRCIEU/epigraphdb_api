FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

RUN apt-get --allow-releaseinfo-change update \
  && apt install -y graphviz
RUN python -m pip install --upgrade pip

COPY ./poetry.lock ./pyproject.toml ./
RUN pip install poetry
RUN poetry config virtualenvs.create false \
  && poetry install --no-dev

COPY ./ /app
