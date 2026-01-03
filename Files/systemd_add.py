import os
accept_value = ['Y', 'y', 'Yes', 'yes', 'YES']


def create_service(maindir, name):
    print(f'Creating {name}.service in /etc/systemd/system..')
    try:
        sys = open(f'/etc/systemd/system/{name}.service', 'w')
        sys.write(f"[Unit]\nDescription={name} autorun service\n\n[Service]\nExecStart={maindir}/autorun/autorun.sh\n\n[Install]\nWantedBy=multi-user.target")
        sys.close()
        print("Done!")
    except Exception as err:
        print(f'Error occurred: {err}')
        exit()


def default(maindir, filename):
    print("Making autorun.sh file..")
    os.chdir(maindir)
    try:
        if os.path.exists(f'{maindir}/autorun') == False:
            os.makedirs(f'{maindir}/autorun')
            os.chmod(f'{maindir}/autorun', 0o775)
        auto = open('autorun/autorun.sh', 'w')
        auto.write(f"#!/bin/bash\ncd {maindir}\npython3 {filename}.py")
        auto.close()
        os.chmod(f'{maindir}/autorun/autorun.sh', 0o775)
        print('Done.')
    except Exception as err:
        print(f"Can't create file!\nException: {err}")
        exit()


def venv(maindir, filename, venv):
    print('Making autorun.sh file..')
    os.chdir(maindir)
    try:
        if os.path.exists(f'{maindir}/autorun') == False:
            os.makedirs(f'{maindir}/autorun')
            os.chmod(f'{maindir}/autorun', 0o775)
        auto = open('autorun/autorun.sh', 'w')
        auto.write(f'#!/bin/bash\ncd {maindir}\n{venv}/bin/python3 {filename}.py')
        auto.close()
        os.chmod(f'{maindir}/autorun/autorun.sh', 0o775)
        print('Done.')
    except Exception as err:
        print(f"Can't create file!\nException: {err}")
        exit()


mdir = os.getcwd()


print("""
S Y S T E M D   A D D E R  v1.2  #
##################################

This script will add your python script to system startup (autostart) using systemd.
You should run this script as root in your main directory.
""")
print(f'Detected current dir: {mdir}')
print(f"""If this directory:
- is your main directory of your python script you want to add to systemd
- includes python3 virtual environment directory (If you need it)
- can be changed by chmod to 775 permissions
      
We can start. If not, You should change it to proper directory.\n""")
check = input("Do you want to start? [Y/N]: ")
if check in accept_value:

    print(f"Selected Main Directory: {mdir}")

    file_name = input("Enter your file name (without '.py'): ")
    systemd_name = input("Enter name for systemd service (without '.service'): ")
    isvenv = input("Do you use venv? [Y/N]: ")
    if isvenv in accept_value:
        venv_name = input('Enter Python3 venv directory name: ')
    else:
        print("python3 venv: False")
        venv_name = 'None'

    print('\nOK.')
    print("Script will create files by following informations:")
    print(f"Python script name: {file_name}.py")
    print(f"Service name: {systemd_name}")
    print(f"autorun.sh location: {mdir}/autorun/autorun.sh")
    print(f"systemd entry location: /etc/systemd/system/{systemd_name}.service")
    if venv_name != 'None':
        print(f"Python3 virtual environment (venv) name: {venv_name}")
        print(f"Venv location: {mdir}/{venv_name}")
    print(f"Main Directory: {mdir}\n")

    check2 = input("Are you ready to start? [Y/N]: ")
    if check2 in accept_value:
        try:
            if venv_name != 'None':
                venv(mdir, file_name, venv_name)
            elif venv_name == 'None':
                default(mdir, file_name)
        except Exception as err:
            print(f"Error occurred while creating autorun.sh\nPossible cause: {err}")

        try:
            create_service(mdir, systemd_name)
            print(f"Run post installation commands to enable {systemd_name}.service to start with system startup:\nsudo chmod 775 -R {mdir}/* <- If it's not executable\nsudo systemctl enable {systemd_name} <- Enables automatic startup\nsudo systemctl start {systemd_name} <- Optional (turns on service)\nsudo systemctl daemon-reload <- if you're running this command second time\nREMEMBER about Reading/Executing permissions for others If something will not work!")
        except Exception as err:
            print(f"Error occurred while creating systemd service entry\nPossible cause: {err}")
    else:
        print('Aborting...')
        exit()
else:
    print('User canceled. Aborting...')
    exit()
