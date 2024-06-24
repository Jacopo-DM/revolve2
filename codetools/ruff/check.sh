#!/bin/sh

cd "$(dirname "$0")"

packages=$(../read_project_parts.sh)

cd ../..

ruff check $packages --diff