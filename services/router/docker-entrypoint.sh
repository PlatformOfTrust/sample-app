#!/bin/sh
set -exuo pipefail

exec haproxy -W -db -f haproxy.cfg
