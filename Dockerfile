# FROM python:3

FROM python:3.9-slim-bullseye

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY . /code/

RUN pip install pipenv
# RUN apt-get update && apt-get install -y --no-install-recommends gcc
COPY Pipfile .
COPY Pipfile.lock .
# RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy
# RUN pipenv shell
RUN pipenv install django autopep8 pylint djangorestframework django-cors-headers pylint-django


# FROM python:3.7-slim as base

# # Setup env
# ENV LANG C.UTF-8
# ENV LC_ALL C.UTF-8
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONFAULTHANDLER 1


# FROM base AS python-deps

# # Install pipenv and compilation dependencies
# RUN pip install pipenv
# RUN apt-get update && apt-get install -y --no-install-recommends gcc
# # RUN pipenv shell
# RUN pipenv install django autopep8 pylint djangorestframework django-cors-headers pylint-django

# # Install python dependencies in /.venv
# COPY Pipfile .
# COPY Pipfile.lock .
# RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy


# FROM base AS runtime

# # Copy virtual env from python-deps stage
# COPY --from=python-deps /.venv /.venv
# ENV PATH="/.venv/bin:$PATH"

# # Create and switch to a new user
# RUN useradd --create-home appuser
# WORKDIR /home/appuser
# USER appuser

# # Install application into container
# COPY . .

# # Run the application
# ENTRYPOINT ["python", "-m", "http.server"]
# CMD ["--directory", "directory", "8000"]
