#!/bin/bash

OPTIONS=(1 "Start Bot"
         2 "Start Bot (not venv)"
         3 "Download pip3 libraries"
         4 "Create Python3 venv in current dir"
         5 "Create .env file")

select=$(dialog --clear \
--backtitle "ServerBot v1.4" \
--title "ServerBot Setup" \
--menu "Select Operation:" \
18 52 4 \
"${OPTIONS[@]}" \
2>&1 >/dev/tty)

clear

case $select in
        1)
            echo "Starting ServerBot.py ..."
            ./.venv/bin/python ServerBot.py
            ;;
        2)
            echo "Starting ServerBot.py..."
            python3 ServerBot.py
            ;;
        3)  echo "Running installation script..."
            Files/setup/setuplib.sh
            ;;
        4)  echo "Running installation script..."
            Files/setup/mkvenv.sh
            ;;
        5)  echo "Creating .env file..."
            echo 'TOKEN=""' >> .env
            echo 'OpenAI=""' >> .env
            echo "admin_usr = ['']" >> .env
            sleep 1
            ./setup.sh
            ;;
esac