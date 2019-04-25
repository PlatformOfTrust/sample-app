#!/usr/bin/env sh
set -exuo pipefail

exec haproxy -W -db -f haproxy.cfg
