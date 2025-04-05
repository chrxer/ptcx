#!/usr/bin/env bash 

set -e

stmp() {
    date +"%m-%d %T"
}

USER=$(awk -F: '$3 >= 1000 && $3 < 60000 {print $1; exit}' /etc/passwd)

nsu() {
    printf "\033[94m[EXC %s]\033[0m %s\n" "$(stmp)" "$*"
    if [[ ! -z "$CI" ]]; then
        sudo "$@"
    else
        sudo -u "$USER" env "PATH=$PATH" "$@"
    fi
}

asu() {
    printf "\033[94m[EXC %s]\033[0m sudo %s\n" "$(stmp)" "$*"
    sudo env "PATH=$PATH" "$@"
}

WRK=$(dirname "$0")
asu  apt install python3
echo "WRK:$WRK"
if [ ! -d "$WRK/.venv" ]; then
  nsu python3 -m venv $WRK/.venv
fi

nsu sudo chmod +x $WRK/mkdocs.py
nsu $WRK/.venv/bin/python3 -m pip install --upgrade pip 
nsu $WRK/.venv/bin/python3 -m pip install -r $WRK/requirements.txt -r $WRK/requirements-dev.txt