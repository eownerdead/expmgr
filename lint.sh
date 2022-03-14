#!/usr/bin/env sh

PROJECT_NAME="expmgr"

flake8 --show-source ./$PROJECT_NAME
mypy --pretty ./$PROJECT_NAME
