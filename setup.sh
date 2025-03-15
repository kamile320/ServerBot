#!/bin/bash

VERSION="v1.6.3"
UPDATEVER="v1.6.3"

OPTIONS=(1 "Start Bot"
         2 "Start Bot (not venv)"
         3 "Download pip3 libraries"
         4 "Create Python3 venv in current dir"
         5 "Create .env file"
         6 "Enter to Python3 venv"
         7 "Manually create systemctl entry"
         8 "Install ServerBot from GitHub")

select=$(dialog --clear \
--backtitle "ServerBot ${VERSION}" \
--title "ServerBot Setup" \
--menu "Select Operation:" \
18 52 8 \
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
        3)  
            echo "Running installation script..."
            Files/setup/setuplib.sh
            ;;
        4)  
            echo "Running installation script..."
            Files/setup/mkvenv.sh
            ;;
        5)  
            echo "Creating .env file..."
            echo "TOKEN=''" >> .env
            echo "OpenAI=''" >> .env
            echo "admin_usr = ['']" >> .env
            echo "mod_usr = ['']" >> .env
            echo "#command_dscserv" >> .env
            echo "dscserv_link = 'https://discord.gg/UMtYGAx5ac'" >> .env
            echo "#command_addbot" >> .env
            echo "addstable = 'stable_link'" >> .env
            echo "addtesting = 'testing_link'" >> .env
            echo "#service_list" >> .env
            echo "service_list = ','" >> .env
            sleep 1
            ./setup.sh
            ;;
        6)
            echo "Entering to Python3 virtual environment..."
            source .venv/bin/activate
            bash setup.sh
            ;;
        7)
            echo "Starting sysctladd.py..."
            python3 Files/sysctladd.py
            ;;
        8)
            echo "Install ServerBot from Github..."
            echo "This option is useful when you want to update Bot or fix/rebuild critical files."
            echo "As default, this option will install ServerBot ${UPDATEVER} in a new directory."
            echo "You can change it for other release."
            echo "Installer uses git command. Make sure you have downloaded it."
            read -p "Type anything to continue."
            cd ..
            git clone -b ${VERSION} https://github.com/kamile320/ServerBot SB_Update
            ;;
esac