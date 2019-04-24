#!/usr/bin/env sh
set -exu

if [[ ! -d "${WORKON_HOME}" ]]; then
    mkdir "${WORKON_HOME}"
fi

rm -rf "${WORKON_HOME}"/*

pip install --upgrade pip
pip install pipenv==11.10.1
pipenv install

pipenv run pip install uwsgi==2.0.17
