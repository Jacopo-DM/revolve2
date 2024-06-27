#!/bin/bash

set -e

cd "$(dirname "$0")"

while read -r package; do
    echo "$package:"

    docconvert $package -o rest --in-place || true

    for py_file in $(find $package -name "*.py"); do
        echo "Processing $py_file"
        docformatter --in-place $py_file || true
        # ↓ pull from github (pipy version is broken)
        pyment -w -o reST -d $py_file || true
    done

    # pyment $package -w -o numpydoc -d
    ruff check $package --fix --unsafe-fixes --preview || true
    ruff format $package --preview
    ruff clean
done < <(./codetools/read_project_parts.sh)