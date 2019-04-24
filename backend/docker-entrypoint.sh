#!/usr/bin/env sh
set -exu

set -- pipenv run invoke dev

exec "$@"
