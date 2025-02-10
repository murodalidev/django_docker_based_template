FROM docker.io/python:3.12.7-slim-bullseye AS python

WORKDIR /usr/src/app

# Create devcontainer user and add it to sudoers
RUN addgroup --system app && adduser --system --group app

RUN echo "deb https://nexus.asakabank.uz/repository/Debian-deb/ bullseye main contrib non-free" > /etc/apt/sources.list && \
    echo "deb https://nexus.asakabank.uz/repository/Debian-security/ bullseye-security main contrib non-free" >> /etc/apt/sources.list

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

RUN pip install -r requirements/production.txt

COPY ./compose/general/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/production/django/start /start-django
RUN sed -i 's/\r$//g' /start-django
RUN chmod +x /start-django

COPY ./compose/general/django/celery/worker/start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker

COPY ./compose/general/django/celery/beat/start /start-celerybeat
RUN sed -i 's/\r$//g' /start-celerybeat
RUN chmod +x /start-celerybeat

COPY ./compose/general/django/celery/flower/start /start-celeryflower
RUN sed -i 's/\r$//g' /start-celeryflower
RUN chmod +x /start-celeryflower

# Create staticfiles directory and set permissions
RUN mkdir -p /usr/src/app/staticfiles && \
    chown -R app:app /usr/src/app/staticfiles && \
    chmod -R 755 /usr/src/app/staticfiles

# copy application code to WORKDIR
COPY . .

RUN chown -R app:app /usr/src/app

USER app

ENTRYPOINT ["/entrypoint"]
