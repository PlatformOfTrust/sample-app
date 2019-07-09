#!/usr/bin/env sh
set -exuo pipefail

set -- pipenv run invoke dev

exec "$@"
