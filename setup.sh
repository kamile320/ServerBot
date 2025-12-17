#!/bin/bash

VERSION="v1.10.0"
UPDATEVER="v1.10.0"

OPTIONS=(1 "Start Bot"
         2 "Start Bot (not venv)"
         3 "Download pip3 libraries"
         4 "Create Python3 venv in current dir"
         5 "Create .env file"
         6 "Enter to Python3 venv"
         7 "Manually create systemctl entry"
         8 "Systemctl service options"
         9 "Other options")

OPTIONS_sctl=(1 "Enable"
              2 "Disable"
              3 "Start"
              4 "Stop"
              5 "Status"
              6 "Remove"
              7 "Return")

OPTIONS_other=(1 "Edit .env"
               2 "Install ServerBot from GitHub"
               3 "Manual"
               4 "Return")

OPTIONS_YN=(1 "Yes"
            2 "No")

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
            ./.venv/bin/python ServerBot.py $*
            ;;
        2)
            echo "Starting ServerBot.py..."
            python3 ServerBot.py $*
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
            echo "AI_token=''" >> .env
            echo "admin_usr = ['']" >> .env
            echo "#command_dscserv" >> .env
            echo "dscserv_link = 'https://discord.gg/UMtYGAx5ac'" >> .env
            echo "#command_addbot" >> .env
            echo "addstable = 'stable_link'" >> .env
            echo "addtesting = 'testing_link'" >> .env
            echo "#service_list" >> .env
            echo "service_monitor = False" >> .env
            echo "service_list = ','" >> .env
            echo "#modules" >> .env
            echo "showmodulemessages = False" >> .env
            echo "ACLmodule = False" >> .env
            echo "#ai" >> .env
            echo "aimodel = 'gemini-2.5-flash'" >> .env
            echo "instructions = ['Answer with max 1500 characters','Always answer in users language','Be precise and truthseeking','Do not answer to illegal, harmful, sexual or violent content']" >> .env
            echo "#extendedErrMess" >> .env
            echo "extendedErrMess = False" >> .env
            sleep 1
            bash setup.sh
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
            select_sctl=$(dialog --clear \
            --backtitle "ServerBot ${VERSION}" \
            --title "Systemctl service options" \
            --menu "These operations will work only if the ServerBot.service exists" \
            18 52 8 \
            "${OPTIONS_sctl[@]}" \
            2>&1 >/dev/tty)

            clear

            case $select_sctl in 
                    1)
                        sudo systemctl enable ServerBot
                        bash setup.sh
                        ;;
                    2)
                        sudo systemctl disable ServerBot
                        bash setup.sh
                        ;;
                    3)
                        sudo systemctl start ServerBot
                        bash setup.sh
                        ;;
                    4)
                        sudo systemctl stop ServerBot
                        bash setup.sh
                        ;;
                    5)
                        sudo systemctl status ServerBot
                        bash setup.sh
                        ;;
                    6)
                        select_del=$(dialog --clear \
                        --backtitle "ServerBot ${VERSION}" \
                        --title "Remove ServerBot.service" \
                        --menu "Are you sure? This will disable service and delete entry." \
                        18 52 8 \
                        "${OPTIONS_YN[@]}" \
                        2>&1 >/dev/tty)
                    
                        clear

                        case $select_del in
                                1)
                                    sudo systemctl stop ServerBot
                                    sudo systemctl disable ServerBot
                                    sudo rm /etc/systemd/system/ServerBot.service
                                    ;;
                                2)
                                    bash setup.sh
                                    ;;
                        esac
                        ;;
                    7)
                        bash setup.sh
                        ;;
            esac
            ;;
        9)
            select_other=$(dialog --clear \
            --backtitle "ServerBot ${VERSION}" \
            --title "ServerBot Setup" \
            --menu "Select Operation:" \
            18 52 8 \
            "${OPTIONS_other[@]}" \
            2>&1 >/dev/tty)

            clear
            
            case $select_other in
                    1)
                        nano .env
                        bash setup.sh
                        ;;
                    2)
                        echo "Install ServerBot from Github..."
                        echo "This option is useful when you want to update Bot or fix/rebuild critical files."
                        echo "As default, this option will install ServerBot ${UPDATEVER} in a new directory."
                        echo "You can change it for other release."
                        echo "Installer uses git command. Make sure you have downloaded it."
                        read -p "Type anything to continue."
                        cd ..
                        git clone -b ${VERSION} https://github.com/kamile320/ServerBot SB_Update
                        ;;
                    3)
                        clear
                        echo "To see manual, open 'manualEN.html' / 'manualPL.html' or visit https://kamile320.github.io/serverbot/manualEN.html"
                        read -p "Type anything to continue."
                        bash setup.sh
                        ;;
                    4)
                        bash setup.sh
                        ;;
            esac
            ;;
esac
