FROM node:10.15.3-alpine

ENV ENV="development" \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8 \
    WORKON_HOME="/.venv"

ADD . /src/sample-app/frontend
WORKDIR /src/sample-app/frontend

RUN chmod +x setup.sh && ./setup.sh

EXPOSE 8080

ENTRYPOINT ["/src/sample-app/frontend/docker-entrypoint.sh"]
