#!/bin/bash

echo ServerBot module Auto-Setup
echo This .sh file will download all needed modules for Python script

sleep 2
echo "This file uses Advanced Packaging Tool - APT. If you don't have pip3 or ffmpeg and you are running script on not-APT-Based system (Fedora/SUSE/etc.), you must edit this file"
sleep 1
echo "If you are not in pip3 venv, you must create a new one (Not Ubuntu 22.04 based Operating Systems)"
sleep 1
read -p "Type anything to continue. (Need root privileges)"

sudo apt update -y
sudo apt install -y python3-pip ffmpeg python3-venv git

pip3 install -r Files/setup/requirements.txt

echo "'Externally managed' error? Run 'mkvenv.sh' script from 'Files/setup' directory to easily create one."
sleep 1

echo "Done. In Discord Server you can create Desktop shortcut using '.mkshortcut' and add ServerBot to system startup using '.mksysctlstart'"
read -p "Type anything to continue.."

python3 ServerBot.py
