import subprocess

def os_selector():
    print("Select Operating System: ")
    print("1 - Linux")
    print("2 - Windows")
    sel = int(input(">>> "))
    if sel == 1:
        subprocess.run(["bash", 'setup.sh'])
    elif sel == 2:
        subprocess.run(['setup.bat'], shell=True)
    else:
        print('Failed to run Script. Aborting Install')

try:
    import discord
    from discord.ext import commands
    from discord import FFmpegPCMAudio
    from discord import *
    import datetime
    import psutil
    import os
    import requests
    import asyncio
    import random
    import shutil
    import openai
    import pyfiglet
    import platform
    import yt_dlp as youtube_dl
    from dotenv import load_dotenv
except:
    print("Error in importing Library's. Trying to install it and update pip3")
    os_selector()


#Baner
baner = pyfiglet.figlet_format("ServerBot")
print(baner)
bluescreenface = pyfiglet.figlet_format(": (")
#YT_DLP
yt_dl_opts = {'format': 'bestaudio/best'}
ytdl = youtube_dl.YoutubeDL(yt_dl_opts)
ffmpeg_options = {'options': "-vn -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 2"}
#Intents
intents = discord.Intents.default()
intents.message_content = True
status = ['Windows 98 SE', 'DSaF:DLI', 'Minesweeper', f'{platform.system()} {platform.release()}', 'system32', 'Fallout 2', 'Windows Vista', 'MS-DOS', 'Team Fortress 2', 'Discord Moderator Simulator', 'Arch Linux']
choice = random.choice(status)
ver = "1.4"
client = commands.Bot(command_prefix='.', intents=intents, activity=discord.Game(name=choice))


try:
    load_dotenv()
    ####### token/intents/etc ##########
    openai.api_key = os.getenv('OpenAI')
    admin_usr = os.getenv('admin_usr')
    ####################################
except:
    print("CAN'T LOAD .env FILE!\nCreate file named '.env' with content:\nTOKEN=''\nOpenAI=''\nadmin_usr=['','']")


#Log_File
logs = open('Logs.txt', 'w')
def createlogs():
    logs.write(f"""S E R V E R  B O T
LOGS
Time: {datetime.datetime.now()}
Info: Remember to shut down bot by .ShutDown command or log will be empty.
=============================================================================\n\n""")
    logs.close()
createlogs()


#Directory
maindir = os.getcwd()
SBbytes = os.path.getsize('ServerBot.py')


#Information/Errors
fileerror = "Error: File not found or don't exist"
filelarge = "Error: File too large"
copiedlog = f"Information[ServerLog]: Copied Log to {maindir}/Files"
ffmpeg_error = "FFmpeg is not installed or File not found"
voice_not_connected_error = "You must be connected to VC first!"
leave_error = "How can I left, when I'm not in VC?"
thread_error = "Something Happened. Try to type:\n.thread {NameWithoutSpaces} {Reason}\nIf no reason, type: None"
not_allowed = "You're not allowed to use this command."
SBservice = "Run post installation commands to enable ServerBot.service to start with system startup:\nsudo chmod 777 -R /BotDirectory/*\nsudo systemctl enable ServerBot <== Enables automatic startup\nsudo systemctl start ServerBot <== Optional (turns on Service)\nsudo systemctl daemon-reload <== if you're running this command second time\nREMEBER about Reading/Executing permissions for others!"
sctlerr = "Something went wrong.\n'sctl' directory with service entries exists?"
sctlmade = "Created 'sctl' directory for systemctl service entry."

#ClientEvent
@client.event
async def on_ready():
    print(f'Logged as {client.user}')
    print(f'Welcome in ServerBot Version {ver}')
    #slash_command_sync
    try:
        syncd = await client.tree.sync()
        print(f'Synced {len(syncd)} slash command(s)')
    except:
        print("Can't sync slash commands")
    print('Bot runtime: ', datetime.datetime.now())
    print('=' *40)


        #ChatBot
#Chat
#1
@client.command()
async def hello(ctx):
    await ctx.send(f'Hello, {ctx.author.mention}!')

#2
@client.command()
async def bye(ctx):
    await ctx.send(f'See you later, {ctx.author.mention}!')

#3
@client.command()
async def hi(ctx):
    await ctx.send(f'hi!')

#4
@client.command()
async def hello_there(ctx):
    await ctx.send(f'OH, HELLO THERE!')
        #Chat-END



        #Random/Fun
#1
@client.command(name='random', help='Shows your random number.\nType .random [min] [max]')
async def random_num(ctx, min = int(), max = int()):
    import random
    try:
        randomn = random.randrange(min, max)
        await ctx.reply(f'This is your random number: {randomn}')
    except:
        await ctx.reply(f'Something went wrong. Did you typed correct min/max values?')

#2
@client.command(name='essa', help='Check your "essa"')
async def essa(ctx):
    import random
    losessa = random.randrange(101)
    await ctx.send(f'Twój dzisiejszy poziom essy: {losessa}%')
    print(f'Information[Random/Fun]: Someone has {losessa}% of essa')
    logs = open(f'{maindir}/Logs.txt', 'a')
    logs.write(f'Information[Random/Fun]: Someone has {losessa}% of essa\n')
    logs.close()

#3
@client.command(name='botbanner', help='Shows Bots Banner')
async def banner(ctx):
    await ctx.send(f'```{baner}```')

#4
@client.command(name='banner', help='Shows your text as Banner')
async def banner(ctx, *, text):
    banerr = pyfiglet.figlet_format(text)
    await ctx.send(f'```{banerr}```')

#5
@client.command(name='blankthing', help='Just blank thing')
async def blank(ctx):
    await ctx.send('ㅤ')

#6
@client.command(name='apple', help='Test for be an Apple')
async def blank(ctx):
    await ctx.send('')

#7
@client.command(name='gpt', help='Talk with ChatGPT.\nUses GPT 3.5 turbo by OpenAI')
async def gpt(ctx, *, question):
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": question}]
        )
        reply_content = completion.choices[0].message.content
        await ctx.reply(reply_content)
    except Exception as error:
        await ctx.reply("""Something went wrong, possible causes:
1. Bad Token - contact with admin to type new one
2. Too long response for Discord
3. Good Token but expired/not working""")
        await ctx.send(f"Exception:\n{error}")
        print(error)
        
#8
@client.command(name='GNU+Linux', help='Richard Stallman.')
async def gnu(ctx):
    await ctx.send("I’d just like to interject for a moment. What you’re refering to as Linux, is in fact, GNU/Linux, or as I’ve recently taken to calling it, GNU plus Linux. Linux is not an operating system unto itself, but rather another free component of a fully functioning GNU system made useful by the GNU corelibs, shell utilities and vital system components comprising a full OS as defined by POSIX.  Many computer users run a modified version of the GNU system every day, without realizing it. Through a peculiar turn of events, the version of GNU which is widely used today is often called Linux, and many of its users are not aware that it is basically the GNU system, developed by the GNU Project.  There really is a Linux, and these people are using it, but it is just a part of the system they use. Linux is the kernel: the program in the system that allocates the machine’s resources to the other programs that you run. The kernel is an essential part of an operating system, but useless by itself; it can only function in the context of a complete operating system. Linux is normally used in combination with the GNU operating system: the whole system is basically GNU with Linux added, or GNU/Linux. All the so-called Linux distributions are really distributions of GNU/Linux!")

#9
@client.command(name='badge')
async def badge(ctx, member: discord.Member):
    user_flags = member.public_flags.all()
    badges = [flag.name for flag in user_flags]
    await ctx.send(f'{member} has the following badges: {", ".join(badges)}')
        #Random/Fun-END



        #BotInfo
#1
@client.command(name='manual', help='Sends HTML manual ')
async def manual(ctx):
    try:
        await ctx.send(file=discord.File(f'{maindir}/manual.html'))
    except:
        await ctx.send(f"Can't open manual.html")

#2
@client.command(name='credits', help='Shows Credits')
async def credits(ctx):
    await ctx.send(f"""
***S e r v e r  B o t***
Version: {ver}
Created By: *Kamile320*.

Thanks to:
- friends for testing Bot
- <@632682413776175107> for some retranslations

Source: ```https://github.com/kamile320/ServerBot```
Used Sounds:
    WinXP/98 sounds -> files from OG OS by Microsoft
    Omegatronic Bot Micspam: ```https://www.youtube.com/watch?v=BNJxlSpBR5A```
    TF2 upgrade station: ```https://youtube.com/watch?v=Q7eJg7hRvqE```
""")

#3
@client.command(name='time', help='Shows local time')
async def time(ctx):
    now = datetime.datetime.now()
    await ctx.send(now.strftime('%d.%m.%Y, %H:%M:%S'))

#4
@client.command(name='ping', help='Pings the Bot')
async def ping(ctx):
    await ctx.send(f':tennis: Pong! ({round(client.latency * 1000)}ms)')
        
#5
@client.command(name='newest_update', help='Shows last changes of Bot functions/Changelog')
async def newest_update(ctx):
    await ctx.send(f"""
[ServerBot Ver. {ver}]
    Changelog:
- updated .random command and more
- /random still in old version
- code improvements
- added .ytplay command

To see older releases, find 'updates.txt' in folder 'Files' 
""")

#6
@client.command(name='next_update', help='Shows future functions/updates')
async def next_update(ctx):
    await ctx.send("""
next update
[N/A]
""")
    
#7
@client.command(name='issues', help='Known Issues of Bot')
async def issues(ctx):
    await ctx.send("""
**Known Issues:**
**1.** '.unban' command doesn't work.
    **Why:** Can't find banned user
    **How Fixed:** Waits for fix.""")
        #BotInfo-END



        #AdminOnly
#1
@client.command(name='ShutDown', help='Turns Off the Bot')
async def ShutDown(ctx):
    if str(ctx.message.author.id) in admin_usr:
        print("Information[ShutDown]: Started turning off the Bot")
        try:
            print("Information[ShutDown]: Saving Logs.txt...")
            src = open(f'{maindir}/Logs.txt', 'r')
            logs = open(f'{maindir}/Files/Logs.txt', 'a')
            append = f"\n\n{src.read()}"
            logs.write(append)
            logs.close()
            src.close()
            print("Logs.txt saved successfully.")
        except:
            print("Error occurred while saving log.")
        print("Information[ShutDown]: Shutting Down...")
        await ctx.send(f'ClosingBot.')
        await asyncio.sleep(1)
        await ctx.send(f'ClosingBot..')
        await asyncio.sleep(1)
        await ctx.send(f'ClosingBot...')
        await asyncio.sleep(1)
        exit()
    else:
        await ctx.reply(not_allowed)

#2
@client.command(name='copylog', help='Copies Bot Log file\nappend -> adds new value to older in Files/Logs.txt\nreplace -> clears old Files/Logs.txt and adds new content\nclearall -> clears all Logs')
async def copylog(ctx, mode):
    if str(ctx.message.author.id) in admin_usr:
        if mode == 'append':
            try:
                src = open(f'{maindir}/Logs.txt', 'r')
                logs = open(f'{maindir}/Files/Logs.txt', 'a')
                append = f"\n\n{src.read()}"
                logs.write(append)
                logs.close()
                src.close()
                await ctx.send('Appending logs to Files/Logs.txt succeed.')
            except:
                await ctx.send(f"Error occurred while copying log.")
        elif mode == 'replace':
            try:
                src_path = fr"{maindir}/Logs.txt"
                dst_path = fr"{maindir}/Files/Logs.txt"
                shutil.copy(src_path, dst_path)
                print(copiedlog)
                await ctx.send(f'Successfully replaced Files/Logs.txt content.')
            except:
                await ctx.send("Error occurred while copying log. Maybe folder doesn't exist?")
        elif mode == 'clearall':
            try:
                l1 = open(f"{maindir}/Logs.txt", 'w')
                l1.write("")
                l1.close()
                l2 = open(f"{maindir}/Files/Logs.txt", 'w')
                l2.write("")
                l2.close()
                await ctx.send("Successfully cleared Logs.")
            except:
                await ctx.send("Can't clear logs.")
        else:
            await ctx.send("Wrong copylog mode.")        
    else:
        await ctx.reply(not_allowed)

#3
@client.command(name='kick', help='Kicks Members')
async def kick(ctx, member: discord.Member, *, reason=None):
    kicked = f'Information[Server/Members]: Kicked {member}. Reason: {reason}\n'
    if str(ctx.message.author.id) in admin_usr:
        await member.kick(reason=reason)
        await ctx.send(f'Kicked **{member}**')
        print(kicked)
        logs = open(f'{maindir}/Logs.txt', 'a')
        logs.write(kicked)
        logs.close()
    else:
        await ctx.reply(not_allowed)

#4
@client.command(name='ban', help='Bans Members')
async def ban(ctx, member: discord.Member, *, reason=None):
    banned = f'Information[Server/Members]: Banned {member}. Reason: {reason}\n'
    if str(ctx.message.author.id) in admin_usr:
        await member.ban(reason=reason)
        await ctx.send(f'Banned **{member}**')
        print(banned)
        logs = open(f'{maindir}/Logs.txt', 'a')
        logs.write(banned)
        logs.close()
    else:
        await ctx.reply(not_allowed)

#5
@client.command(name='unban', help='Unbans Members')
async def unban(ctx, member: discord.Member, *, reason=None):
    unbanned = f'Information[Server/Members]: Unbanned {member}. Reason: {reason}\n'
    if str(ctx.message.author.id) in admin_usr:
        await member.unban(reason=reason)
        await ctx.send(f'Unbanned **{member}**')
        print(unbanned)
        logs = open(f'{maindir}/Logs.txt', 'a')
        logs.write(unbanned)
        logs.close()
    else:
        await ctx.reply(not_allowed)

#6
@client.command(name="bash", help="Runs Bash like scripts on hosting computer (Linux only)\nUses .sh extensions\nBest to work with .touch command")
async def bash(ctx, file):
    if str(ctx.message.author.id) in admin_usr:
        try:
            subprocess.run(["bash", file])
        except:
            await ctx.send(f'Failed to run Script')
    else:
        await ctx.reply(not_allowed)

#7
@client.command(name='rebuild', help='Rebuilds files and directories')
async def rebuild(ctx):
    if str(ctx.message.author.id) in admin_usr:
        await ctx.send('Trying to rebuild files...')
        try:
            os.chdir(maindir)
            logs1 = open('Logs.txt', 'w')
            logs1.close()

            os.makedirs(f'{maindir}/Files')
            os.chdir(f'{maindir}/Files')
            updates = open('updates.txt', 'w')
            updates.close()
            logs2 = open('Logs.txt', 'w')
            logs2.close()
            
            os.makedirs(f'{maindir}/setup')
            os.chdir(maindir)
            await ctx.send("Success.\nRebuilded Files with no content")
        except:
            await ctx.send("Can't rebuild files.")
    else:
        await ctx.reply(not_allowed)

#8
@client.command(name="mkshortcut", help="Creates a shortcut on your Desktop. (Linux (Ubuntu 22.04 based) only)\nType: .mkshortcut [Name of your Desktop Folder (Desktop/Pulpit etc.)]")
async def shrtct(ctx, desk):
    if str(ctx.message.author.id) in admin_usr:
        try:
            home_dir = os.path.expanduser('~')
            os.chdir(home_dir)
            os.chdir(desk)
            shrt = open('ServerBot.sh', 'w')
            shrt.write(f'cd {maindir}\npython3 ServerBot.py')
            shrt.close()
            os.chdir(maindir)
            await ctx.send('Done.')
            
            print(f"Information: Created desktop shortcut ({home_dir})")
            logs = open(f'{maindir}/Logs.txt', 'a')
            logs.write(f"Information: Created desktop shortcut ({home_dir})\n")
            logs.close()
        except:
            await ctx.send('Something went wrong, please try again.')
    else:
        await ctx.send(not_allowed)

#9
@client.command(name="disks", help="Shows mounted disks with free disk space")
async def disk(ctx):
    if str(ctx.message.author.id) in admin_usr:
        try:
            await ctx.send(f"```{subprocess.getoutput(['df -h'])}```")
        except:
            await ctx.send('Something went wrong\nDo you use Linux?')
    else:
        await ctx.send(not_allowed)

#10
@client.command(name="mksysctlstart", help="Adds ServerBot to systemctl to start with system startup (Bot needs to be running as root)\nMode:\n'none' -> creates default autorun entry (python3)\n'your entry' -> you need enter pwd of your python virtual environment (eg. .venv/bin/python)\n.venv file in this example hides in ServerBot main directory)\nIt's recommended to save bot files into main (root) directory (/ServerBot) with full permissions (chmod 777 recursive). Without full permissions to bot files systemctl startup will not work.")
async def mksysctlstart(ctx, mode):
    if str(ctx.message.author.id) in admin_usr:
        try:
            if mode == 'none':
                try:
                    await ctx.send("Making autorun.sh file..")
                    try:
                        auto = open('Files/autorun.sh', 'w')
                        auto.write(f"#!/bin/bash\ncd {maindir}\npython3 ServerBot.py")
                        auto.close()
                        await ctx.send('Done.')

                        print(f"Information: Created autorun.sh file (Files/autorun.sh)")
                        logs = open(f'{maindir}/Logs.txt', 'a')
                        logs.write(f"Information: Created autorun.sh file (Files/autorun.sh)\n")
                        logs.close()
                    except:
                        await ctx.send("Can't create file!")

                    await ctx.send('Making ServerBot.service in /etc/systemd/system..')
                    try:
                        sys = open('/etc/systemd/system/ServerBot.service', 'w')
                        sys.write(f"[Unit]\nDescription=ServerBot autorun service\n\n[Service]\nExecStart={maindir}/Files/autorun.sh\n\n[Install]\nWantedBy=multi-user.target")
                        await ctx.send("Done!")
                        await ctx.send(SBservice)

                        print(f"Information: Created ServerBot service file (/etc/systemd/system/)\n{SBservice}")
                        logs = open(f'{maindir}/Logs.txt', 'a')
                        logs.write(f"Information: Created ServerBot service file (/etc/systemd/system/)\n{SBservice}\n")
                        logs.close()
                    except:
                        await ctx.send("Can't create service file!\nAre you root?")
                except:
                    await ctx.send('Got 1 error (or more) while creating systemctl entry.')
            else:
                try:
                    await ctx.send('Making autorun.sh file..')
                    try:
                        auto = open('Files/autorun.sh', 'w')
                        auto.write(f'#!/bin/bash\ncd {maindir}\n{mode} ServerBot.py')
                        auto.close()
                        await ctx.send('Done.')

                        print(f"Information: Created autorun.sh file (Files/autorun.sh)")
                        logs = open(f'{maindir}/Logs.txt', 'a')
                        logs.write(f"Information: Created autorun.sh file (Files/autorun.sh)\n")
                        logs.close()
                    except:
                        await ctx.send("Can't create file!")

                    await ctx.send('Making ServerBot.service in /etc/systemd/system..')
                    try:
                        sys = open('/etc/systemd/system/ServerBot.service', 'w')
                        sys.write(f"[Unit]\nDescription=ServerBot autorun service\n\n[Service]\nExecStart={maindir}/Files/autorun.sh\n\n[Install]\nWantedBy=multi-user.target")
                        await ctx.send("Done!")
                        await ctx.send(SBservice)
                    
                        print(f"Information: Created ServerBot service file (/etc/systemd/system/)\n{SBservice}")
                        logs = open(f'{maindir}/Logs.txt', 'a')
                        logs.write(f"Information: Created ServerBot service file (/etc/systemd/system/)\n{SBservice}\n")
                        logs.close()
                    except:
                        await ctx.send("Can't create service file!\nAre you root?")
                except:
                    await ctx.send('Got 1 error (or more) while creating systemctl entry.')
        except:
            await ctx.send(f"""```{bluescreenface}``` Unexpected problem ocurred""")
    else:
        await ctx.send(not_allowed)

#11
@client.command(name='service', help="Lists active/inactive services. To add service entry, create empty file in directory 'sctl'\nUses systemctl\n\nlist -> lists created entries in 'sctl' directory\nstatus -> lists service entries and checks if they're active\nprepare -> creates 'sctl' directory for service entries")
async def service(ctx, mode):
    if str(ctx.message.author.id) in admin_usr:
        try:
            if mode == 'list':
                try:
                    listdir = os.listdir(f"{maindir}/sctl")
                    await ctx.send(f'Service Entries:')
                    for file in listdir:
                        await ctx.send(file)
                except:
                    await ctx.send(sctlerr)
            elif mode == 'status':
                try:
                    await ctx.send("**Service Activity:**")
                    listdir = os.listdir(f"{maindir}/sctl")
                    for file in listdir:
                        await ctx.send(f"```{file}: {subprocess.getoutput([f'systemctl is-active {file}'])}```")
                except:
                    await ctx.send(sctlerr)
            elif mode == 'status-detailed':
                try:
                    await ctx.send("**Service Activity:**")
                    listdir = os.listdir(f"{maindir}/sctl")
                    for file in listdir:
                        await ctx.send(f"```{file}: {subprocess.getoutput([f'systemctl status {file}'])}```")
                except:
                    await ctx.send(sctlerr)
            elif mode == 'prepare':
                try:
                    os.makedirs('sctl')
                    await ctx.send(f"{sctlmade}\nCreate empty files named as systemctl services in this directory to see if they're active/inactive.")
                
                    print(f"Information[Files/Directories]: {sctlmade}\n")
                    logs = open(f'{maindir}/Logs.txt', 'a')
                    logs.write(f"Information[Files/Directories]: {sctlmade}\n")
                    logs.close()
                except:
                    await ctx.send("Can't create directory.")
            else:
                await ctx.send("Incorrect mode.")
        except:
            await ctx.send('Something went wrong.')
    else:
        await ctx.send(not_allowed)
        #AdminOnly-END



        #Utility_and_Diagnostics
#1
@client.command(name='testbot', help='Tests some functions of Host and Bot')
async def testbot(ctx):
    teraz = datetime.datetime.now()
    await ctx.send(f"""
***S e r v e r  B o t***  *test*:
====================================================
Time: **{teraz.strftime('%d.%m.%Y, %H:%M:%S')}**
Bot name: **{client.user}**
Version: **{ver}**
CPU Usage: **{psutil.cpu_percent()}** (%)
CPU Count: **{psutil.cpu_count()}**
CPU Type: **{platform.processor()}ㅤ**
RAM Usage: **{psutil.virtual_memory().percent}** (%)
Ping: **{round(client.latency * 1000)}ms**
OS Test (Windows): **{psutil.WINDOWS}**
OS Test (MacOS): **{psutil.MACOS}**
OS Test (Linux): **{psutil.LINUX}**
OS Version: **{platform.version()}**
OS Kernel: **{platform.system()} {platform.release()}**
Bot Current Dir: **{os.getcwd()}**
Bot Main Dir: **{maindir}**
File size: **{os.path.getsize(f'{maindir}/ServerBot.py')}**
Floppy: **{os.path.exists('/dev/fd0')}**
====================================================""")

#2
@client.command(name='testos', help='Check OS of server with running bot. \n .testos <os name> \n eg. .testos linux/windows/macos')
async def testos(ctx, operatingsys):
    if operatingsys == 'linux':
        await ctx.send(f'Linux: {psutil.LINUX}')
    elif operatingsys == 'windows':
        await ctx.send(f'Windows: {psutil.WINDOWS}')
    elif operatingsys == 'macos':
        await ctx.send(f'MacOS: {psutil.MACOS}')
    else:
        await ctx.send(f'Please enter windows/linux/macos')

#3
@client.command(name='bytes', help='Shows size of main code')
async def bytes(ctx):
    await ctx.send(f'{SBbytes} bytes of code!')

#4
@client.command(name='delete', help='Deletes set amount of messages (eg. .delete 6 => will delete 6 messages)')
async def delete(ctx, amount: int = 0):
    deleted = await ctx.channel.purge(limit=amount)
    await ctx.channel.send(f'Deleted {len(deleted)} message(s)')
    print(f"Information: Deleted {len(deleted)} messages using '.delete' on channel: {ctx.channel.name}")
    logs = open(f'{maindir}/Logs.txt', 'a')
    logs.write(f"Information: Deleted {len(deleted)} messages using '.delete' on channel: {ctx.channel.name}\n")
    logs.close()

#5
@client.command(name='cleaner', help='Cleans channel from last 100 messages')
async def cleaner(ctx):
    deleted = await ctx.channel.purge(limit=100)
    await ctx.channel.send(f'[Cleaner] deleted max amount of messages ({len(deleted)})')
    print(f"Information: Deleted {len(deleted)} messages using '.cleaner' on channel: {ctx.channel.name}")
    logs = open(f'{maindir}/Logs.txt', 'a')
    logs.write(f"Information: Deleted {len(deleted)} messages using '.cleaner' on channel: {ctx.channel.name}\n")
    logs.close()

#6
@client.command(name='binary', help='Converts decimal number to binary. \n .binary <dec number>; eg. binary 2019')
async def binary(ctx, number):
    binn = bin(int(number))
    await ctx.send(f'{number} in binary: {binn}')
    print(f'Information[Command]: Converted {number} to {binn} using .binary')
    logs = open(f'{maindir}/Logs.txt', 'a')
    logs.write(f'Information[Command]: Converted {number} to {binn} using .binary\n')
    logs.close()

#7
@client.command(name='hexa', help="Converts decimal number to hexadecimal. \n .hexa <dec number>; eg. hexa 2007")
async def hexadecimal(ctx, number):
    hexa = hex(int(number))
    await ctx.send(f'{number} in hexadecimal: {hexa}')
    print(f'Information[Command]: Converted {number} to {hexa} using .hexa')
    logs = open(f'{maindir}/Logs.txt', 'a')
    logs.write(f'Information[Command]: Converted {number} to {hexa} using .hexa\n')
    logs.close()

#8
@client.command(name='convert', help='Advanced Converter v1.0\n========================\n\nConverts one number to other number systems - binary, octal, decimal, hexa (hexadecimal)')
async def multiconv(ctx, type, number):
    try:
        if type == 'decimal':
            number = int(number)
            hexa = hex(number)
            octa = oct(number)
            bina = bin(number)
            try:
                await ctx.send(f'Conversion of {number} ({type}):\nHexadecimal: {hexa}\nDecimal: {number}\nOctal: {octa}\nBinary: {bina}')
            except:
                await ctx.send(f'Unexpected Error\nPlease try again')
        elif type == 'octal':
            deci = int(number, base=8)
            bina1 = int(number, base=8)
            bina2 = bin(bina1)
            hexa1 = int(number, base=8)
            hexa2 = hex(hexa1)
            try:
                await ctx.send(f'Conversion of {number} ({type}):\nHexadecimal: {hexa2}\nDecimal: {deci}\nOctal: {number}\nBinary: {bina2}')
            except:
                await ctx.send(f'Unexpected Error\nPlease try again')
        elif type == 'binary':
            deci = int(number, base=2)
            octa1 = int(number, base=2)
            octa2 = oct(octa1)
            hexa1 = int(number, base=2)
            hexa2 = hex(hexa1)
            try:
                await ctx.send(f'Conversion of {number} ({type}):\nHexadecimal: {hexa2}\nDecimal: {deci}\nOctal: {octa2}\nBinary: {number}')
            except:
                await ctx.send(f'Unexpected Error\nPlease try again')
        elif type == 'hexa':
            deci = int(number, base=16)
            octa1 = int(number, base=16)
            octa2 = oct(octa1)
            bina1 = int(number, base=16)
            bina2 = bin(bina1)
            try:
                await ctx.send(f'Conversion of {number} ({type}):\nHexadecimal: {number}\nDecimal: {deci}\nOctal: {octa2}\nBinary: {bina2}')
            except:
                await ctx.send(f'Unexpected Error\nPlease try again')
        else:
            await ctx.send("Wrong value.\nType: .convert binary/octal/decimal/hexa and value for selected number system")
    except:
        await ctx.send(f'```{bluescreenface}\nUnexpected error occurred```')

#9
@client.command(name="thread", help="Makes server threads\n.thread {name} {reason}")
async def thread(ctx, name, *, reason):
    try:
        channel = ctx.channel
        thread = await channel.create_thread(name=name, auto_archive_duration=60, slowmode_delay=None, reason=reason)
        await ctx.send(f"Created new thread [{name}]")
        print(f"Information[Threads]: Created new thread [{name}] on {channel}. Reason: {reason}")
        logs = open(f'{maindir}/Logs.txt', 'a')
        logs.write(f"Information[Threads]: Created new thread [{name}] on {channel}. Reason: {reason}\n")
        logs.close()
    except:
        await ctx.send(thread_error)

#10
@client.command(name="webreq", help="Sends website request code")
async def webreq(ctx, *, web):
    try:
        rq = requests.get(web)
        await ctx.send(f"Response: {rq}")
    except:
        await ctx.send("Something went wrong.\nHave you typed the correct address?\n..Or maybe the website just doesn't exist? ")

#11
@client.command(name='pingip', help='Pings selected IPv4 address.')
async def pingip(ctx, ip):
    try:
        ipaddr = ip
        await ctx.send(f"```{subprocess.getoutput([f'ping {ipaddr} -c 1'])}```")
    except:
        await ctx.send('Something went wrong')
        #Utility_and_Diagnostics-END



        #VoiceChannel
#1 - connect
@client.command(pass_context=True, name='join', help='Join Voice Channel')
async def connect(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        source = FFmpegPCMAudio(f'{maindir}/Media/Windows XP - Autostart.wav')
        player = voice.play(source)
        await ctx.reply(f'Connected to {channel.name}')
        print(f'Information[VoiceChat]: Joined to {channel.name}')
        logs = open(f'{maindir}/Logs.txt', 'a')
        logs.write(f'Information[VoiceChat]: Joined to {channel.name}\n')
        logs.close()
    else:
        await ctx.reply(voice_not_connected_error)

#2 - disconnect
@client.command(pass_context=True, name='leave', help='Leave Voice Channel')
async def disconnect(ctx):
    if (ctx.voice_client):
        channel = ctx.message.author.voice.channel
        voice = ctx.guild.voice_client
        source = FFmpegPCMAudio(f'{maindir}/Media/Windows XP - Zamkniecie.wav')
        player = voice.play(source)
        await asyncio.sleep(3)
        await ctx.guild.voice_client.disconnect()
        await ctx.reply("Left from VC")
        print(f'Information[VoiceChat]: User forced bot to leave from: {channel.name}')
        logs = open(f'{maindir}/Logs.txt', 'a')
        logs.write(f'Information[VoiceChat]: User forced bot to leave from: {channel.name}\n')
        logs.close()
    else:
        await ctx.reply(leave_error)

#3 - play
@client.command(name='play', help="Play a local music file.\n.play {filename*}\n*With complete directory path when file isn't in maindir")
async def play(ctx, *, name):
    try:
        try:
            channel = ctx.message.author.voice.channel
            voice = await channel.connect()
            print(f'Information[VoiceChat]: Joined to {channel.name}')
            logs = open(f'{maindir}/Logs.txt', 'a')
            logs.write(f'Information[VoiceChat]: Joined to {channel.name}\n')
            logs.close()
        except:
            print(f"Information[VoiceChat]: Can't join to {channel.name}. Already joined?")
            logs = open(f'{maindir}/Logs.txt', 'a')
            logs.write(f"Information[VoiceChat]: Can't join to {channel.name}. Already joined?\n")
            logs.close()
        try:
            exist = os.path.exists(name)
            if exist == True:
                voice = ctx.guild.voice_client
                source = FFmpegPCMAudio(name)
                player = voice.play(source)
                await ctx.reply(f'Playing music...\nSource: {name}')
            else:
                await ctx.reply("Can't find source file.")
        except:
            await ctx.reply("Can't play music.\nSource exist?")
    except:
        await ctx.reply(voice_not_connected_error)

#4 - ytplay
@client.command(name='ytplay', help="Play music from YouTube URL\n.ytplay {URL}")
async def ytplay(ctx, *, url):
    try:
        try:
            channel = ctx.message.author.voice.channel
            voice = await channel.connect()
            print(f'Information[VoiceChat]: Joined to {channel.name}')
            logs = open(f'{maindir}/Logs.txt', 'a')
            logs.write(f'Information[VoiceChat]: Joined to {channel.name}\n')
            logs.close()
        except:
            print(f"Information[VoiceChat]: Can't join to {channel.name}. Already joined?")
            logs = open(f'{maindir}/Logs.txt', 'a')
            logs.write(f"Information[VoiceChat]: Can't join to {channel.name}. Already joined?\n")
            logs.close()
        try:
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
            song = data['url']
            voice = ctx.guild.voice_client
            player = discord.FFmpegPCMAudio(song, **ffmpeg_options)
            voice.play(player)
            await ctx.send(f'Playing from source: ```{url}```')
        except:
            await ctx.reply("Can't play music.\nSource exist?")
    except:
        await ctx.reply(voice_not_connected_error)

#5 - stop
@client.command(pass_context=True, name='stop', help='Stops playing audio')
async def stop(ctx):
    voice = ctx.guild.voice_client
    if voice.is_playing():
        voice.stop()
    else:
        await ctx.reply('Music is not playing right now')

#6
@client.command(pass_context = True, name='pause', help='Pause/Resume command')
async def pause(ctx):
    voice = ctx.guild.voice_client
    if voice.is_playing():
        voice.pause()
    elif voice.is_paused():
        voice.resume()
    else:
        await ctx.reply('Music is not playing on voice channel right now')

#7
@client.command(name='waiting', help="Say everyone that you're waiting!")
async def wait(ctx):
    try:
        voice = ctx.guild.voice_client
        source = FFmpegPCMAudio(f'{maindir}/Media/Team Fortress 2 Upgrade Station.ogg')
        player = voice.play(source)
        await ctx.send(f"@everyone, {ctx.author.mention} is waiting!")
    except AttributeError:
        await ctx.reply(voice_not_connected_error)
    except:
        await ctx.reply(ffmpeg_error)

#8
@client.command(name='micspam')
async def micspam(ctx):
    try:
        voice = ctx.guild.voice_client
        source = FFmpegPCMAudio(f'{maindir}/Media/OMEGATRONIC BOT MICSPAM.mp3')
        player = voice.play(source)
    except AttributeError:
        await ctx.reply(voice_not_connected_error)
    except:
        await ctx.reply(ffmpeg_error)
        #VoiceChannelEND



        #FileManager/Directory
#1
@client.command(name='cd', help="Changes directory\nYou can go back by .dir <return>")
async def chdir(ctx, *, directory):
    try:
        os.chdir(directory)
        await ctx.send(f"changed directory to {os.getcwd()}")
    except:
        await ctx.send("You can't go to this directory; make it or enter existing one")

#2
@client.command(name='dir', help='Directory commands \n.dir <mode> \n   mode: \nreturn -> Goes back to main dir\ncheck -> checks dir that you are in\nlist -> list of files and directories in your dir\nlistall -> same but easier to read')
async def dir(ctx, *, mode):
    if mode == 'return':#
        os.chdir(maindir)
        await ctx.send(f'Returned to main directory ({maindir})')

    elif mode == 'check':#
        await ctx.send(f'You are here: {os.getcwd()}')

    elif mode == 'list':#
        listdir = os.listdir()
        await ctx.send(f'Files in this directory:\n{listdir}')

    elif mode == 'listall':#
        listdir = os.listdir()
        await ctx.send(f'Files in this directory:')
        for file in listdir:
            await ctx.send(file)

#3      
@client.command(name='file', help='Commands for file/directory creating, deleting etc.\n.file <mode> <filename> \n    mode:\nopen -> opens file (REMEMBER to add extension (.py/.png/etc))\nmakedir -> creates directory (folder)\nchksize -> checks the size of selected file')
async def file(ctx, mode, *,filename):
    if mode == 'open':#
        try:
            await ctx.send(file=discord.File(filename))
        except:
            await ctx.send(fileerror)
    elif mode == 'mkdir':#
        try:
            os.makedirs(filename)
            await ctx.send("Created new directory. Use '.dir list' to check this")
        except:
            await ctx.send("Can't create directory.")
    elif mode == 'size':#
        try:
            size = os.path.getsize(filename)
            await ctx.send(f'Size of {filename} is {size} bytes')
        except:
            await ctx.send('Error')
    elif mode == 'create':#
        try:
            mkfile = open(filename, 'wt')
            mkfile.close()
            await ctx.send("Created new empty file. Use '.dir list' to check this")
        except:
            await ctx.send("Can't create file.")
    else:
        await ctx.send('Incorrect mode/filename')

#4
@client.command(name='touch', help='Creates files with selected extension and content.\nGo to selected directory and use .touch command')
async def makefile(ctx, name, *, content):
    try:
        directory = os.getcwd()
        mkfile = open(name, 'wt')
        mkfile.write(content)
        mkfile.close()

        created = f'Created file {name}, in directory {directory}.\nContent: {content}'
        await ctx.send(f'Created file {name}, in directory {directory}.')
        print(created)
        logs = open(f'{maindir}/Logs.txt', 'a')
        logs.write(f'Information[Files/Directories]: {created}\n')
        logs.close()
    except:
        await ctx.send(f'Something went wrong while creating file.')
        #FileManager/Directory-END


        #YouTubeLinks
@client.command(name='yt', help='Sends Link to YT\ntest1\ntest2')
async def yt(ctx, YTname):
    if YTname == 'test1':
        await ctx.send(f'test1')
    elif YTname == 'test2':
        await ctx.send(f'test2')
    else:
        await ctx.send("Wrong name")
        #YouTubeLinks-END



        #Links_and_Servers
#1
@client.command(name='mcservs', help='Shows Addresses to Minecraft Servers\nYou need to enter your own addresses')
async def mcservs(ctx):

    await ctx.send(f"""
```
====Minecraft Servers====
    <<Java Edition>>
Serv1
    -Ver:
    -Addresss:

Serv2
    -Ver:
    -Address:
                   
    <<Bedrock Edition>>
Serv3
    -Ver:
    -Address:
    -Port:
    -Link:
```""")
    
#2
@client.command(name='dscserv', help='Shows link to Discord Server')
async def dscserv(ctx):
    await ctx.send(f'https://discord.gg/UMtYGAx5ac')

#3
@client.command(name='addbot', help='Shows Link to add Bot to other Servers\nstable -> sends link to stable version\ntesting -> sends link to testing version')
async def addbot(ctx, version):
    if version == "stable":
        await ctx.reply("Enter your link here")
    elif version == "testing":
        await ctx.reply("Enter your link here")
    else:
        await ctx.send("Wrong value, try again.")
        #Links_and_Servers-END



        #FileSending
#1
@client.command(name='Teensie', help='TeensieGif')
async def Teensie(ctx):
    try:
        await ctx.send(file=discord.File(f'{maindir}/Files/Teensie.gif'))
    except:
        await ctx.send('https://media.discordapp.net/attachments/1099605026948780143/1099605179193622570/Teensien.gif')
        #FileSending-END



        #Test_Commands
#1
@client.command(name='test', help='test', tts=True)
async def test(ctx):
    await ctx.send(f'test {ctx.author.mention}')

#2
#@client.command(name='ServerKiller', help="Don't use this")
#async def kill(ctx):
#    while True:
#        await ctx.send('@everyone')
#
        #Test_Commands-END



################################################ S L A S H   C O M M A N D S ###########################################################################################
#1
@client.tree.command(name='random', description='Shows your random number')
async def random(interaction):
    import random
    randomn = random.randrange(-1, 999999)
    await interaction.response.send_message(f'This is your random number: {randomn}')

#2
@client.tree.command(name='ping', description='Pings the Bot')
async def ping(interaction):
    await interaction.response.send_message(f':tennis: Pong! ({round(client.latency * 1000)}ms)')

#3
@client.tree.command(name='testbot', description='Tests some functions of Bot')
async def testbot(interaction):
    teraz = datetime.datetime.now()
    await interaction.response.send_message(f"""
***S e r v e r  B o t***  *test*:
====================================================
Time: **{teraz.strftime('%d.%m.%Y, %H:%M:%S')}**
Bot name: **{client.user}**
Version: **{ver}**
CPU Usage: **{psutil.cpu_percent()}** (%)
CPU Count: **{psutil.cpu_count()}**
CPU Type: **{platform.processor()}ㅤ**
RAM Usage: **{psutil.virtual_memory().percent}** (%)
Ping: **{round(client.latency * 1000)}ms**
OS Test (Windows): **{psutil.WINDOWS}**
OS Test (MacOS): **{psutil.MACOS}**
OS Test (Linux): **{psutil.LINUX}**
OS Version: **{platform.version()}**
OS Kernel: **{platform.system()} {platform.release()}**
Bot Current Dir: **{os.getcwd()}**
Bot Main Dir: **{maindir}**
File size: **{os.path.getsize(f'{maindir}/ServerBot.py')}**
Floppy: **{os.path.exists('/dev/fd0')}**
====================================================""")
################################################ S L A S H   C O M M A N D S  - E N D #######################################################################################

try:
    client.run(os.getenv('TOKEN'))
except:
    print("Can't load Bot Token!\nEnter valid Token in '.env' file!")