#!/bin/bash

python3 -m venv venv
. venv/bin/activate
pip install pip-tools
pip-sync
