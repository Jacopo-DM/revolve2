#!/bin/bash

set -e

cd "$(dirname "$0")"

while read -r package; do
    echo "$package:"
    # docconvert $package -o rest --in-place
    pyment $package -w -o numpydoc -d
done < <(./codetools/read_project_parts.sh)