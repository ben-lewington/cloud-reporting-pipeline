FROM python:3.10-slim as base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.7.1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true

RUN pip install poetry==${POETRY_VERSION}

WORKDIR /app

FROM base as release

COPY pyproject.toml poetry.* *.md ./
COPY pipeline pipeline

RUN python -m venv /.build
RUN poetry export --without=dev | /.build/bin/pip install -r /dev/stdin
RUN poetry build && /.build/bin/pip install dist/*.whl

FROM base as dev

ENV PYTHONPYCACHEPREFIX="/tmp"

FROM cgr.dev/chainguard/python as deploy

COPY run run
WORKDIR /run

ENTRYPOINT [ "python" ]
