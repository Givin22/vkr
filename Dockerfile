# Dockerfile

# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.12-slim

ENV POETRY_VERSION=1.8.2 \
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local' \
  PYTHONUNBUFFERED=1

WORKDIR /vkr

RUN pip install poetry==${POETRY_VERSION}

# Allows docker to cache installed dependencies between builds
COPY poetry.lock /poetry.lock
COPY pyproject.toml /pyproject.toml

RUN poetry install

# Mounts the application code to the image
COPY . /vkr
EXPOSE 80

# runs the production server
CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]
