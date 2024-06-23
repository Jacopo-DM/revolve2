#!/bin/sh

set -e

cd "$(dirname "$0")"

START_DIR="$(pwd)"

PIPELINE=(
    './mypy/check_all.sh'
    # './black/fix.sh'
    # './isort/fix.sh'
    # './sort_all/fix.sh'
    './ruff/fix.sh'
    './pyflakes/check.sh'
    './pydocstyle/check.sh'
    './darglint/check.sh'
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
