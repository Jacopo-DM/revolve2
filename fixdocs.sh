#!/bin/bash

set -e

cd "$(dirname "$0")"

while read -r package; do
    echo "$package:"

    docconvert $package -o rest --in-place

    for py_file in $(find $package -name "*.py"); do
        echo "Processing $py_file"
        docformatter --in-place $py_file || true
    done

    # pyment $package -w -o numpydoc -d
    pyment $package -w -o reST -d
    ruff clean
    ruff check $package --fix --unsafe-fixes --preview --silent
    ruff format $package --preview
done < <(./codetools/read_project_parts.sh)