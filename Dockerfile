################################
# BUILDER
# Sets up all our shared environment variables and install deps
################################
FROM python:3.12.2-slim-bookworm AS builder

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PYTHONDONTWRITEBYTECODE=1 \
    # pip:
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_ROOT_USER_ACTION=ignore \
    # poetry:
    POETRY_VERSION=1.8.3 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=true

ENV USER app_user

RUN apt-get update && \
    apt-get install gcc curl -y && \
    apt-get autoremove --purge && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -ms /bin/bash ${USER}
RUN mkdir -p /home/${USER}/app && \
    chown ${USER}:${USER} /home/${USER}/app

WORKDIR /home/${USER}/app

# install deps
# RUN pip install --upgrade pip
# This will install Poetry and its dependencies into your main site-packages/
# RUN pip install poetry==${POETRY_VERSION}

# To install from curl, remember to config poetry at pyproject.toml
# requires = ["poetry-core>=1.6"]
# build-backend = "poetry.core.masonry.api"
RUN curl -sSL https://install.python-poetry.org | python3 -

# Copy and install deps
COPY pyproject.toml poetry.lock ./
RUN pip install poetry-plugin-bundle
# RUN poetry bundle venv --without dev /home/${USER}/app/.venv

ARG TEST_ENV=false
RUN if [ "$TEST_ENV" = "true" ]; then \
        poetry bundle venv --with test /home/${USER}/app/.venv; \
    else \
        poetry bundle venv --without dev /home/${USER}/app/.venv; \
    fi

################################
# TEST-STAGE
# Run tests
################################
FROM builder AS test-stage


ENV PATH="/home/${USER}/app/.venv/bin:$PATH"

RUN mkdir -p /home/${USER}/app

# Copy application code for testing
COPY . /home/${USER}/app/

WORKDIR /home/${USER}/app

# Run tests
USER ${USER}
RUN poetry run pytest


################################
# FINAL-STAGE
# Copy deps from builder and start application
################################
FROM python:3.12-slim-bookworm AS final-stage

ENV USER app_user
EXPOSE 8000

# add non-root user
RUN useradd -ms /bin/bash ${USER}
RUN mkdir -p /home/${USER}/app && \
    chown ${USER}:${USER} /home/${USER}/app

WORKDIR /home/${USER}/app

# Copy virtual environment
COPY --from=builder /home/${USER}/app/.venv /home/${USER}/app/.venv

ENV VIRTUAL_ENV=/home/${USER}/app/.venv \
    PATH="/home/${USER}/app/.venv/bin:$PATH"

# Copy application
COPY ./src /home/${USER}/app/

# set user to run app
USER ${USER}
ENV PYTHONPATH "/home/${USER}/app"

# Set entrypoint
ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
