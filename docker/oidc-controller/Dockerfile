FROM python:3.12 as main

WORKDIR /app

COPY oidc-controller/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY oidc-controller ./

EXPOSE 5000

RUN ["chmod", "+x", "./docker-entrypoint.sh"]

ENTRYPOINT ["./docker-entrypoint.sh"]