FROM python:3.10

WORKDIR /app

COPY oidc-controller/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY oidc-controller ./

EXPOSE 5000
ENTRYPOINT ["./docker-entrypoint.sh"]