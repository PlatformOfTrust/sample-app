# python:3.6-alpine3.9 specific working version
FROM python@sha256:ad2b24eacc9865244d7b1ae198d507f4ce8f506484c35d27158e7f1dd6041a8b

ENV ENV="development"
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV WORKON_HOME="/.venv"

COPY ./docker-entrypoint.sh /

ADD . /src/sample-app/frontend
WORKDIR /src/sample-app/frontend

RUN apk add --update --no-cache --virtual build-dependencies \
    nodejs \
    npm \
 && chmod +x *.sh /*.sh \
 && ./setup.sh

EXPOSE 8080

ENTRYPOINT ["/docker-entrypoint.sh"]
