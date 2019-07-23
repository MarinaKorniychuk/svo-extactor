FROM 516380634521.dkr.ecr.us-east-1.amazonaws.com/ner/prodigy:1.8.3-2

ENV PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=0.12.11

WORKDIR /facts

RUN savedAptMark="$(apt-mark showmanual)" \
    && apt-get update \
    && apt-get install -y curl --no-install-recommends \
    \
    && curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py > get-poetry.py \
    && python get-poetry.py --version $POETRY_VERSION \
    && ln -s $HOME/.poetry/bin/poetry /usr/local/bin/poetry \
	&& poetry --version \
    \
    && rm -f get-poetry.py \
	&& apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false

COPY poetry.lock pyproject.toml ./

RUN poetry config settings.virtualenvs.create false \
    && poetry install --no-interaction --no-ansi -vvv

COPY . ./

ENTRYPOINT ["python", "-m", "facts"]
