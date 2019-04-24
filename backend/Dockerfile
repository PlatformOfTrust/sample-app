# python:3.6-alpine3.9 specific working version
FROM python@sha256:ad2b24eacc9865244d7b1ae198d507f4ce8f506484c35d27158e7f1dd6041a8b

ENV ENV="development" \
	LC_ALL=C.UTF-8 \
	LANG=C.UTF-8 \
	WORKON_HOME="/.venv" \
	PYTHONUNBUFFERED=1

ADD . /src/sample-app/backend
WORKDIR /src/sample-app/backend

RUN apk add --update --no-cache --virtual build-dependencies \
    python3-dev \
    build-base \
    linux-headers \
 && chmod +x *.sh \
 && ./setup.sh \
 && apk del build-dependencies

EXPOSE 8080

ENTRYPOINT ["./docker-entrypoint.sh"]

