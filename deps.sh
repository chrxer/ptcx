#!/usr/bin/env bash 

set -e

for arg in "$@"; do
    if [[ "$arg" == "--force-sudo" || "$arg" == "-f" ]]; then
        echo "Warning: --force-sudo provided, always using sudo"
        FORCESU=1
    else
        echo "Invalid argument: $arg"
        exit 1
    fi
done


stmp() {
    date +"%m-%d %T"
}

USER=$(awk -F: '$3 >= 1000 && $3 < 60000 {print $1; exit}' /etc/passwd)

nsu() {
    printf "\033[94m[EXC %s]\033[0m %s\n" "$(stmp)" "$*"
    if [[ "$FORCESU" == "1" ]]; then
        sudo env "PATH=$PATH" "$@"
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
if [ ! -d "$WRK/.venv" ]; then
  nsu python3 -m venv $WRK/.venv
fi

nsu sudo chmod +x $WRK/mkdocs.py
nsu $WRK/.venv/bin/python3 -m pip install --upgrade pip 
nsu $WRK/.venv/bin/python3 -m pip install -r $WRK/requirements.txt -r $WRK/requirements-dev.txt