#!/bin/bash

echo "Python3 virtual environment creating script."

read -p "Type anything to continue. (Need root privileges)"

sudo apt update -y
sudo apt install -y python3-venv
python3 -m venv .venv

source .venv/bin/activate

bash setup.sh