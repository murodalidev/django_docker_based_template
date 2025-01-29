FROM docker.io/python:3.12.7-slim-bullseye AS python

WORKDIR /usr/src/app

# Create devcontainer user and add it to sudoers
RUN addgroup --system app && adduser --system --group app

# Install additional dependencies
RUN apt-get update --fix-missing && \
    apt-get install --no-install-recommends -y \
    libc-dev \
    build-essential \
    python3-dev \
    libpq-dev \
    gettext \
    shared-mime-info && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

 # Requirements are installed here to ensure they will be cached.
COPY ./requirements ./requirements

RUN pip install --upgrade pip setuptools wheel

RUN pip install -r requirements/local.txt

COPY ./compose/local/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/local/django/start /start-django
RUN sed -i 's/\r$//g' /start-django
RUN chmod +x /start-django

COPY ./compose/local/django/celery/worker/start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker

COPY ./compose/local/django/celery/beat/start /start-celerybeat
RUN sed -i 's/\r$//g' /start-celerybeat
RUN chmod +x /start-celerybeat

COPY ./compose/local/django/celery/flower/start /start-celeryflower
RUN sed -i 's/\r$//g' /start-celeryflower
RUN chmod +x /start-celeryflower

# copy application code to WORKDIR
COPY . .

RUN chown -R app:app /usr/src/app

USER app

ENTRYPOINT ["/entrypoint"]
