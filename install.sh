#!/bin/bash

python3 -m venv venv
. venv/bin/activate
pip install Flask
pip install Flask-HTTPAuth
export FLASK_APP=api