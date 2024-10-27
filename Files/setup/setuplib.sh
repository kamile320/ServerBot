#!/bin/bash

echo ServerBot module Auto-Setup
echo This .sh file will download all needed modules for Python script

sleep 2
echo "This file uses Advanced Packaging Tool - APT. If you don't have pip3 or ffmpeg and you are running script on not-APT-Based system (Fedora/SUSE/etc.), you must edit this file"
sleep 1
echo "If you are not in pip3 venv, you must create a new one (not Ubuntu 22.04 based Operating Systems)"
sleep 1
read -p "Type anything to continue. (Need root privileges)"

sudo apt install python3-pip
sudo apt install ffmpeg

pip3 install discord
pip3 install discord.py[voice]
pip3 install datetime
pip3 install psutil
pip3 install asyncio
pip3 install openai==0.28.1
pip3 install ffmpeg
pip3 install python-dotenv
pip3 install requests
pip3 install pyfiglet

echo "'Externally managed' error? Run 'mkvenv.sh' script from 'Files/setup' directory to easily create one."

echo "Done. In Discord Server you can create Desktop shortcut using '.mkshortcut' and add ServerBot to system startup using '.mksysctlstart'"
read -p "Type anything to continue.."

python3 ServerBot.py