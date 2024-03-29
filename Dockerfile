FROM python:3.7.4-slim as python-base
ENV PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_PATH=/opt/poetry \
    VENV_PATH=/opt/venv \
    POETRY_VERSION=0.12.17
ENV PATH="$POETRY_PATH/bin:$VENV_PATH/bin:$PATH"

FROM python-base as poetry
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        # deps for installing poetry
        curl \
        # deps for building python deps
        build-essential \
    \
    # install poetry - uses $POETRY_VERSION internally
    && curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python \
    && mv /root/.poetry $POETRY_PATH \
    && poetry --version \
    \
    # configure poetry & make a virtualenv ahead of time since we only need one
    && python -m venv $VENV_PATH \
    && poetry config settings.virtualenvs.create false \
    \
    # cleanup
    && rm -rf /var/lib/apt/lists/*

COPY poetry.lock pyproject.toml ./
RUN poetry install --no-interaction --no-ansi -vvv

FROM python-base as runtime
WORKDIR /facts

COPY --from=poetry $POETRY_PATH $POETRY_PATH
RUN poetry config settings.virtualenvs.create false
COPY --from=poetry $VENV_PATH $VENV_PATH

# stopgap for https://github.com/sdispater/poetry/issues/1297 - when fixed, install to pyproject.toml
RUN pip install --no-cache-dir --no-deps \
        https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.1.0/en_core_web_sm-2.1.0.tar.gz#egg=en_core_web_sm

COPY . ./

ENTRYPOINT ["python", "-m", "facts"]
