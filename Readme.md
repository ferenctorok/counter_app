# A basic example web API that implements a counter

- [A basic example web API that implements a counter](#a-basic-example-web-api-that-implements-a-counter)
  - [Usage](#usage)
    - [Build docker images](#build-docker-images)
    - [Run the example with docker compose](#run-the-example-with-docker-compose)
    - [Run tests](#run-tests)
    - [Code checking](#code-checking)
    - [OpenAPI description](#openapi-description)


## Usage

### Build docker images

The app uses 2 docker images: one for the database, and one for the app itself.
To build these images, you need to execute the 2 build scripts:

```bash
bash docker/build_database_image.sh
bash docker/build_app_image.sh
```

This builds the following 2 images:

- `counter_database:latest`: When started, it also launches a postgreSQL
database. The config parameters of the database can be given over as environment
variables. The environment variables that can be set and their default values
are as follows:
  - `POSTGRES_USER=appuser`
  - `POSTGRES_PASSWORD=secret`
  - `POSTGRES_DB=appdb`
  - `POSTGRES_PORT=5432`
  - `POSTGRES_DATA_DIR=/var/lib/postgresql/data`
- `counter_app:latest`: The container that contains all dependencies for running
  the app itself. When started, it doesn't automatically start the app itself.
  The reason for this is that I also wanted to use this image for the
  devcontainer during development. (Of course this is debatable, because this
  way it also contains a couple of dependencies that are not strictly necessary
  for running the app itself, but I didn't want to make the docker setup more
  complicated.) Similarly to the database image, in this image there are also
  environment variables to configure the database connection. You can set these
  when starting the container. The following environment variables are available
  to set:
  - `POSTGRES_USER=appuser`
  - `POSTGRES_PASSWORD=secret`
  - `POSTGRES_DB=appdb`
  - `POSTGRES_HOST=db`
  - `POSTGRES_PORT=5432`


### Run the example with docker compose

You can start up the database and the application by executing

```bash
docker compose up
```

in the root of the repository.

This should start up the database container, wait until that is fully
initialized, and then launch the app container as well. Then you should be able
to go to `http://0.0.0.0:80/docs` to interact with the app.

You can try out changing the configs of the database by editing the environment
variables in `docker-compose.yml`.

### Run tests

To be able to run the tests, mount the repo into a running instance of
`counter_app:latest`. The easiest is to open it with the devcontainer extension
of VSCode. The repo contains a `devcontainer.json` file that sets up everything
(mounts, port forwarding, extensions, python lib installation.).

To run the tests, just execute

```bash
python3 -m pytest
```

### Code checking

The code checking is automated with pre-commit, which is also installed into
`counter_app:latest`. To run all checks, execute

```bash
pre-commit run --all-files
```

To see the checks that pre-commit runs, see `.pre-commit-config.yaml`. To see
how ruff and mypy are set up, see the respective files under
`.code_checker_configs/`


### OpenAPI description

The descreption of the API in the OpenAPI format can be found in
`counter_app/openapi/openapi.json`.
