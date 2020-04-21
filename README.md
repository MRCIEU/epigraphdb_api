# EpiGraphDB API Server

## Setup

1. Get example **environment variable** configs from **project space** (check internal docs) and place under `./`.
1. Review the example `.env` configs and change accordingly.
1. Get dependent **datasets** from **project space** and place under `./data`.
1. **Deployment** or **Development** scenarios:
   1. **Deployment**:
      1. Run `docker-compose up -d` to start containers.
      1. Run `docker-compose run api make test` to check your setup is correct via unit testing.
         If things go wrong, double check previous steps, and check configs in `.env`.
   1. **Development**:
      1. Run `docker-compose -f docker-compose-dev.yml up -d` to start containers.
      1. Run `docker-compose -f docker-compose-dev.yml run api make test` to check your setup is correct via unit testing.
         If things go wrong, double check previous steps, and check configs in `.env`.

## Development

- The API tech stack:
  - fastapi: https://fastapi.tiangolo.com/
  - poetry: https://python-poetry.org/
  - pytest: https://pytest.org/
  - requests: https://requests.readthedocs.io/en/master/
- `docker-compose-dev.yml` allows for live-reloading via host volume mapping.
  The server will reload once you make changes.
- Before pushing commits, **always** run `docker-compose -f docker-compose-dev.yml run api make test`.
  to ensure your changes don't break stuff.

## Advanced

- **Local** development:
  - Use `environment-base.yml` to bootstrap a barebone python virtual env, then `poetry install`.
  - Or use `environment.yml` if you don't need to mess with package dependency.
- Use `make fmt` to do code formatting.
- Use `make lint` to do code linting.

## Environment variables

file: `.env`

variables:

- `<API>`:
  - DEBUG
  - DOCKER_API_PORT
  - API_PRIVATE_ACCESS: determines if the api is a service with private endpoints
  - API_KEY
- `<EpiGraphDB platform>`:
  - EPIGRAPHDB_DB_BROWSER
- `<EpiGraphDB graph>`:
  - EPIGRAPHDB_PORT
  - EPIGRAPHDB_SERVER
  - EPIGRAPHDB_USER
  - EPIGRAPHDB_PASSWD
  - EPIGRAPHDB_DB_VERSION
- `<pQTL graph>`:
  - PQTL_SERVER
  - PQTL_PORT
  - PQTL_USER
  - PQTL_PASSWD
  - PQTL_DB_VERSION
- `<EpiGraphDB docs>`:
  - EPIGRAPHDB_API_URL
