# fact-extract
Extract facts from the internet as SVO triples


## Usage
`fact-extract` is distributed as a CLI built in docker. To use it, just run the docker image:

```shell
$ docker run -it facts [OPTIONS] COMMAND [ARGS]
```


## Development
You can build & run the docker image simply using the following commands:

```shell
$ docker build -t facts .
$ docker run -it facts
```

Alternatively, a `docker-compose.yml` file is provided that wraps most functionality you should need,
and mirrors in your local code so that you can run & develop changes faster:

```shell
$ docker-compose run facts  # implies docker-compose build facts if the image doesn't exist
```

### Dependencies
We use [poetry](https://poetry.eustace.io/) for packaging & dependency management. If you'd like to 
install a new dependency (i.e. `requests`), use the following command:

```shell
$ docker-compose run poetry add requests
```

**Note:** docker containers are not persistent, so this will only change the `pyproject.toml` and `poetry.lock`.
Remember to rebuild the image so that subsequent calls to `docker-compose` will have the new dependencies:
```shell
$ docker-compose build facts
```

Since the Docker image is built off of the [prodigy-docker](https://github.com/fintechstudios/prodigy-docker) image, your
environment will also implicitly have access to all the packages installed there. Keep this in mind, as there may be
version conflicts when you add dependencies.


### Lint
Strict code style is enforced through [`black`](https://github.com/psf/black). Code that does
not pass linting will not be accepted. [Editor integrations](https://black.readthedocs.io/en/stable/editor_integration.html)
exist to make your life easier - otherwise, reformat your files before commit by running:

```shell
$ docker-compose run lint
```

### Unit Tests
Unit tests are written with [`pytest`](https://github.com/pytest-dev/pytest). They should be added
to the `tests/` folder, organized to match the file structure of the `facts/` folder. Run
the tests with:

```shell
$ docker-compose run unit
```
