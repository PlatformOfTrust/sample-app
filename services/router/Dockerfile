FROM haproxy:1.9-alpine

ENV ENV="development"
ENV SAMPLE_APP_HOST="sample-app.local"

COPY . /usr/local/etc/haproxy/
WORKDIR "/usr/local/etc/haproxy/"

RUN chmod +x *.sh

ENTRYPOINT ["./docker-entrypoint.sh"]
