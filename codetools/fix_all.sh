#!/bin/sh

set -e

cd "$(dirname "$0")"

START_DIR="$(pwd)"

PIPELINE=(
    './mypy/check_all.sh'
    './ruff/fix.sh'
    './pyflakes/check.sh'
    './pydoclint/check.sh'
)

for var in ${PIPELINE[@]}
    do
        echo "--------------"
        echo "${var}"
        echo "--------------"
        eval $var
        echo
    done

cd $START_DIR
