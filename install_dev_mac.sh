#!/bin/sh

# Installs all Revolve2 packages in editable mode as well as all example requirements.
# This is the same as installing `requirements_editable.txt`.

cd "$(dirname "$0")"

# ↓ git pull robot hat (to run once)
cd ..
git clone git@github.com:ci-group/robohat.git
cd robohat
pip install -e .
cd ../revolve2

pip install -r ./requirements_dev_mac.txt

# ↓ git pull revolve2 (to run once)
cd ..
git clone git@github.com:dadadel/pyment.git
cd pyment
pip install -e .
cd ../revolve2