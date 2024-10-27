#!/bin/bash

OPTIONS=(1 "Start Bot"
         2 "Start Bot (not venv)"
         3 "Download pip3 libraries"
         4 "Create Python3 venv in current dir")

select=$(dialog --clear \
--backtitle "ServerBot v1.0" \
--title "ServerBot Setup" \
--menu "Select Operation:" \
15 50 4 \
"${OPTIONS[@]}" \
2>&1 >/dev/tty)

clear

case $select in
        1)
            echo "Starting ServerBot.py ..."
            ./.venv/bin/python ServerBot.py
            ;;
        2)
            echo "Starting ServerBot.py ..."
            python3 ServerBot.py
            ;;
        3)  echo "Running installation script ..."
            Files/setup/setuplib.sh
            ;;
        4)  echo "Running installation script ..."
            Files/setup/mkvenv.sh
            ;;
esac