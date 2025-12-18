import subprocess
import os
import sys

ver = "1.10.0-test"
displayname='ServerBot'
db_dir = 'Files/serverbot.db'

#ModuleVersion
ACLver = "3.1"


#Check flags
if '--help' in sys.argv:
    print(f"""ServerBot v{ver} made by Kamile320\n\n
          Project: https://github.com/kamile320/serverbot\n

          --help                Shows this message\n
          --ignore-pip          Doesn't abort bot startup if an error occur 
                                while loading pip libraries\n
          --version             Shows version information\n
    """)
    exit()

if '--version' in sys.argv:
    print(f"ServerBot v{ver}\nA.C.L. v{ACLver}")
    exit()


#Loading PIP Libraries
def os_selector():
    print(f"====ServerBot v{ver} Recovery Menu====")
    print("""Select Method: 
1 - Linux
2 - Windows
3 - Setup.sh
4 - Exit
""")
    sel = int(input('>>> '))
    if sel == 1:
        subprocess.run(['bash', 'Files/setup/setuplib.sh'])
    elif sel == 2:
        subprocess.run(['setup.bat'], shell=True)
    elif sel == 3:
        subprocess.run(['bash', 'setup.sh'])
    elif sel == 4:
        exit()
    else:
        print('Failed to run Script. Aborting Install...')
        exit()

try:
    import discord
    from discord.ext import commands
    from discord import FFmpegPCMAudio
    from discord import *
    import datetime
    import psutil
    import requests
    import asyncio
    import random
    import shutil
    import sqlite3
    import pyfiglet
    import platform
    import yt_dlp as youtube_dl
    from google import genai
    from google.genai import types
    from dotenv import load_dotenv
except Exception as exc:
    if '--ignore-pip' in sys.argv:
        print(f"Error while importing libraries: {exc}\nIgnoring.. Expect unstable experience.")
    else:
        print(f"Error while importing libraries. Trying to install it and update pip3\nException: {exc}\n")
        os_selector()
        exit()



#Baner
banner = pyfiglet.figlet_format(displayname)
bluescreenface = pyfiglet.figlet_format(": (")
print(banner)



#YT_DLP
yt_dl_opts = {"format": "bestaudio/best"}
ytdl = youtube_dl.YoutubeDL(yt_dl_opts)
ffmpeg_options = {"options": "-vn -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 2"}

#YT_DLP - search
ytdl_opts_search = {
    'default_search': 'ytsearch',
    'quiet': True,
    'extract_flat': True,
    'verbose': False, #True for debug
    'noplaylist': True,
    'format': 'bestaudio/best',
    'http_headers': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://www.youtube.com/'}}
ytdl_search = youtube_dl.YoutubeDL(ytdl_opts_search)



#Intents
intents = discord.Intents.default()
intents.message_content = True
status = ['Windows 98 SE', 'DSaF:DLI', 'Minesweeper', f'{platform.system()} {platform.release()}', 'system32', 'Fallout 2', 'Windows Vista', 'MS-DOS', 'Team Fortress 2', 'Discord Moderator Simulator', 'Arch Linux', f'ServerBot v{ver}', displayname]
choice = random.choice(status)
client = commands.Bot(command_prefix='.', intents=intents, activity=discord.Game(name=choice))
testbot_cpu_type = platform.processor() or 'Unknown'
accept_value = ['True', 'true', 'Enabled', 'enabled', '1', 'yes', 'Yes', 'YES', True]



try:
    load_dotenv()
    ############# token/intents/etc ################
    ai_token = os.getenv('AI_token')
    admin_usr = os.getenv('admin_usr')
        #To remove
    mod_usr = os.getenv('mod_usr')
    ai_model = f"{os.getenv('aimodel')}"
    ai_client = genai.Client(api_key=f"{ai_token}")
    extendedErrMess = os.getenv('extendedErrMess')
    ################################################
except:
    print("CAN'T LOAD .env FILE!\nCreate .env file using setup.sh")



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

#LogMessage
def logMessage(info):
    time = datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')
    logs = open(f'{maindir}/Logs.txt', 'a', encoding='utf-8')
    logs.write(f'[{time}] {info}\n')
    logs.close()
#PrintMessage
def printMessage(info):
    time = datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')
    print(f'[{time}] {info}')



#Directory
maindir = os.getcwd()
SBbytes = os.path.getsize('ServerBot.py')



#Database - create or load
def load_db():
    if os.path.exists(db_dir) == True:
        if extendedErrMess in accept_value:
            print("Database found.")
    else:
        print("Database not found. Creating new database...")
        db = sqlite3.connect(db_dir)
        cur = db.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS users(
                    id integer not null primary key AUTOINCREMENT, 
                    discord_id integer unique not null, 
                    username text, 
                    SBrole text default None, 
                    exp_points integer default 0, 
                    level integer default 0)""")
        db.commit()

#User registration
def register_user(id, name):
    db = sqlite3.connect('Files/serverbot.db')
    cur = db.cursor()
    #SELECT
    cur.execute('SELECT 1 FROM users WHERE discord_id=?', (id,))
    if cur.fetchone() is None:
        #INSERT
        cur.execute(f"INSERT INTO users (discord_id, username) VALUES (?, ?) ON CONFLICT(discord_id) DO NOTHING", (id, f"{name}"))
        db.commit()



#Information/Errors
fileerror = "Error: File not found or don't exist"
filelarge = "Error: File too large"
copiedlog = f"Information[ServerLog]: Copied Log to {maindir}/Files"
ffmpeg_error = "FFmpeg is not installed or File not found"
voice_not_connected_error = "You must be connected to VC first!"
leave_error = "How can I left, when I'm not in VC?"
thread_error = "Something Happened. Try to type:\n.thread {NameWithoutSpaces} {Reason}\nIf no reason, type: None"
not_allowed = "You're not allowed to use this command."
SBservice = "Run post installation commands to enable ServerBot.service to start with system startup:\nsudo chmod 775 -R /BotDirectory/*\nsudo systemctl enable ServerBot <== Enables automatic startup\nsudo systemctl start ServerBot <== Optional (turns on Service)\nsudo systemctl daemon-reload <== if you're running this command second time\nREMEBER about Reading/Executing permissions for others!"
service_err = "Something went wrong.\nHave you added the service entries to the .env file?"
badsite = "Something went wrong.\nHave you typed the correct address?\n..Or maybe the website just doesn't exist?"
random_err = 'Something went wrong. Have you typed correct min/max values?'
    #A.C.L
if os.getenv('ACLmodule') in accept_value:
    ACL_notfounderr = "User history not found."
    ACL_historynotfound = "Default message history does not exist."
    ACL_nopermission = "You don't have permission to use ACL mode. This incident will be reported."
    ACL_rm_all_success = "Cleared all saved message history."
    ACL_rm_all_fail = "Can't clear all message history."
    ACL_rm_user_fail = "Can't clear message history of the selected user. Does it even exist?"



#AdvancedChannelListener
def aclcheck():
    if os.path.exists(f'{maindir}/ACL') == True:
        print("ACL check OK")
    else:
        print("ACL not found.\nCreating...")
        try:
            os.makedirs(f'{maindir}/ACL')
        except:
            print('Cannot create ACL directory.')


#MessageLogging
def userLog(usr, usrmsg, chnl, srv, usr_id, chnl_id, srv_id):
    time = datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')
    if os.path.exists(f'{maindir}/ACL/{usr_id}/message.txt') == True:
        usrmessage = open(f'{maindir}/ACL/{usr_id}/message.txt', 'a', encoding='utf-8')
        usrmessage.write(f'[{time}] [{srv}({srv_id}) / {chnl}({chnl_id})] {usr}: {usrmsg}\n')
        usrmessage.close()
    else:
        print("[ACL] New user detected. Creating new entry...")
        os.makedirs(f'{maindir}/ACL/{usr_id}')
        usrmessage = open(f'{maindir}/ACL/{usr_id}/message.txt', 'a', encoding='utf-8')
        usrmessage.write(f'{displayname} user message log\nUsername: {usr}\nUserID: {usr_id}\n##############################\n\n')
        usrmessage.write(f'[{time}] [{srv}({srv_id}) / {chnl}({chnl_id})] {usr}: {usrmsg}\n')
        usrmessage.close()


def channelLog(usr, usrmsg, chnl, srv, usr_id, chnl_id, srv_id):
    time = datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')
    print(f"[{time}] [Message//{srv}/{chnl}] {usr}: {usrmsg}")
    if os.path.exists(f'{maindir}/ACL/default/message.txt') == True:
        usrmessage = open(f'{maindir}/ACL/default/message.txt', 'a', encoding='utf-8')
        usrmessage.write(f"[{time}] [Message//{srv}/{chnl}] {usr}: {usrmsg}\n")
        usrmessage.close()
    else:
        print("[ACL] Default message history not detected. Creating new entry...")
        os.makedirs(f'{maindir}/ACL/default')
        usrmessage = open(f'{maindir}/ACL/default/message.txt', 'a', encoding='utf-8')
        usrmessage.write(f"[{time}] [Message//{srv}/{chnl}] {usr}: {usrmsg}\n")
        usrmessage.close()



#Module Status
if os.getenv('ACLmodule') in accept_value:
    ACLstatus = 'enabled'
else:
    ACLstatus = 'disabled'

if os.getenv('service_monitor') in accept_value:
    service_status = 'enabled'
else:
    service_status = 'disabled'

#LogModuleStatus [After Status]
if os.getenv('showmodulemessages') in accept_value:
    def logmodule():
        logs = open('Logs.txt', 'a', encoding='utf-8')
        logs.write(f"""
=========={displayname} Built-in modules: ==========
Advanced Channel Listener v{ACLver}: {ACLstatus} 
Service command: {service_status}
\n\n""")
        logs.close()
    logmodule()



#ClientEvent
@client.event
async def on_ready():
    print(f'Logged as {client.user}')
    print(f'Welcome in ServerBot v{ver}')
    #Load Database
    load_db()
    #slash_command_sync
    try:
        syncd = await client.tree.sync()
        print(f'Synced {len(syncd)} slash command(s)')
    except:
        print("Can't sync slash commands")
    #showmodulemessages
    if os.getenv('showmodulemessages') in accept_value:
            if os.getenv('ACLmodule') in accept_value:
                print('Advanced Channel Listener module enabled')
                aclcheck()
            else:
                print('[showmodulemessages] A.C.L. is disabled.')
    print('Bot runtime: ', datetime.datetime.now())
    print('=' *40)



@client.event
async def on_message(message):
    #Username
    username = str(message.author).split('#')[0]
    #UserMessage
    user_message = str(message.content)
    #Channel
    try:
        channel = str(message.channel.name)
    except AttributeError:
        channel = str(message.channel)
    #Server
    try:
        server = str(message.guild.name)
    except AttributeError:
        server = str(message.guild)
    #UserID
    userid = message.author.id
    #ChannelID
    channelid = message.channel.id
    #ServerID
    try:
        serverid = message.guild.id
    except AttributeError:
        serverid = "DM"

    #A.C.L
    if os.getenv('ACLmodule') in accept_value:
        channelLog(username, user_message, channel, server, userid, channelid, serverid)
        userLog(username, user_message, channel, server, userid, channelid, serverid)

    register_user(userid, username)

    await client.process_commands(message)



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
    except Exception as err:
        if extendedErrMess:
            await ctx.reply(f'{random_err}\nPossible cause: {err}')
        else:
            await ctx.reply(random_err)

#2
@client.command(name='essa', help='Check your "essa"')
async def essa(ctx):
    import random
    losessa = random.randrange(101)
    await ctx.send(f'Twój dzisiejszy poziom essy: {losessa}%')
    
    message = f'Information[Random/Fun]: Someone has {losessa}% of essa'
    printMessage(message)
    logMessage(message)

#3
@client.command(name='botbanner', help='Shows Bots Banner')
async def banner(ctx):
    await ctx.send(f'```{banner}```')

#4
@client.command(name='banner', help='Shows your text as Banner')
async def banner1(ctx, *, text):
    banner1 = pyfiglet.figlet_format(text)
    await ctx.send(f'```{banner1}```')

#5
@client.command(name='blankthing', help='Just blank thing')
async def blank(ctx):
    await ctx.send('ㅤ')

#6
@client.command(name='apple', help='Test for be an Apple')
async def blank(ctx):
    await ctx.send('')

#7
@client.command(name='ai', help=f'Talk with AI.\nUses {ai_model} model.\n.ai [question]')
async def ai(ctx, *, question):
    try:
        response = ai_client.models.generate_content(
            model=f"{ai_model}", 
            contents=question, 
            config=types.GenerateContentConfig(
                system_instruction=[f'{os.getenv("instructions")}', f'You are a {displayname} v{ver} Discord Bot based on your language model ({ai_model}) and ServerBot v{ver} from GitHub project (https://github.com/kamile320/serverbot).'],
                tools=[
                    types.Tool(
                        google_search=types.GoogleSearch()
                    )
                ]
            )
        )
        await ctx.reply(response.text)
    except Exception as err:
        await ctx.reply(f"Something went wrong, possible cause:\n{err}")
        
        error_message = f"DiscordCommandException[AI]: {err}"
        printMessage(error_message)
        logMessage(error_message)

#8
@client.command(name='GNU+Linux', help='Richard Stallman.')
async def gnu(ctx):
    await ctx.send("I’d just like to interject for a moment. What you’re refering to as Linux, is in fact, GNU/Linux, or as I’ve recently taken to calling it, GNU plus Linux. Linux is not an operating system unto itself, but rather another free component of a fully functioning GNU system made useful by the GNU corelibs, shell utilities and vital system components comprising a full OS as defined by POSIX.  Many computer users run a modified version of the GNU system every day, without realizing it. Through a peculiar turn of events, the version of GNU which is widely used today is often called Linux, and many of its users are not aware that it is basically the GNU system, developed by the GNU Project.  There really is a Linux, and these people are using it, but it is just a part of the system they use. Linux is the kernel: the program in the system that allocates the machine’s resources to the other programs that you run. The kernel is an essential part of an operating system, but useless by itself; it can only function in the context of a complete operating system. Linux is normally used in combination with the GNU operating system: the whole system is basically GNU with Linux added, or GNU/Linux. All the so-called Linux distributions are really distributions of GNU/Linux!")

#9
@client.command(name='badge')
async def badge(ctx, member: discord.Member):
    try:
        user_flags = member.public_flags.all()
        badges = [flag.name for flag in user_flags]
        await ctx.send(f'{member} has the following badges: {", ".join(badges)}')
    except:
        await ctx.reply("Incorrect user or incomplete command. Use .badge @user")
        #Random/Fun-END



        #BotInfo
#1
@client.command(name='manual', help="Sends HTML manual\n'web' - see manual in browser\n'local' - download HTML manual from Discord")
async def manual(ctx, type):
    try:
        if type == 'web':
            await ctx.send("ServerBot user Manual [PL](https://Kamile320.github.io/ServerBot/manualPL.html) [EN](https://Kamile320.github.io/ServerBot/manualEN.html)")
        elif type == 'local':
            await ctx.send(file=discord.File(f'{maindir}/manualEN.html'))
        else:
            await ctx.send("Wrong type.\nChoose 'web' to read manual in browser or 'local' to download .html from Discord")
    except:
        await ctx.send(f"Something went wrong. Try again.")

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
Discord Server: [Here](https://discord.gg/UMtYGAx5ac)

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
@client.command(name='release', help='Shows last changes of Bot functions/Changelog')
async def newest_update(ctx):
    await ctx.send(f"""
[ServerBot v{ver}]
    Changelog:
- Added database support (sqlite3)
- Bot moderators now must be defined in the database
- Updated ACL module to v3.1
- Removed .issues command (use GitHub Issues page)
- Pip installers now use requirements.txt file
- Small change in version naming - now each version has a scheme X.Y.Z(-tag)
  instead of X.Y or X.Y.Z
  X -> Major changes incompatible with older versions
  Y -> Normal updates, new functions
  Z -> Bugfixes, small changes
  (-tag) -> marks versions (like X.Y.Z-test as unfinished version; 
  these versions will not have a release on GitHub)
- Moved extendedErrMess variable to the .env file
- Added .db .showdb commands
- Updates in .gitignore
- Minor fixes and improvements

To see older releases, find 'updates.txt' in 'Files' directory.
""")

#6
@client.command(name='next_update', help='Shows future functions/updates')
async def next_update(ctx):
    await ctx.send("""
Ideas for Future Updates
- Better Informations/Errors
- More slash commands
- Database support for leveling system (sqlite3)
You can give your own ideas on my [Discord Server](https://discord.gg/UMtYGAx5ac)
""")
        #BotInfo-END



        #AdminOnly
#1
@client.command(name='ShutDown', help='Turns Off the Bot')
async def ShutDown(ctx):
    if str(ctx.message.author.id) in admin_usr:
        print("Information[ShutDown]: Started turning off the Bot")
        try:
            print("Saving Logs.txt...")
            src = open(f'{maindir}/Logs.txt', 'r')
            logs = open(f'{maindir}/Files/Logs.txt', 'a')
            append = f"\n\n{src.read()}"
            logs.write(append)
            logs.close()
            src.close()
            print("Logs.txt saved successfully.")
        except:
            print("Error occurred while saving log.")
        try:
            print("Closing database...")
            db = sqlite3.connect('Files/serverbot.db')
            db.close()
        except:
            print("Failed to close databse.")

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
@client.command(name='bash', help='Runs Bash like scripts on hosting computer (Linux only)\nUses .sh extensions\nBest to work with .touch command')
async def bash(ctx, file):
    if str(ctx.message.author.id) in admin_usr:
        try:
            subprocess.run(['bash', file])
        except:
            await ctx.send(f'Failed to run Script')
    else:
        await ctx.reply(not_allowed)

#4
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
            
            os.makedirs(f'{maindir}/Files/setup')
            os.makedirs(f'{maindir}/Media')
            os.chdir(maindir)
            await ctx.send("Success.\nRebuilded Files with no content")
        except:
            await ctx.send("Can't rebuild files.")
    else:
        await ctx.reply(not_allowed)

#5
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
            
            message = f"Information[mkshortcut]: Created desktop shortcut ({home_dir})"
            printMessage(message)
            logMessage(message)
        except:
            await ctx.send('Something went wrong, please try again.')
    else:
        await ctx.send(not_allowed)

#6
@client.command(name="mksysctlstart", help="Adds ServerBot to systemctl to start with system startup (Bot needs to be running as root)\nMode:\n'def' -> creates default autorun entry (python3)\n'venv' -> creates autorun entry that uses python virtual environment created by setup.sh (mkvenv.sh)\n.venv directory is located in the ServerBot main directory\nIt's recommended to save bot files into main (root) directory (/ServerBot) with 775 permissions (chmod 775 recursive). Without these permissions to bot files, systemctl startup will not work. Do not place bot in your home dir.")
async def mksysctlstart(ctx, mode):
    if str(ctx.message.author.id) in admin_usr:
        try:
            if mode == 'def':
                try:
                    await ctx.send("Making autorun.sh file..")
                    try:
                        auto = open('Files/autorun.sh', 'w')
                        auto.write(f"#!/bin/bash\ncd {maindir}\npython3 ServerBot.py")
                        auto.close()
                        await ctx.send('Done.')

                        message = f"Information[mksysctlstart]: Created autorun.sh file (Files/autorun.sh)"
                        logMessage(message)
                        printMessage(message)
                    except:
                        await ctx.send("Can't create file!")

                    await ctx.send('Making ServerBot.service in /etc/systemd/system..')
                    try:
                        sys = open('/etc/systemd/system/ServerBot.service', 'w')
                        sys.write(f"[Unit]\nDescription=ServerBot autorun service\n\n[Service]\nExecStart={maindir}/Files/autorun.sh\n\n[Install]\nWantedBy=multi-user.target")
                        sys.close()
                        await ctx.send('Done!')
                        await ctx.send(SBservice)

                        message = f"Information[mksysctlstart]: Created ServerBot service file (/etc/systemd/system/)\n{SBservice}"
                        logMessage(message)
                        printMessage(message)
                    except:
                        await ctx.send("Can't create service file!\nAre you root?")
                except Exception as error:
                    await ctx.send(f'Got 1 error (or more) while creating systemctl entry.\nPossible cause: {error}')
            elif mode == 'venv':
                try:
                    await ctx.send('Making autorun.sh file..')
                    try:
                        auto = open('Files/autorun.sh', 'w')
                        auto.write(f'#!/bin/bash\ncd {maindir}\n.venv/bin/python3 ServerBot.py')
                        auto.close()
                        await ctx.send('Done.')

                        message = f"Information[mksysctlstart]: Created autorun.sh file (Files/autorun.sh)"
                        logMessage(message)
                        printMessage(message)
                    except:
                        await ctx.send("Can't create file!")

                    await ctx.send('Making ServerBot.service in /etc/systemd/system..')
                    try:
                        sys = open('/etc/systemd/system/ServerBot.service', 'w')
                        sys.write(f"[Unit]\nDescription=ServerBot autorun service\n\n[Service]\nExecStart={maindir}/Files/autorun.sh\n\n[Install]\nWantedBy=multi-user.target")
                        await ctx.send("Done!")
                        await ctx.send(SBservice)
                    
                        message = f"Information[mksysctlstart]: Created ServerBot service file (/etc/systemd/system/)\n{SBservice}"
                        logMessage(message)
                        printMessage(message)
                    except:
                        await ctx.send("Can't create service file!\nAre you root?")
                except Exception as error:
                    await ctx.send(f'Got 1 error (or more) while creating systemctl entry.\nPossible cause: {error}')
        except:
            await ctx.send(f"""```{bluescreenface}``` Unexpected problem ocurred""")
    else:
        await ctx.send(not_allowed)

#7
if os.getenv('service_monitor') in accept_value:
    @client.command(name="service", help="Lists active/inactive services. To add service entry, enter service name in .env file (service_list)\nUses systemctl\n\nlist -> lists entries in '.env' file\nstatus -> lists service entries and checks if they're active\nstatus-detailed -> same as above, but with details (systemctl status [service name])\n[service name] -> shows current status of service in systemctl")
    async def service(ctx, mode):
        if str(ctx.message.author.id) in admin_usr:
            try:
                if mode == 'list':
                    try:
                        listdir_env = os.getenv('service_list')
                        await ctx.send(f'**Service Entries:**\n{listdir_env}')
                    except:
                        await ctx.send(service_err)

                elif mode == 'status':
                    try:
                        listdir_env = os.getenv('service_list')
                        listdir = [item.strip() for item in listdir_env.split(',')]
                        await ctx.send("**Service Activity:**")
                        for file in listdir:
                            await ctx.send(f"```{file}: {subprocess.getoutput([f'systemctl is-active {file}'])}```")
                    except:
                        await ctx.send(service_err)

                elif mode == 'status-detailed':
                    try:
                        listdir_env = os.getenv('service_list')
                        listdir = [item.strip() for item in listdir_env.split(',')]
                        await ctx.send("**Service Activity:**")
                        for file in listdir:
                            await ctx.send(f"```{file}: {subprocess.getoutput([f'systemctl status {file}'])}```")
                    except:
                        await ctx.send(service_err)

                else:
                    try:
                        await ctx.send(f"**Service {mode}:**")
                        await ctx.send(f"```{subprocess.getoutput([f'systemctl status {mode}'])}```")
                    except Exception as err:
                        await ctx.send(f'Something went wrong.\nPossible cause: {err}')

            except Exception as err:
                await ctx.send(f'Something went wrong.\nPossible cause: {err}')
        else:
            await ctx.send(not_allowed)

#8
@client.command(name='pingip', help='Pings selected IPv4 address.')
async def pingip(ctx, ip):
    if str(ctx.message.author.id) in admin_usr:
        try:
            ipaddr = ip
            await ctx.send(f"```{subprocess.getoutput([f'ping {ipaddr} -c 1'])}```")
        except:
            await ctx.send('Something went wrong')
    else:
        await ctx.send(not_allowed)

#9
@client.command(name='module', help='Shows status of built-in modules')
async def module(ctx):
    if str(ctx.message.author.id) in admin_usr:
        #ACL
        if os.getenv('ACLmodule') in accept_value:
            ACLstatus = 'enabled'
        else:
            ACLstatus = 'disabled'
        #Service
        if os.getenv('service_monitor') in accept_value:
            service_status = 'enabled'
        else:
            service_status = 'disabled'
        
        await ctx.send(f"""
==========**{displayname} Built-in modules: **==========
Advanced Channel Listener v{ACLver}: {ACLstatus} 
Service command:  {service_status}
""")
    else:
        await ctx.send(not_allowed)
        #AdminOnly-END



        #Database
#1
@client.command(name='db', help='Database commands\n.db register {userID} - manually registers user in database\n.db remove {userID} - removes user from database\n.db op {userID} - gives Moderator role to user (Discord bot mod)\n.db deop {userID} - removes Mod role from user')
async def db(ctx, mode, value1, *, value2=None):
    if str(ctx.message.author.id) in admin_usr:
        db = sqlite3.connect(db_dir)
        cur = db.cursor()
        if mode == 'register':
            if value2 is None:
                value2 = "No nickname"
            try:
                #INSERT
                cur.execute(f"INSERT INTO users (discord_id, username) VALUES (?, ?)", (value1, value2,))
                db.commit()
                #SELECT
                res = cur.execute(f'SELECT * FROM users WHERE discord_id=?', (value1,))

                await ctx.reply(f"Result: {res.fetchall()}")
            except Exception as err:
                await ctx.reply(f'Error: {err}')
        
        elif mode == 'remove':
            try:
                #DELETE
                cur.execute(f"DELETE FROM users WHERE discord_id = ?", (value1,))
                db.commit()
                #SELECT
                res = cur.execute(f'SELECT * FROM users WHERE discord_id=?', (value1,))

                await ctx.reply(f"Result: {res.fetchall()}")
            except Exception as err:
                await ctx.reply(f'Error: {err}')

        elif mode == 'op':
            try:
                #UPDATE
                cur.execute(f"UPDATE users SET SBrole='mod' WHERE discord_id=?", (value1,))
                db.commit()

                await ctx.reply(f"Opped <@{value1}>.")
            except Exception as err:
                await ctx.reply(f'Error: {err}')

        elif mode == 'deop':
            try:
                #UPDATE
                cur.execute(f"UPDATE users SET SBrole='None' WHERE discord_id=?", (value1,))
                db.commit()

                await ctx.reply(f"Deopped <@{value1}>.")
            except Exception as err:
                await ctx.reply(f'Error: {err}')
    else:
        await ctx.reply(not_allowed)

#2
@client.command(name='showdb', help='Shows database content in .txt file')
async def showdb(ctx):
    if str(ctx.message.author.id) in admin_usr:
        db = sqlite3.connect(db_dir)
        cur = db.cursor()
        #SELECT
        result = cur.execute('SELECT * FROM users')
        #SAVE
        save = open('tempDB.txt', 'w', encoding='utf-8')
        save.write(str(result.fetchall()))
        save.close()

        await ctx.reply("Database content saved in tempDB.txt file.")
        await ctx.send(file=discord.File('tempDB.txt'))
    else:
        await ctx.reply(not_allowed)
        #Database-END



        #ModeratorOnly
#1
@client.command(name='testbot', help='Tests some functions of Host and Bot')
async def testbot(ctx):
    if str(ctx.message.author.id) in mod_usr:
        teraz = datetime.datetime.now()
        await ctx.send(f"""
***S e r v e r  B o t***  *test*:
====================================================
Time: **{teraz.strftime('%d.%m.%Y, %H:%M:%S')}**
Bot name: **{client.user}**
Version: **{ver}**
DisplayName: **{displayname}**
CPU Usage: **{psutil.cpu_percent()}** (%)
CPU Count: **{psutil.cpu_count()}**
CPU Type: **{testbot_cpu_type}**
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
    else:
        await ctx.send(not_allowed)

#2
@client.command(name='testos', help='Check OS of server with running bot. \n .testos <os name> \n eg. .testos linux/windows/macos')
async def testos(ctx, operatingsys):
    if str(ctx.message.author.id) in mod_usr:
        if operatingsys == 'linux':
            await ctx.send(f'Linux: {psutil.LINUX}')
        elif operatingsys == 'windows':
            await ctx.send(f'Windows: {psutil.WINDOWS}')
        elif operatingsys == 'macos':
            await ctx.send(f'MacOS: {psutil.MACOS}')
        else:
            await ctx.send(f'Please enter windows/linux/macos')
    else:
        await ctx.send(not_allowed)

#3
@client.command(name="disks", help="Shows mounted disks with free disk space")
async def disk(ctx):
    if str(ctx.message.author.id) in mod_usr:
        try:
            await ctx.send(f"```{subprocess.getoutput(['df -h'])}```")
        except:
            await ctx.send('Something went wrong\nDo you use Linux?')
    else:
        await ctx.send(not_allowed)

#4
@client.command(name='delete', help='Deletes set amount of messages (eg. .delete 6 => will delete 6 messages)')
async def delete(ctx, amount: int = 0):
    if str(ctx.message.author.id) in mod_usr:
        deleted = await ctx.channel.purge(limit=amount)
        await ctx.channel.send(f'Deleted {len(deleted)} message(s)')
        
        message = f"Information[delete]: Deleted {len(deleted)} messages using '.delete' on channel: {ctx.channel.name}"
        printMessage(message)
        logMessage(message)
    else:
        await ctx.reply(not_allowed)

#5
@client.command(name='cleaner', help='Cleans channel from last 100 messages')
async def cleaner(ctx):
    if str(ctx.message.author.id) in mod_usr:
        deleted = await ctx.channel.purge(limit=100)
        await ctx.channel.send(f'[Cleaner] deleted max amount of messages ({len(deleted)})')
        
        message = f"Information[cleaner]: Deleted {len(deleted)} messages using '.cleaner' on channel: {ctx.channel.name}"
        printMessage(message)
        logMessage(message)
    else:
        await ctx.reply(not_allowed)

#6
@client.command(name="webreq", help="Sends website request codes and headers\n.webreq {get/getheader} {website}")
async def webreq(ctx, mode, *, web):
    if str(ctx.message.author.id) in mod_usr:
        try:
            if mode == 'get':
                try:
                    rq = requests.get(web)
                    await ctx.reply(f"Response: {rq.status_code}")
                except:
                    await ctx.reply(badsite)
            elif mode == 'getheader':
                try:
                    rq = requests.get(web)
                    await ctx.reply(f"Website Header:\n{rq.headers}")
                except:
                    await ctx.reply(badsite)
            else:
                await ctx.reply('')
        except:
            await ctx.reply("Wrong mode.")
    else:
        await ctx.reply(not_allowed)

#7
@client.command(name='kick', help='Kicks Members')
async def kick(ctx, member: discord.Member, *, reason=None):
    if str(ctx.message.author.id) in mod_usr:
        await member.kick(reason=reason)
        await ctx.send(f'Kicked **{member}**')
        
        kicked = f'Information[Server/Members]: Kicked {member}. Reason: {reason}\n'
        printMessage(kicked)
        logMessage(kicked)
    else:
        await ctx.reply(not_allowed)

#8
@client.command(name='ban', help='Bans Members')
async def ban(ctx, member: discord.Member, *, reason=None):
    if str(ctx.message.author.id) in mod_usr:
        await member.ban(reason=reason)
        await ctx.send(f'Banned **{member}**')
        
        banned = f'Information[Server/Members]: Banned {member}. Reason: {reason}\n'
        printMessage(banned)
        logMessage(banned)
    else:
        await ctx.reply(not_allowed)

#9
@client.command(name='unban', help='Unbans Members')
async def unban(ctx, member: discord.Member, *, reason=None):
    if str(ctx.message.author.id) in mod_usr:
        await member.unban(reason=reason)
        await ctx.send(f'Unbanned **{member}**')
        
        unbanned = f'Information[Server/Members]: Unbanned {member}. Reason: {reason}\n'
        printMessage(unbanned)
        logMessage(unbanned)
    else:
        await ctx.reply(not_allowed)
        #ModeratorOnly-END



        #Converters
#1
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
            await ctx.send('Wrong value.\nType: .convert binary/octal/decimal/hexa and value for selected number system')
    except:
        await ctx.send(f'```{bluescreenface}\nUnexpected error occurred```')

#2
@client.command(name='binary', help='Converts decimal number to binary. \n .binary <dec number>; eg. binary 2019')
async def binary(ctx, number):
    binn = bin(int(number))
    await ctx.send(f'{number} in binary: {binn}')
    
    message = f'Information[Command]: Converted {number} to {binn} using .binary'
    printMessage(message)
    logMessage(message)

#3
@client.command(name='hexa', help="Converts decimal number to hexadecimal. \n .hexa <dec number>; eg. hexa 2007")
async def hexadecimal(ctx, number):
    hexa = hex(int(number))
    await ctx.send(f'{number} in hexadecimal: {hexa}')
    
    message = f'Information[Command]: Converted {number} to {hexa} using .hexa'
    printMessage(message)
    logMessage(message)
        #Converters-END



        #VoiceChannel
#1 - connect
@client.command(pass_context=True, name='join', help='Join Voice Channel')
async def connect(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        source = FFmpegPCMAudio(f'{maindir}/Media/Windows XP - Autostart.wav')
        voice.play(source)
        await ctx.reply(f'Connected to {channel.name}')
        
        message = f'Information[VoiceChat]: Joined to {channel.name}'
        printMessage(message)
        logMessage(message)
    else:
        await ctx.reply(voice_not_connected_error)

#2 - disconnect
@client.command(pass_context=True, name='leave', help='Leave Voice Channel')
async def disconnect(ctx):
    if (ctx.voice_client):
        channel = ctx.message.author.voice.channel
        voice = ctx.guild.voice_client
        source = FFmpegPCMAudio(f'{maindir}/Media/Windows XP - Zamkniecie.wav')
        voice.play(source)
        await asyncio.sleep(3)
        await ctx.guild.voice_client.disconnect()
        await ctx.reply("Left from VC")
        
        message = f'Information[VoiceChat]: User forced bot to leave from: {channel.name}'
        printMessage(message)
        logMessage(message)
    else:
        await ctx.reply(leave_error)

#3 - play
@client.command(name='play', help="Play a local music file.\n.play {filename*}\n*With complete directory path when file isn't in maindir")
async def play(ctx, *, name):
    try:
        try:
            channel = ctx.message.author.voice.channel
            voice = await channel.connect()
            
            message = f'Information[VoiceChat]: Joined to {channel.name}'
            printMessage(message)
            logMessage(message)
        except:
            message = f"Information[VoiceChat]: Can't join to {channel.name}. Already joined?"
            print(message)
            logMessage(message)
        try:
            exist = os.path.exists(name)
            if exist == True:
                voice = ctx.guild.voice_client
                source = FFmpegPCMAudio(name)
                voice.play(source)
                await ctx.reply(f'Playing music...\nSource: {name}')
            else:
                await ctx.reply("Can't find source file.")
        except:
            await ctx.reply("Can't play music.\nSource exist?")
    except:
        await ctx.reply(voice_not_connected_error)

#4 - ytplay
@client.command(name='ytplay', help="Play music from YouTube URL\n.ytplay {url/search} {URL/Title}\nurl - playing from YouTube URL's\nsearch - playing from typed phrase")
async def ytplay(ctx, type, *, url):
    try:
        #Joining
        try:
            channel = ctx.message.author.voice.channel
            voice = await channel.connect()
            
            message = f'Information[VoiceChat]: Joined to {channel.name}'
            printMessage(message)
            logMessage(message)
        except:
            message = f"Information[VoiceChat]: Can't join to {channel.name}. Already joined?"
            printMessage(message)
            logMessage(message)
        #URL Playing
        if type == 'url':
            try:
                loop = asyncio.get_event_loop()
                data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
                song = data['url']
                voice = ctx.guild.voice_client
                player = discord.FFmpegPCMAudio(song, **ffmpeg_options)
                voice.play(player)
                await ctx.reply(f'Playing from source...')
            except:
                await ctx.reply("Can't play music.\nSource exist?")
        #Phrase Playing
        elif type == 'search':
            try:
                search_results = ytdl_search.extract_info(f"ytsearch:{url}", download=False)
                for entry in search_results['entries']:
                    output = entry['url']
                    
                    message = f"Information[YouTubePlay-Search]: Found {output}."
                    printMessage(message)
                    logMessage(message)
            except Exception as exc:
                message = f"Information[YouTubePlay-Search]: Failed to use search function.\nCause: {exc}"
                printMessage(message)
                logMessage(message)
                await ctx.reply(f"Something went wrong while searching YouTube Video. See 'Logs.txt' for more details")
            try:
                loop = asyncio.get_event_loop()
                data = await loop.run_in_executor(None, lambda: ytdl.extract_info(output, download=False))
                song = data['url']
                voice = ctx.guild.voice_client
                player = discord.FFmpegPCMAudio(song, **ffmpeg_options)
                voice.play(player)
                await ctx.reply(f'Playing from source...')
            except Exception as exc:
                await ctx.reply(f"Can't play music.\nSource exist?\nPossible cause: {exc}")
        else:
            await ctx.send("Wrong mode. Type '.ytplay url/search link/phrase'")
    except:
        await ctx.reply(voice_not_connected_error)

#5 - ytsearch
@client.command(name='ytsearch', help='Searches YouTube Videos by typed phrase')
async def ytsearch(ctx, *, search):
    try:
        search_results = ytdl_search.extract_info(f"ytsearch:{search}", download=False)
        for entry in search_results['entries']:
            output = entry['url']
            await ctx.reply(f'Found: {output}')
            
            message = f"Information[YouTubeSearch]: Found {output}."
            printMessage(message)
            logMessage(message)
    except Exception as exc:
        await ctx.reply(f"Something went wrong while searching YouTube Video. See 'Logs.txt' for more details")
        
        message = f'Information[YouTubeSearch]: Failed to use search function.\nCause: {exc}'
        printMessage(message)
        logMessage(message)

#6 - stop
@client.command(pass_context=True, name='stop', help='Stop playing audio')
async def stop(ctx):
    voice = ctx.guild.voice_client
    if voice.is_playing():
        voice.stop()
    else:
        await ctx.reply('Music is not playing right now')

#7 - pause
@client.command(pass_context = True, name='pause', help='Pause/Resume playing audio')
async def pause(ctx):
    voice = ctx.guild.voice_client
    if voice.is_playing():
        voice.pause()
    elif voice.is_paused():
        voice.resume()
    else:
        await ctx.reply('Music is not playing on the voice channel right now')

#8 - resume
@client.command(pass_context = True, name='resume', help='Resume playing audio')
async def resume(ctx):
    voice = ctx.guild.voice_client
    if voice.is_paused():
        voice.resume()
    elif voice.is_playing():
        await ctx.send("Music is playing right now")
    else:
        await ctx.reply('Music is not playing on the voice channel right now')

#9 - waiting
@client.command(name='waiting', help="Say everyone that you're waiting!")
async def wait(ctx):
    try:
        voice = ctx.guild.voice_client
        source = FFmpegPCMAudio(f'{maindir}/Media/Team Fortress 2 Upgrade Station.ogg')
        voice.play(source)
        await ctx.reply(f"@everyone, {ctx.author.mention} is waiting!")
    except AttributeError:
        await ctx.reply(voice_not_connected_error)
    except:
        await ctx.reply(ffmpeg_error)

#10 - micspam
@client.command(name='micspam', help='OMEGATRONIC BOT MICSPAM')
async def micspam(ctx):
    try:
        voice = ctx.guild.voice_client
        source = FFmpegPCMAudio(f'{maindir}/Media/OMEGATRONIC BOT MICSPAM.mp3')
        voice.play(source)
    except AttributeError:
        await ctx.reply(voice_not_connected_error)
    except:
        await ctx.reply(ffmpeg_error)
        #VoiceChannel-END



        #FileManager/Directory
#1
@client.command(name='cd', help="Changes directory\nYou can go back by .dir <return>")
async def chdir(ctx, *, directory):
    if str(ctx.message.author.id) in admin_usr:
        try:
            os.chdir(directory)
            await ctx.send(f"changed directory to {os.getcwd()}")
        except:
            await ctx.send("You can't go to this directory; make it or enter existing one")
    else:
        await ctx.send(not_allowed)

#2
@client.command(name='dir', help='Directory commands \n.dir <mode> \n   mode: \nreturn -> Goes back to main dir\ncheck -> checks dir that you are in\nlist -> list of files and directories in your dir\nlistall -> same but easier to read')
async def dir(ctx, *, mode):
    if str(ctx.message.author.id) in admin_usr:
        if mode == 'return':#
            os.chdir(maindir)
            await ctx.send(f'Returned to main directory ({maindir})')

        elif mode == 'check':#
            await ctx.send(f'You are here: {os.getcwd()}')

        elif mode == 'list':#
            listdir = os.listdir()
            await ctx.send(f'Files in **{os.getcwd()}**:\n{", ".join(listdir)}')

        elif mode == 'listall':#
            listdir = os.listdir()
            files_dir = '\n'.join(listdir)
            await ctx.send(f'Files in **{os.getcwd()}**:\n{files_dir}')
    else:
        await ctx.send(not_allowed)

#3      
@client.command(name='file', help='Commands for file/directory creating, deleting etc.\n.file <mode> <filename> \n    mode:\nopen -> opens file (REMEMBER to add extension (.py/.png/etc))\nmakedir -> creates directory (folder)\nchksize -> checks the size of selected file')
async def file(ctx, mode, *,filename):
    if str(ctx.message.author.id) in admin_usr:
        if mode == 'open':#open
            try:
                await ctx.send(file=discord.File(filename))
            except:
                await ctx.send(fileerror)
            
        elif mode == 'mkdir':#mkdir
            try:
                os.makedirs(filename)
                await ctx.send("Created new directory. Use '.dir list' to check this")
            except:
                await ctx.send("Can't create directory.")
                print()
            
        elif mode == 'size':#size
            try:
                size = os.path.getsize(filename)
                await ctx.send(f'Size of {filename} is {size} bytes')
            except:
                await ctx.send('Error')
            
        elif mode == 'create':#create
            try:
                mkfile = open(filename, 'wt')
                mkfile.close()
                await ctx.send("Created new empty file. Use '.dir list' to check this")
            except:
                await ctx.send("Can't create file.")
            
        else:#else
            await ctx.send('Incorrect mode/filename')
    else:
        await ctx.send(not_allowed)

#4
@client.command(name='touch', help='Creates files with selected extension and content.\nGo to selected directory and use .touch command')
async def makefile(ctx, name, *, content):
    if str(ctx.message.author.id) in admin_usr:
        try:
            directory = os.getcwd()
            mkfile = open(name, 'wt', encoding='utf-8')
            mkfile.write(content)
            mkfile.close()

            await ctx.send(f'Created file {name}, in directory {directory}.')
            
            message = f'Information[FileManager]: Created file {name}, in directory {directory}.\nContent: {content}'
            printMessage(message)
            logMessage(message)
        except:
            await ctx.send(f'Something went wrong while creating file.')
    else:
        await ctx.send(not_allowed)
        #FileManager/Directory-END



        #Other
#1
@client.command(name="thread", help="Makes server threads\n.thread {name} {reason}")
async def thread(ctx, name, *, reason):
    try:
        channel = ctx.channel
        await channel.create_thread(name=name, auto_archive_duration=60, slowmode_delay=None, reason=reason)
        await ctx.send(f"Created new thread [{name}]")
        
        message = f"Information[Threads]: Created new thread [{name}] on {channel}. Reason: {reason}"
        printMessage(message)
        logMessage(message)
    except:
        await ctx.send(thread_error)

#2
@client.command(name='Teensie', help='TeensieGif')
async def Teensie(ctx):
    try:
        await ctx.send(file=discord.File(f'{maindir}/Files/Teensie.gif'))
    except:
        await ctx.send('https://media.discordapp.net/attachments/1099605026948780143/1099605179193622570/Teensien.gif')
        #Other-END
 


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
    await ctx.send(os.getenv('dscserv_link'))

#3
@client.command(name='addbot', help='Shows Link to add Bot to other Servers\nstable -> sends link to stable version\ntesting -> sends link to testing version')
async def addbot(ctx, version):
    if version == "stable":
        await ctx.reply(os.getenv('addstable'))
    elif version == "testing":
        await ctx.reply(os.getenv('addtesting'))
    else:
        await ctx.send("Wrong value, try again.")

#4
@client.command(name='yt', help='Sends Link to YT\ntest1\ntest2')
async def yt(ctx, YTname):
    if YTname == 'test1':
        await ctx.send(f'test1')
    elif YTname == 'test2':
        await ctx.send(f'test2')
    else:
        await ctx.send("Wrong name")
        #Links_and_Servers-END



    ###Built-in Modules###
        
        #AdvancedChannelListener
#1
if os.getenv('ACLmodule') in accept_value:
    @client.command(name='ACL', help='Manage A.C.L. users messages saved history\ngetusr - shows User history by User ID\nget history - history of all saved messages\nclear [all/user_id] - removes all saved messages or only messages of selected user')
    async def ACL(ctx, mode, *, value):
        if str(ctx.message.author.id) in admin_usr:
            if mode == 'getusr':
                try:
                    await ctx.send(file=discord.File(f'{maindir}/ACL/{value}/message.txt'))
                except:
                    await ctx.send(ACL_notfounderr)
            elif mode == 'get' and value == 'history':
                try:
                    await ctx.send(file=discord.File(f'{maindir}/ACL/default/message.txt'))
                except:
                    await ctx.send(ACL_historynotfound)
            elif mode == 'clear':
                if value == 'all':
                    try:
                        shutil.rmtree(f'{maindir}/ACL/')
                        await ctx.send(ACL_rm_all_success)
                        message = f"Information[ACL]: {ACL_rm_all_success} Command executed by: {ctx.author.id}\n"
                        printMessage(message)
                        logMessage(message)
                    except Exception as exc:
                        if extendedErrMess:
                            await ctx.send(f"{ACL_rm_all_fail} \nException: {exc}")
                        else:
                            await ctx.send(ACL_rm_all_fail)
                        message = f"Information[ACL]: User {ctx.message.author.id} tried to clear all message history but failed. \nException: \n{exc}\n"
                        printMessage(message)
                        logMessage(message)
                else:
                    try:
                        shutil.rmtree(f'{maindir}/ACL/{value}')
                        await ctx.send(f"Cleared message history of <@{value}>.")
                        message = f"Information[ACL]: User {ctx.message.author.id} cleared message history of {value}.\n"
                        printMessage(message)
                        logMessage(message)
                    except Exception as exc:
                        if extendedErrMess:
                            await ctx.send(f"{ACL_rm_user_fail} \nException: {exc}")
                        else:
                            await ctx.send(ACL_rm_user_fail)
                        message = f"Information[ACL]: User {ctx.message.author.id} tried to clear message history of {value} but failed. \nException: \n{exc}\n"
                        printMessage(message)
                        logMessage(message)
            else:
                await ctx.send("Wrong mode. See '.help ACL' for more info")
        else:
            await ctx.send(ACL_nopermission)
            message = f"Information[ACL]: User {ctx.message.author.id} tried to use .ACL command without permission.\nSee {maindir}/ACL/{ctx.message.author.id} for more information.\n"
            printMessage(message)
            logMessage(message)
        #AdvancedChannelListener-END



        #Test_Commands
#1
#@client.command(name='test', help='test', tts=True)
#async def test(ctx):
#    await ctx.send(f'test {ctx.author.mention}')

#2
#@client.command(name='ServerKiller', help="Don't use this")
#async def kill(ctx):
#    while True:
#        await ctx.send('@everyone')

        #Test_Commands-END



################################################ S L A S H   C O M M A N D S ###########################################################################################
#1
@client.tree.command(name='random', description='Shows your random number. Type .random [min] [max]')
@app_commands.describe(min="Minimum value", max="Maximum value")
async def random_slash(interaction: discord.Interaction, min: int, max: int):
    import random
    try:
        randomn = random.randrange(min, max)
        await interaction.response.send_message(f'This is your random number: {randomn}')
    except Exception as error:
        if extendedErrMess:
            await interaction.response.send_message(f'{random_err}\nPossible cause: {error}')
        else:
            await interaction.response.send_message(random_err)

#2
@client.tree.command(name='ping', description='Pings the Bot')
async def ping(interaction):
    await interaction.response.send_message(f':tennis: Pong! ({round(client.latency * 1000)}ms)')

#3
@client.tree.command(name='testbot', description='Tests some functions of Bot')
async def testbot(interaction):
    if str(interaction.user.id) in mod_usr:
        teraz = datetime.datetime.now()
        await interaction.response.send_message(f"""
    ***S e r v e r  B o t***  *test*:
    ====================================================
    Time: **{teraz.strftime('%d.%m.%Y, %H:%M:%S')}**
    Bot name: **{client.user}**
    Version: **{ver}**
    DisplayName: **{displayname}**
    CPU Usage: **{psutil.cpu_percent()}** (%)
    CPU Count: **{psutil.cpu_count()}**
    CPU Type: **{testbot_cpu_type}**
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
    else:
        await interaction.response.send_message(not_allowed)

#4
@client.tree.command(name='ai', description=f'Talk with AI. Uses {ai_model} model.')
@app_commands.describe(question="prompt/question for AI")
async def ai(interaction: discord.Interaction, question: str):
    await interaction.response.defer(thinking=True)
    try:
        response = ai_client.models.generate_content(
            model=f"{ai_model}", 
            contents=question, 
            config=types.GenerateContentConfig(
                system_instruction=[f'{os.getenv("instructions")}', f'You are a {displayname} v{ver} Discord Bot based on your language model ({ai_model}) and ServerBot v{ver} from GitHub project (https://github.com/kamile320/serverbot).'],
                tools=[
                    types.Tool(
                        google_search=types.GoogleSearch()
                    )
                ]
            )
        )
        await interaction.followup.send(response.text)
    except Exception as error:
        await interaction.followup.send(f"Something went wrong, possible cause:\n{error}")
        
        error_message = f"DiscordCommandException[AI]: {error}"
        printMessage(error_message)
        logMessage(error_message)

#5
@client.tree.command(name='random_old', description='Shows your random number [Old version]')
async def random_old(interaction):
    import random
    randomn = random.randrange(-1, 999999)
    await interaction.response.send_message(f'This is your random number: {randomn}')
################################################ S L A S H   C O M M A N D S  - E N D #######################################################################################

try:
    client.run(os.getenv('TOKEN'))
except Exception as err:
    print(f"Can't load Bot Token!\nEnter valid Token in '.env' file!\nPossible cause: {err}")