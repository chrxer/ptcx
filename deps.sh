#!/usr/bin/env bash 

set -e

sudo apt install python3
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi
./.venv/bin/python3 -m pip install --upgrade pip 
./.venv/bin/python3 -m pip install -r requirements.txt -r requirements-dev.txt