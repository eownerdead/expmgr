#!/usr/bin/env sh

PROJECT_NAME="expmgr"

yapf -ir ./$PROJECT_NAME
isort ./$PROJECT_NAME
