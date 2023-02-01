# Do all the development in Docker since poetry sucks at env management
ARG PYTHON_VERSION=3.9
FROM python:$PYTHON_VERSION-slim-buster AS base
ARG USERNAME=vorboss

# TODO: For full Docker dev I would want to have neovim + lsp
RUN apt-get update \
    && apt-get install --no-install-recommends -yq \
    git \
    jq \
    htop \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean \
    && adduser --disabled-password --gecos "" $USERNAME


WORKDIR /app
FROM base as builder

ARG POETRY_VERSION=1.1.13

ENV USERNAME=$USERNAME \
    # output python directly to stdout
    PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # poetry
    # https://python-poetry.org/docs/configuration/#using-environment-variables
    POETRY_VERSION=$POETRY_VERSION \
    # make poetry install to this location
    POETRY_HOME=/home/$USERNAME/poetry \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1 \
    # cache dir
    POETRY_CACHE_DIR=/tmp \
    # virtual envs dir
    POETRY_VIRTUALENVS_PATH=/home/$USERNAME/venvs \
    # home dir
    HOME=/home/$USERNAME \
    # add poetry to path
    PATH=/home/$USERNAME/poetry/bin:$PATH

# install poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN curl -sSL https://install.python-poetry.org | python3 -

RUN pip install "poetry==$POETRY_VERSION"
RUN python -m venv /venv

COPY pyproject.toml poetry.lock ./
RUN . /venv/bin/activate && poetry install --no-dev --no-root

COPY . .
RUN . /venv/bin/activate && poetry build

FROM base as dev

COPY --from=builder /venv /venv
COPY --from=builder /app/dist .

# activate env on startup
RUN echo "source $(poetry env info --path)/bin/activate" >> ~/.bashrc

# copy codes
COPY --chown=$USERNAME pcreations pcreations
#COPY README.rst README.rst

CMD ["poetry check"]
#CMD ["poetry", "run", "jupyter", "lab", "--no-browser", "--ip=0.0.0.0", "--NotebookApp.token=''", "--NotebookApp.password=''", "--allow-root"]
