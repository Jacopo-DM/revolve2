#!/bin/sh

cd "$(dirname "$0")"

packages=$(../read_project_parts.sh)

cd ../..

pydoclint --style sphinx $packages --check-return-types=False
