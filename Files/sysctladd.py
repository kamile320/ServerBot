import os



def sysctl_service(maindir, name):
    print(f'Making {name}.service in /etc/systemd/system..')
    try:
        sys = open(f'/etc/systemd/system/{name}.service', 'w')
        sys.write(f"[Unit]\nDescription={name} autorun service\n\n[Service]\nExecStart={maindir}/sysctl/autorun.sh\n\n[Install]\nWantedBy=multi-user.target")
        sys.close()
        print("Done!")
    except Exception as err:
        print(f'Error occurred: {err}')


def default(maindir, filename):
    print("Making autorun.sh file..")
    os.chdir(maindir)
    try:
        if os.path.exists(f'{maindir}/sysctl') == False:
            os.makedirs(f'{maindir}/sysctl')

        auto = open('sysctl/autorun.sh', 'w')
        auto.write(f"#!/bin/bash\ncd {maindir}\npython3 {filename}.py")
        auto.close()
        print('Done.')
    except:
        print("Can't create file!")


def venv(maindir, filename, venv):
    print('Making autorun.sh file..')
    os.chdir(maindir)
    try:
        if os.path.exists(f'{maindir}/sysctl') == False:
            os.makedirs(f'{maindir}/sysctl')

        auto = open('sysctl/autorun.sh', 'w')
        auto.write(f'#!/bin/bash\ncd {maindir}\n{venv}/bin/python3 {filename}.py')
        auto.close()
        print('Done.')

    except:
        print("Can't create file!")


mdir = os.getcwd()


print("""
S Y S T E M C T L  A D D E R  v1.1  #
#####################################

This script will add your python script to system startup (autostart) via systemctl.
You should run this script as root in your main directory.
""")
print(f'Detected current dir: {mdir}')
print(f"""If this directory:
- is your main directory of your python script you want to add to systemctl
- includes python3 virtual environment directory (If you need it)
- can be changed by chmod to 775 permissions
      
We can start. If not, You should change it to proper directory.\n""")
check = input("Do you want to start? [Y/N]: ")
if check == 'Y':

    print(f"Selected Main Directory: {mdir}")

    file_name = input("Enter your file name (without '.py'): ")
    sctlname = input("Enter name for systemctl service: ")
    isvenv = input("Do you use venv? [Y/N]: ")
    if isvenv == 'Y' or isvenv == 'y':
        venv_name = input('Enter Python3 venv directory name: ')
    else:
        print("python3 venv: False")
        venv_name = 'None'

    print('\nOK.')
    print("Script will create files by following informations:")
    print(f"Python script name: {file_name}.py")
    print(f"systemctl name: {sctlname}")
    print(f"autorun.sh location: {mdir}/sctl/autorun.sh")
    print(f"systemctl entry location: /etc/systemd/system/{sctlname}.service")
    if venv_name != 'None':
        print(f"Python3 virtual environment (venv) name: {venv_name}")
        print(f"Venv location: {mdir}/{venv_name}")
    print(f"Main Directory: {mdir}\n")

    check2 = input("Are you ready to start? [Y/N]: ")
    if check2 == 'Y' or check2 == 'y':
        try:
            if venv_name != 'None':
                venv(mdir, file_name, venv_name)
            elif venv_name == 'None':
                default(mdir, file_name)
        except Exception as err:
            print(f"Error occurred while creating autorun.sh\nPossible cause: {err}")

        try:
            sysctl_service(mdir, sctlname)
            print(f"Run post installation commands to enable {sctlname}.service to start with system startup:\nsudo chmod 775 -R {mdir}/*\nsudo systemctl enable {sctlname} <== Enables automatic startup\nsudo systemctl start {sctlname} <== Optional (turns on Service)\nsudo systemctl daemon-reload <== if you're running this command second time\nREMEBER about Reading/Executing permissions for others!")
        except Exception as err:
            print(f"Error occurred while creating systemctl service entry\nPossible cause: {err}")
    else:
        print('Aborting...')
        exit()
else:
    print('User canceled. Aborting...')
    exit()
