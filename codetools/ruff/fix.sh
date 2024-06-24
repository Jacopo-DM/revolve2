#!/bin/sh

cd "$(dirname "$0")"

packages=$(../read_project_parts.sh)

cd ../..

# packages=$(git ls-files | grep -E '\.py$' | xargs dirname | sort | uniq)

if [ -n "$packages" ]; then
    echo "$packages" | xargs
	ruff clean
    ruff check $packages --fix --unsafe-fixes --preview --silent
    ruff format $packages --preview
fi
