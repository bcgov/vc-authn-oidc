FROM python:3.11 as main

WORKDIR /app

ENV POETRY_VIRTUALENVS_CREATE=false
RUN pip3 install --no-cache-dir poetry

COPY pyproject.toml poetry.lock README.md ./
RUN poetry install --only main

COPY ./oidc-controller .

EXPOSE 5000

RUN ["chmod", "+x", "./docker-entrypoint.sh"]

ENTRYPOINT ["./docker-entrypoint.sh"]
