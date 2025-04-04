#!/usr/bin/env bash 

set -e

stmp() {
    date +"%m-%d %T"
}

USER=$(awk -F: '$3 >= 1000 && $3 < 60000 {print $1; exit}' /etc/passwd)

nsu() {
    printf "\033[94m[EXC %s]\033[0m %s\n" "$(stmp)" "$*"
    sudo -u "$USER" env "PATH=$PATH" "$@"
}

asu() {
    printf "\033[94m[EXC %s]\033[0m sudo %s\n" "$(stmp)" "$*"
    sudo env "PATH=$PATH" "$@"
}

asu  apt install python3
if [ ! -d ".venv" ]; then
  nsu python3 -m venv .venv
fi
asu sudo chmod +x mkdocs.py
nsu ./.venv/bin/python3 -m pip install --upgrade pip 
nsu ./.venv/bin/python3 -m pip install -r requirements.txt -r requirements-dev.txt