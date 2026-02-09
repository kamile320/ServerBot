import subprocess
import os
import sys
import datetime


# Bot Version
ver = "1.10.1"
# Bot Name
displayname = "ServerBot"
# Name of service in systemd; change if needed, WITHOUT .service file extension
servicename = "ServerBot"

#ModuleVersion
ACLver = "3.1"



#Directory
maindir = os.getcwd()
SBbytes = os.path.getsize('ServerBot.py')

#Directory for music files; If you set ForceMediaDir to True, bot will be able to use local sounds only from this dir.
medialib = f'{maindir}/Media' 



# .env file template - if .env not exists, bot will automatically create a new one
# Do not type values here!
def create_env():
    try:
        env = open('.env', 'w')
        env.write(f"""#ServerBot v{ver} config file
TOKEN=''
admin_usr = ['']

#AI
AI_token=''
aimodel = 'gemini-2.5-flash'
instructions = ['Answer with max 1500 characters','Always answer in users language','Be precise and truthseeking','Do not answer to illegal, harmful, sexual or violent content']

#Music
JoinLeaveSounds = True
ForceMediaDir = False

#Command_dscserv
dscserv_link = 'https://discord.gg/UMtYGAx5ac'

#Service_list
service_monitor = False
service_list = ','

#Command_addbot
addstable = 'stable_link'
addtesting = 'testing_link'

#Modules
showmodulemessages = False
ACLmodule = False

#ExtendedErrorMessages
extendedErrMess = False""")
        env.close()
    except Exception as err:
        print(f"Error occurred while creating .env file.\nPossible cause: {err}")



#Check flags
if '--help' in sys.argv:
    print(f"""ServerBot v{ver} made by Kamile320\n\n
          Project: https://github.com/kamile320/serverbot\n

          --help                Shows this message\n
          --ignore-pip          Doesn't abort bot startup if an error occur 
                                while loading pip libraries\n
          --version             Shows version information\n
          --reset-env           Removes .env file and creates a new one
                                with default values\n
    """)
    exit()

if '--version' in sys.argv:
    print(f"ServerBot v{ver}\nA.C.L. v{ACLver}")
    exit()
if '--reset-env' in sys.argv:
    print("Removing .env file...")
    if os.path.exists(f'{maindir}/.env'):
        os.remove(f'{maindir}/.env')
        print("Removed .env file.\nCreating new one...")
        create_env()
        print("Created .env file.\nYou can now fill it with proper values.")
    else:
        print(".env file not found.\nCreating new one...")
        create_env()
        print("Created .env file.\nYou can now fill it with proper values.")



if os.path.exists(f'{maindir}/.env') == False:
    create_env()



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
    from discord import app_commands
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



#Intents
intents = discord.Intents.default()
intents.message_content = True
status = ['Windows 98 SE', 'DSaF:DLI', 'Minesweeper', f'{platform.system()} {platform.release()}', 'system32', 'Fallout 2', 'Windows Vista', 'MS-DOS', 'Team Fortress 2', 'Discord Moderator Simulator', 'Arch Linux', f'ServerBot v{ver}', displayname]
choice = random.choice(status)
client = commands.Bot(command_prefix='.', intents=intents, activity=discord.Game(name=choice))
testbot_cpu_type = platform.machine() or 'Unknown'
accept_value = ['True', 'true', 'Enabled', 'enabled', '1', 'yes', 'Yes', 'YES', True]
start_time = datetime.datetime.now()


try:
    load_dotenv()
    ############# token/intents/etc ################
    ai_token = os.getenv('AI_token')
    if ai_token == '': ai_token = None

    admin_usr = os.getenv('admin_usr')
    ai_model = f"{os.getenv('aimodel')}"
    ai_client = genai.Client(api_key=f"{ai_token}")
    extendedErrMess = os.getenv('extendedErrMess')
    JLS = os.getenv('JoinLeaveSounds')
    FMD = os.getenv('ForceMediaDir')
    ################################################
except Exception as err:
    print(f"CAN'T LOAD .env FILE!\nCreate .env file using setup.sh and fill with proper values!\nException: {err}")



#YT_DLP
yt_dl_opts = {"format": "bestaudio/best"}
ytdl = youtube_dl.YoutubeDL(yt_dl_opts)
ffmpeg_options = {"options": "-vn -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 2"}

#YT_DLP - search
ytdl_opts_search = {
    'default_search': 'ytsearch',
    'quiet': True,
    'extract_flat': True,
    'verbose': False, # True for debug
    'noplaylist': True,
    'format': 'bestaudio/best',
    'http_headers': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://www.youtube.com/'}}
ytdl_search = youtube_dl.YoutubeDL(ytdl_opts_search)



#Log_File
logs = open('Logs.txt', 'w')
def createlogs():
    logs.write(f"""S E R V E R  B O T
LOGS
Time: {datetime.datetime.now().strftime('%H:%M:%S, %d.%m.%Y')}
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



#Database - create or load
def load_db():
    if os.path.exists(f"{maindir}/Files/serverbot.db") == True:
        if extendedErrMess in accept_value:
            print("Database found.")
    else:
        print("Database not found. Creating new database...")
        db = sqlite3.connect(f"{maindir}/Files/serverbot.db")
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
    db = sqlite3.connect(f"{maindir}/Files/serverbot.db")
    cur = db.cursor()
    #SELECT
    cur.execute('SELECT 1 FROM users WHERE discord_id=?', (id,))
    if cur.fetchone() is None:
        #INSERT
        cur.execute(f"INSERT INTO users (discord_id, username) VALUES (?, ?) ON CONFLICT(discord_id) DO NOTHING", (id, f"{name}"))
        db.commit()

#Check if mod
def is_mod(id):
    db = sqlite3.connect(f"{maindir}/Files/serverbot.db")
    cur = db.cursor()
    cur.execute("SELECT 1 FROM users WHERE discord_id=? AND SBrole='mod'", (id,))
    if cur.fetchone() is not None:
        return True

#OS check
def os_check():
    if psutil.LINUX:
        return "Linux"
    elif psutil.WINDOWS:
        return "Windows"
    elif psutil.MACOS:
        return "macOS"
    else:
        return "Other / Unknown"



#Information/Errors
fileerror = "Error: File not found"
filelarge = "Error: File too large"
direrror = "Error: Directory not found"
cannotcreatedir = "Error: Can't create directory."
cannotcreatefile = "Error: Can't create file."
chksize_error = "Error occurred while checking file size."
copiedlog = f"Information[ServerLog]: Copied Log to {maindir}/Files"
ffmpeg_error = "FFmpeg is not installed or File not found"
voice_not_connected_error = "You must be connected to VC first!"
not_playing = "Music is not playing right now."
leave_error = "How can I left, when I'm not in VC?"
thread_error = "Something went wrong. Try to type:\n.thread {NameWithoutSpaces} {Reason}\nReason is optional"
not_allowed = "You're not allowed to use this command."
SBservice = "Run post installation commands to enable ServerBot.service to start with system startup:\nsudo chmod 775 -R /BotDirectory/*\nsudo systemctl enable ServerBot -> Enables automatic startup\nsudo systemctl start ServerBot -> Optional (turns on Service)\nsudo systemctl daemon-reload -> if you're running this command second time\nREMEBER about Reading/Executing permissions for others!"
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
    except Exception as err:
        print("Can't sync slash commands\nSee Logs.txt for details.")
        logMessage(f"Information[SlashCommandSync]: Error occurred while syncing slash commands.\nException: {err}")

    #showmodulemessages
    if os.getenv('showmodulemessages') in accept_value:
            if os.getenv('ACLmodule') in accept_value:
                print('Advanced Channel Listener module enabled')
                aclcheck()
            else:
                print('[showmodulemessages] A.C.L. is disabled.')

    print(start_time.strftime('Time: %H:%M:%S           Day: %d.%m.%Y'))
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
@client.command(name='botbanner', help='Show Bots Banner')
async def botbanner(ctx):
    await ctx.send(f'```{banner}```')

#3
@client.command(name='banner', help='Show your text as Banner')
async def userbanner(ctx, *, text=None):
    if text is not None:
        userbanner = pyfiglet.figlet_format(text)
        await ctx.send(f'```{userbanner}```')
    else:
        await ctx.send("Incomplete command.\nType text to convert to banner.")

#4
@client.command(name='blankthing', help='Just blank thing')
async def blank(ctx):
    await ctx.send('ㅤ')

#5
@client.command(name='apple', help='Test for be an Apple')
async def blank(ctx):
    await ctx.send('')

#6
@client.command(name='ai', help=f'Talk with AI.\nUses {ai_model} model.\n.ai [question]')
async def ai(ctx, *, question):
    try:
        response = ai_client.models.generate_content(
            model=f"{ai_model}", 
            contents=question, 
            config=types.GenerateContentConfig(
                system_instruction=[f'{os.getenv("instructions")}', f'You are a {displayname} Discord Bot based on your language model ({ai_model}) and ServerBot v{ver} from GitHub project (https://github.com/kamile320/serverbot).'],
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

#7
@client.command(name='GNU+Linux', help='Richard Stallman.')
async def gnu(ctx):
    await ctx.send("I’d just like to interject for a moment. What you’re refering to as Linux, is in fact, GNU/Linux, or as I’ve recently taken to calling it, GNU plus Linux. Linux is not an operating system unto itself, but rather another free component of a fully functioning GNU system made useful by the GNU corelibs, shell utilities and vital system components comprising a full OS as defined by POSIX.  Many computer users run a modified version of the GNU system every day, without realizing it. Through a peculiar turn of events, the version of GNU which is widely used today is often called Linux, and many of its users are not aware that it is basically the GNU system, developed by the GNU Project.  There really is a Linux, and these people are using it, but it is just a part of the system they use. Linux is the kernel: the program in the system that allocates the machine’s resources to the other programs that you run. The kernel is an essential part of an operating system, but useless by itself; it can only function in the context of a complete operating system. Linux is normally used in combination with the GNU operating system: the whole system is basically GNU with Linux added, or GNU/Linux. All the so-called Linux distributions are really distributions of GNU/Linux!")

#8
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
- Updated structure of .env file and improved file creation in setup.sh
- Now bot will create empty .env file on start if it doesn't exists
- Updated voice commands
- Updated .testbot .testos commands
- Added .library command
- Added --reset-env flag
- Small fixes and improvements

To see older releases, find 'updates.txt' in 'Files' directory.
""")

#6
@client.command(name='next_update', help='Shows future functions/updates')
async def next_update(ctx):
    await ctx.send("""
Ideas for Future Updates
- Better Informations/Errors
- More slash commands
- Database support and leveling system (sqlite3)
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
async def bash(ctx, file=None):
    if str(ctx.message.author.id) in admin_usr:
        try:
            if file is not None:
                message = f'Information[Bash]: User {ctx.message.author.id} executed script: {file}'
                printMessage(message)
                logMessage(message)

                subprocess.run(['bash', file])
            else:
                await ctx.reply("Incomplete command.\nType '.bash {filename}'")
        except Exception as err:
            message = f'Information[Bash]: User {ctx.message.author.id} failed to run script {file}.\nPossible cause: {err}'
            printMessage(message)
            logMessage(message)

            if extendedErrMess in accept_value:
                await ctx.send(f'Failed to run Script\nPossible cause: {err}')
            else:
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
@client.command(name="mkservice", help="Adds ServerBot to systemd to start with system startup (Bot needs to be running as root)\nMode:\n'def' -> creates default autorun entry (python3)\n'venv' -> creates autorun entry that uses python virtual environment created by setup.sh (mkvenv.sh)\n.venv directory is located in the ServerBot main directory\nIt's recommended to save bot files into main (root) directory (/ServerBot) with 775 permissions (chmod 775 recursive). Without these permissions to bot files, systemd startup will not work. Do not place bot in your home dir.")
async def mkservice(ctx, mode):
    if str(ctx.message.author.id) in admin_usr:
        try:
            if mode == 'def':
                try:
                    await ctx.send("Making autorun.sh file..")
                    try:
                        auto = open('Files/autorun.sh', 'w')
                        auto.write(f"#!/bin/bash\ncd {maindir}\npython3 ServerBot.py")
                        auto.close()
                        os.chmod('Files/autorun.sh', 0o775)
                        await ctx.send('Done.')

                        message = f"Information[mkservice]: Created autorun.sh file (Files/autorun.sh)"
                        logMessage(message)
                        printMessage(message)
                    except:
                        await ctx.send("Can't create file!")

                    await ctx.send(f'Making {servicename}.service in /etc/systemd/system..')
                    try:
                        sys = open(f'/etc/systemd/system/{servicename}.service', 'w')
                        sys.write(f"[Unit]\nDescription=ServerBot autorun service\n\n[Service]\nExecStart={maindir}/Files/autorun.sh\n\n[Install]\nWantedBy=multi-user.target")
                        sys.close()
                        await ctx.send('Done!')
                        await ctx.send(SBservice)

                        message = f"Information[mkservice]: Created {servicename} service file (/etc/systemd/system/)\n{SBservice}"
                        logMessage(message)
                        printMessage(message)
                    except:
                        await ctx.send("Can't create service file!\nAre you root?")
                except Exception as error:
                    await ctx.send(f'Got 1 error (or more) while creating systemd entry.\nPossible cause: {error}')
            elif mode == 'venv':
                try:
                    await ctx.send('Making autorun.sh file..')
                    try:
                        auto = open('Files/autorun.sh', 'w')
                        auto.write(f'#!/bin/bash\ncd {maindir}\n.venv/bin/python3 ServerBot.py')
                        auto.close()
                        os.chmod('Files/autorun.sh', 0o775)
                        await ctx.send('Done.')

                        message = f"Information[mkservice]: Created autorun.sh file (Files/autorun.sh)"
                        logMessage(message)
                        printMessage(message)
                    except:
                        await ctx.send("Can't create file!")

                    await ctx.send(f'Making {servicename}.service in /etc/systemd/system..')
                    try:
                        sys = open(f'/etc/systemd/system/{servicename}.service', 'w')
                        sys.write(f"[Unit]\nDescription=ServerBot autorun service\n\n[Service]\nExecStart={maindir}/Files/autorun.sh\n\n[Install]\nWantedBy=multi-user.target")
                        await ctx.send("Done!")
                        await ctx.send(SBservice)

                        message = f"Information[mkservice]: Created {servicename} service file (/etc/systemd/system/)\n{SBservice}"
                        logMessage(message)
                        printMessage(message)
                    except:
                        await ctx.send("Can't create service file!\nAre you root?")
                except Exception as error:
                    await ctx.send(f'Got 1 error (or more) while creating systemd entry.\nPossible cause: {error}')
        except:
            await ctx.send(f"""```{bluescreenface}``` Unexpected problem occurred""")
    else:
        await ctx.send(not_allowed)

#7
if os.getenv('service_monitor') in accept_value:
    @client.command(name="service", help="Lists active/inactive services. To add service entry, enter service name in .env file (service_list)\nUses systemctl\n\nlist -> lists entries in '.env' file\nstatus -> lists service entries and checks if they're active\nstatus-detailed -> same as above, but with details (systemctl status [service name])\n[service name] -> shows current status of service in systemd")
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
@client.command(name='db', help='Database commands\n.db register {userID} {nickname} - manually registers user in database. Nickname is optional\n.db remove {userID} - removes user from database.\n.db op {userID} - gives Moderator role to user (Discord bot mod).\n.db deop {userID} - removes Mod role from user.\n.db select {userID} - search user data in database.\n.db setnickname {nickname} {userID} - updates user nickname.')
async def db(ctx, mode, value1, *, value2=None):
    if str(ctx.message.author.id) in admin_usr:
        db = sqlite3.connect(f"{maindir}/Files/serverbot.db")
        cur = db.cursor()

        if mode == 'register':
            try:
                if value2 is None:
                    value2 = "No nickname"
                #INSERT
                cur.execute(f"INSERT INTO users (discord_id, username) VALUES (?, ?)", (value1, value2,))
                db.commit()
                #SELECT
                res = cur.execute(f"SELECT * FROM users WHERE discord_id=?", (value1,))

                await ctx.reply(f"Registered user <@{value1}>.\n{res.fetchall()}")
            except Exception as err:
                await ctx.reply(f"Error: {err}")
        
        elif mode == 'remove':
            try:
                #DELETE
                cur.execute(f"DELETE FROM users WHERE discord_id = ?", (value1,))
                db.commit()
                #SELECT
                res = cur.execute(f"SELECT * FROM users WHERE discord_id=?", (value1,))

                await ctx.reply(f"Removed user with ID {value1}.")
            except Exception as err:
                await ctx.reply(f"Error: {err}")

        elif mode == 'op':
            try:
                #UPDATE
                cur.execute(f"UPDATE users SET SBrole='mod' WHERE discord_id=?", (value1,))
                db.commit()

                gained = f"User <@{value1}> gained Moderator privileges."
                await ctx.reply(gained)
                logMessage(gained)
                printMessage(gained)
            except Exception as err:
                await ctx.reply(f"Error: {err}")

        elif mode == 'deop':
            try:
                #UPDATE
                cur.execute(f"UPDATE users SET SBrole='None' WHERE discord_id=?", (value1,))
                db.commit()

                revoked = f"Revoked Moderator privileges from <@{value1}>"
                await ctx.reply(revoked)
                logMessage(revoked)
                printMessage(revoked)
            except Exception as err:
                await ctx.reply(f"Error: {err}")

        elif mode == 'select':
            try:
                #SELECT
                res = cur.execute(f"SELECT * FROM users WHERE discord_id=?", (value1,))

                await ctx.reply(f"Data of user <@{value1}>:\n{res.fetchall()}")
            except Exception as err:
                await ctx.reply(f"Error: {err}")

        elif mode == 'setnickname':
            try:
                if value2 is None:
                    value2 = ctx.message.author.id
                #UPDATE
                cur.execute(f"UPDATE users SET username=? WHERE discord_id=?", (value1, value2,))
                db.commit()

                #SELECT
                res = cur.execute(f"SELECT username, discord_id FROM users WHERE discord_id=?", (value2,))

                await ctx.reply(f"Updated nickname of <@{value2}> in the database.\n{res.fetchall()}")
            except Exception as err:
                await ctx.reply(f"Error: {err}")

        else:
            await ctx.reply("Wrong mode selected. Use '.help db' for help.")
    else:
        await ctx.reply(not_allowed)

#2
@client.command(name='showdb', help='Shows database content in .txt file')
async def showdb(ctx):
    if str(ctx.message.author.id) in admin_usr:
        db = sqlite3.connect(f"{maindir}/Files/serverbot.db")
        cur = db.cursor()
        #SELECT
        result = cur.execute("SELECT * FROM users")
        #SAVE
        save = open(f"{maindir}/tempDB.txt", 'w', encoding='utf-8')
        save.write(str(result.fetchall()))
        save.close()

        await ctx.reply("Database content saved in tempDB.txt file.")
        await ctx.send(file=discord.File(f"{maindir}/tempDB.txt"))
    else:
        await ctx.reply(not_allowed)
        #Database-END



        #ModeratorOnly
#1
@client.command(name='testbot', help='Tests some functions of Host and Bot')
async def testbot(ctx):
    if str(ctx.message.author.id) in admin_usr or is_mod(ctx.message.author.id):
        now = datetime.datetime.now()
        await ctx.send(f"""
***S e r v e r  B o t***  *test*:
========================================================
Time: **{now.strftime('%H:%M:%S, %d.%m.%Y')} [Day {(now - start_time).days}]**
Bot name: **{client.user}**
DisplayName: **{displayname}**
Version: **{ver}**
CPU Usage: **{psutil.cpu_percent()}%**
CPU Cores: **{psutil.cpu_count(logical=False)}/{psutil.cpu_count(logical=True)}**
Arch: **{testbot_cpu_type}**
RAM Usage: **{psutil.virtual_memory().percent}%**
Ping: **{round(client.latency * 1000)} ms**
OS Type: **{os_check()}**
OS Version: **{platform.system()} {platform.release()}**
OS Kernel: **{platform.version()}**
Bot Current Dir: **{os.getcwd()}**
Bot Main Dir: **{maindir}**
Music library: **{medialib}**
File size: **{os.path.getsize(f'{maindir}/ServerBot.py')} B**
Floppy: **{'Yes' if os.path.exists('/dev/fd0') else 'No'}**
========================================================""")
    else:
        await ctx.send(not_allowed)

#2
@client.command(name='testos', help='Check information about Operating System and Hardware')
async def testos(ctx):
    if str(ctx.message.author.id) in admin_usr or is_mod(ctx.message.author.id):
        await ctx.send(f"""
***Operating System Information***:
========================================================
Type: **{os_check()}**
Version: **{platform.system()} {platform.release()}**
Kernel: **{platform.version()}**
Hostname: **{platform.node() or 'Unknown'}**

Hardware info:
    CPU Usage: **{psutil.cpu_percent()}%**
    RAM Usage: **{psutil.virtual_memory().percent}%**
    CPU Cores: **{psutil.cpu_count(logical=False)}/{psutil.cpu_count(logical=True)}**
    Arch: **{testbot_cpu_type}**
========================================================""")
    else:
        await ctx.send(not_allowed)

#3
@client.command(name="disks", help="Shows mounted disks with free disk space")
async def disk(ctx):
    if str(ctx.message.author.id) in admin_usr or is_mod(ctx.message.author.id):
        try:
            await ctx.send(f"```{subprocess.getoutput(['df -h'])}```")
        except:
            await ctx.send('Something went wrong\nDo you use Linux?')
    else:
        await ctx.send(not_allowed)

#4
@client.command(name='delete', help='Deletes set amount of messages\n.delete 6 -> will delete 6 messages')
async def delete(ctx, amount: int = 1):
    if str(ctx.message.author.id) in admin_usr or is_mod(ctx.message.author.id):
        deleted = await ctx.channel.purge(limit=amount+1)
        await ctx.channel.send(f'Deleted {len(deleted)-1} message(s)')
        
        message = f"Information[delete]: Deleted {len(deleted)-1} messages using '.delete' on channel: //{ctx.guild.name}/{ctx.channel.name}"
        printMessage(message)
        logMessage(message)
    else:
        await ctx.reply(not_allowed)

#5
@client.command(name='cleaner', help='Wipes out last 100 messages on channel')
async def cleaner(ctx):
    if str(ctx.message.author.id) in admin_usr or is_mod(ctx.message.author.id):
        deleted = await ctx.channel.purge(limit=100)
        await ctx.channel.send(f'[Cleaner] Deleted last 100 messages.')
        
        message = f"Information[cleaner]: Deleted {len(deleted)} messages using '.cleaner' on channel: //{ctx.guild.name}/{ctx.channel.name}"
        printMessage(message)
        logMessage(message)
    else:
        await ctx.reply(not_allowed)

#6
@client.command(name="webreq", help="Sends website request codes and headers\n.webreq {get/getheader} {website}")
async def webreq(ctx, mode, *, web):
    if str(ctx.message.author.id) in admin_usr or is_mod(ctx.message.author.id):
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
                await ctx.reply('Wrong mode.\nSee .help webreq for help.')
        except Exception as err:
            message = f"DiscordCommandException[webreq]: {err}"
            if extendedErrMess in accept_value:
                await ctx.reply(f"Error occurred: {err}")
                printMessage(message)
                logMessage(message)
            else:
                await ctx.reply("Error occurred.")
                printMessage(message)
                logMessage(message)
    else:
        await ctx.reply(not_allowed)

#7
@client.command(name='kick', help='Kick Members\n.kick @member {reason} - reason is optional')
async def kick(ctx, member: discord.Member, *, reason=None):
    if str(ctx.message.author.id) in admin_usr or is_mod(ctx.message.author.id):
        try:
            await member.kick(reason=reason)
            await ctx.send(f'Kicked **{member}**')

            kicked = f'Information[Server/Members]: Kicked {member} with userID:{member.id}. Reason: {reason}\n'
            printMessage(kicked)
            logMessage(kicked)
        except Exception as err:
            await ctx.reply(f"Error occurred: {err}")
    else:
        await ctx.reply(not_allowed)

#8
@client.command(name='ban', help='Ban Members\n.ban @member {reason} - reason is optional')
async def ban(ctx, member: discord.Member, *, reason=None):
    if str(ctx.message.author.id) in admin_usr or is_mod(ctx.message.author.id):
        try:
            await member.ban(reason=reason)
            await ctx.send(f'Banned **{member}**')

            banned = f'Information[Server/Members]: Banned {member} with userID:{member.id}. Reason: {reason}\n'
            printMessage(banned)
            logMessage(banned)
        except Exception as err:
            await ctx.reply(f"Error occurred: {err}")
    else:
        await ctx.reply(not_allowed)

#9
@client.command(name='unban', help='Unban Members\n.unban @member {reason} - reason is optional')
async def unban(ctx, member: discord.User, *, reason=None):
    if str(ctx.message.author.id) in admin_usr or is_mod(ctx.message.author.id):
        try:
            await ctx.guild.unban(member, reason=reason)
            await ctx.send(f'Unbanned **{member}**')

            unbanned = f'Information[Server/Members]: Unbanned {member} with userID:{member.id}. Reason: {reason}\n'
            printMessage(unbanned)
            logMessage(unbanned)
        except discord.errors.NotFound:
            await ctx.reply(f"User {member} is not banned.")
        except Exception as err:
            await ctx.reply(f"Error occurred: {err}")
    else:
        await ctx.reply(not_allowed)

#10
@client.command(name='invitegen', help="Create invite link to specific channel via ID.\n.invitegen {channelID} - if None, bot will create invite link to current channel.")
async def invitegen (ctx, channel_id: int = None):
    if str(ctx.message.author.id) in admin_usr or is_mod(ctx.message.author.id):
        try:
            if channel_id is None:
                channel = client.get_channel(ctx.message.channel.id)
            else:
                channel = client.get_channel(channel_id)
            
            if channel is not None:
                invite = await channel.create_invite(reason=None, max_age=86400, max_uses=0, temporary=False, unique=True)
                await ctx.reply(f"Invite link: {invite.url}")
            else:
                await ctx.reply(f"Channel does not exist.")
        except Exception as err:
            await ctx.reply(f"Error occurred: {err}")
    else:
        await ctx.reply(not_allowed)

#11
@client.command(name='echo', help="Make the bot say something.\n.echo {channelID} {message} - you have to type channel ID. It's recommended to use slash version of this command (easier to use).")
async def echo (ctx, channel_id: int, *, message):
    if str(ctx.message.author.id) in admin_usr or is_mod(ctx.message.author.id):
        try:
            channel = client.get_channel(channel_id)

            if channel is not None:
                await channel.send(message)
            else:
                await ctx.reply(f"Can't find channel. Type proper channel ID.")
        
        except Exception as err:
            if extendedErrMess in accept_value:
                await ctx.reply(f"Error occurred: {err}")
            else:
                await ctx.reply(f"Can't send message. Have you typed command and channel ID correctly?")
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
@client.command(name='binary', help='Convert decimal number to binary.\n.binary <dec number>; eg. binary 2019')
async def binary(ctx, number):
    binn = bin(int(number))
    await ctx.send(f'{number} in binary: {binn}')
    
    message = f'Information[Command]: Converted {number} to {binn} using .binary'
    printMessage(message)
    logMessage(message)

#3
@client.command(name='hexa', help="Convert decimal number to hexadecimal.\n.hexa <dec number>; eg. hexa 2007")
async def hexadecimal(ctx, number):
    hexa = hex(int(number))
    await ctx.send(f'{number} in hexadecimal: {hexa}')
    
    message = f'Information[Command]: Converted {number} to {hexa} using .hexa'
    printMessage(message)
    logMessage(message)
        #Converters-END



        #VoiceChannel
#1 - connect
@client.command(pass_context=True, name='join', help="Join Voice Channel")
async def connect(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        
        if (JLS in accept_value):
            source = FFmpegPCMAudio(f'{maindir}/Media/join.wav')
            voice.play(source)
        
        await ctx.reply(f'Connected to {channel.name}')
        
        message = f'Information[VoiceChat]: Joined to {channel.name}'
        printMessage(message)
        logMessage(message)
    else:
        await ctx.reply(voice_not_connected_error)

#2 - disconnect
@client.command(pass_context=True, name='leave', help="Leave Voice Channel")
async def disconnect(ctx):
    if (ctx.voice_client):
        channel = ctx.message.author.voice.channel
        voice = ctx.guild.voice_client

        if (JLS in accept_value):
            source = FFmpegPCMAudio(f'{maindir}/Media/leave.wav')
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
@client.command(name='play', help="Play a local music file.\n.play {filename*}\n*Type full directory path when file isn't located in current dir, or if ForceMediaDir is set to False")
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
            if (FMD in accept_value):
                music = f"{medialib}/{name}"
                exist = os.path.exists(music)
                if exist:
                    voice = ctx.guild.voice_client
                    source = FFmpegPCMAudio(music)
                    voice.play(source)
                    await ctx.reply(f"Playing {name}...")
                else:
                    await ctx.reply("Can't find source file from library.")

            else:
                exist = os.path.exists(name)
                if exist:
                    voice = ctx.guild.voice_client
                    source = FFmpegPCMAudio(name)
                    voice.play(source)
                    await ctx.reply(f'Playing music...\nSource: {name}')
                else:
                    await ctx.reply("Can't find source file.")
        
        except Exception as err:
            if (extendedErrMess in accept_value):
                await ctx.reply(f"Can't play music.\nPossible cause: {err}")
            else:
                await ctx.reply("Can't play music.\nSource exist?")
    
    except Exception as err:
        if (extendedErrMess in accept_value):
            await ctx.reply(f"{voice_not_connected_error}\nException: {err}")
        else:
            await ctx.reply(f"{voice_not_connected_error}")

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
@client.command(name='ytsearch', help="Search YouTube Videos by typed phrase")
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
@client.command(pass_context=True, name='stop', help="Stop playing audio")
async def stop(ctx):
    voice = ctx.guild.voice_client
    if voice.is_playing():
        voice.stop()
    else:
        await ctx.reply(not_playing)

#7 - pause
@client.command(pass_context = True, name='pause', help="Pause/Resume playing audio")
async def pause(ctx):
    voice = ctx.guild.voice_client
    if voice.is_playing():
        voice.pause()
    elif voice.is_paused():
        voice.resume()
    else:
        await ctx.reply(not_playing)

#8 - resume
@client.command(pass_context = True, name='resume', help="Resume playing audio")
async def resume(ctx):
    voice = ctx.guild.voice_client
    if voice.is_paused():
        voice.resume()
    elif voice.is_playing():
        await ctx.send("Music is playing right now")
    else:
        await ctx.reply(not_playing)

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

#10 - library
if (FMD in accept_value):
    @client.command(name='library', help="Show list of music files in media library")
    async def library(ctx):
            list = os.listdir(medialib)
            nl = ',\n'
            await ctx.send(f"**Music files in media library:**\n{nl.join(list)}")
        #VoiceChannel-END



        #FileManager/Directory
#1
@client.command(name='cd', help="Changes directory\nYou can go back using '.dir <return>'")
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
@client.command(name='dir', help="Directory commands\n.dir return -> Goes back to main dir\n.dir check -> checks where you are\n.dir list -> list of files and directories in your dir\n.dir listall -> same but easier to read")
async def dir(ctx, *, mode):
    if str(ctx.message.author.id) in admin_usr:
        if mode == 'return':#
            os.chdir(maindir)
            await ctx.send(f"Returned to main directory ({maindir})")

        elif mode == 'check':#
            await ctx.send(f"You are here: {os.getcwd()}")

        elif mode == 'list':#
            listdir = os.listdir()
            await ctx.send(f"Files in **{os.getcwd()}**:\n{', '.join(listdir)}")

        elif mode == 'listall':#
            listdir = os.listdir()
            files_dir = '\n'.join(listdir)
            await ctx.send(f"Files in **{os.getcwd()}**:\n{files_dir}")
    else:
        await ctx.send(not_allowed)

#3
@client.command(name='file', help='Manage/open/create files and directories\n.file open {filename} -> open file (REMEMBER to add extension (.py/.png/etc))\n.file mkdir {dir_name} -> create directory (folder)\n.file size {filename} -> check size of selected file\n.file create {filename} {content} -> create file with content (like .touch command; content is optional)')
async def file(ctx, mode, filename, *, value=None):
    if str(ctx.message.author.id) in admin_usr:
        if mode == 'open':#open
            try:
                await ctx.send(file=discord.File(filename))
            except Exception as err:
                if extendedErrMess in accept_value:
                    await ctx.send(f"{fileerror}\nPossible cause: {err}")
                else:
                    await ctx.send(fileerror)

        elif mode == 'mkdir':#mkdir
            try:
                directory = os.getcwd()
                message = f"Information[FileManager]: Created directory {filename}, in directory {directory}."
                
                os.makedirs(filename)
                
                await ctx.send("Created new directory.\nUse '.dir list' to check this")
                printMessage(message)
                logMessage(message)
            except Exception as err:
                if extendedErrMess in accept_value:
                    await ctx.send(f"{cannotcreatedir}\nPossible cause: {err}")
                else:
                    await ctx.send(cannotcreatedir)

        elif mode == 'size':#size
            try:
                size = os.path.getsize(filename)
                await ctx.send(f"Size of {filename} is {size} bytes")
            except Exception as err:
                if extendedErrMess in accept_value:
                    await ctx.send(f"{chksize_error}\nPossible cause: {err}")
                else:
                    await ctx.send(f"{chksize_error} File exist?")

        elif mode == 'create':#create
            try:
                directory = os.getcwd()
                response = f"Created '{filename}'.\nUse '.file open {filename}' to see content."
                response_empty = "Created new empty file.\nUse '.dir list' to check this"
                message = f"Information[FileManager]: Created file {filename}, in directory {directory}.\nContent: {value}"

                if value is None:    
                    mkfile = open(filename, 'wt')
                    mkfile.close()

                    await ctx.send(response_empty)
                    printMessage(message)
                    logMessage(message)
                else:
                    mkfile = open(filename, 'wt')
                    mkfile.write(value)
                    mkfile.close()

                    await ctx.send(response)
                    printMessage(message)
                    logMessage(message)
            except Exception as err:
                if extendedErrMess in accept_value:
                    await ctx.send(f"{cannotcreatefile}\nPossible cause: {err}")
                else:
                    await ctx.send(cannotcreatefile)

        else:#else
            await ctx.send("Incorrect mode selected.\nSee '.help file' for help.")
    else:
        await ctx.send(not_allowed)

#4
@client.command(name='touch', help='Create files with selected extension and content.\n.touch {filename} {content} - content is optional')
async def makefile(ctx, name, *, content=None):
    if str(ctx.message.author.id) in admin_usr:
        try:
            directory = os.getcwd()
            response = f"Created file {name}, in directory {directory}."
            message = f"Information[FileManager]: Created file {name}, in directory {directory}.\nContent: {content}"
            
            if content is not None:
                mkfile = open(name, 'wt', encoding='utf-8')
                mkfile.write(content)
                mkfile.close()

                await ctx.send(response)
                printMessage(message)
                logMessage(message)
            else:
                mkfile = open(name, 'wt', encoding='utf-8')
                mkfile.close()

                await ctx.send(response)
                printMessage(message)
                logMessage(message)
        except Exception as err:
            await ctx.send(f"Something went wrong while creating file.\nException: {err}")
    else:
        await ctx.send(not_allowed)
        #FileManager/Directory-END



        #Other
#1
@client.command(name="thread", help="Create server threads\n.thread {name} {reason}")
async def thread(ctx, name, *, reason=None):
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
@client.command(name='dscserv', help='Show link to Discord Server')
async def dscserv(ctx):
    await ctx.send(os.getenv('dscserv_link'))

#3
@client.command(name='addbot', help='Show invite link to add Bot to other Servers\nstable -> sends link to stable version\ntesting -> sends link to testing version')
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
    if str(interaction.user.id) in admin_usr or is_mod(interaction.user.id):
        now = datetime.datetime.now()
        await interaction.response.send_message(f"""
    ***S e r v e r  B o t***  *test*:
    ====================================================
    Time: **{now.strftime('%H:%M:%S, %d.%m.%Y')} [Day {(now - start_time).days}]**
    Bot name: **{client.user}**
    DisplayName: **{displayname}**
    Version: **{ver}**
    CPU Usage: **{psutil.cpu_percent()}%**
    CPU Cores: **{psutil.cpu_count(logical=False)}/{psutil.cpu_count(logical=True)}**
    Arch: **{testbot_cpu_type}**
    RAM Usage: **{psutil.virtual_memory().percent}%**
    Ping: **{round(client.latency * 1000)} ms**
    OS Type: **{os_check()}**
    OS Version: **{platform.system()} {platform.release()}**
    OS Kernel: **{platform.version()}**
    Bot Current Dir: **{os.getcwd()}**
    Bot Main Dir: **{maindir}**
    Music library: **{medialib}**
    File size: **{os.path.getsize(f'{maindir}/ServerBot.py')} B**
    Floppy: **{'Yes' if os.path.exists('/dev/fd0') else 'No'}**
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
                system_instruction=[f'{os.getenv("instructions")}', f'You are a {displayname} Discord Bot based on your language model ({ai_model}) and ServerBot v{ver} from GitHub project (https://github.com/kamile320/serverbot).'],
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

#6
@client.tree.command(name='echo', description="Make the bot say something.")
@app_commands.describe(message="Message to send", channel_id="Channel ID where message will be sent")
async def echo(interaction: discord.Interaction, message: str, channel_id: str = None):
    if str(interaction.user.id) in admin_usr or is_mod(interaction.user.id):
        try:
            if channel_id is None:
                channel_id = interaction.channel_id
                channel = client.get_channel(int(channel_id))
            else:
                channel = client.get_channel(int(channel_id))

            if channel is not None:
                await channel.send(message)
                await interaction.response.send_message("Message sent successfully.", ephemeral=True)
            else:
                await interaction.response.send_message(f"Can't find channel. Type proper channel ID.", ephemeral=True)

        except Exception as err:
            if extendedErrMess in accept_value:
                await interaction.response.send_message(f"Error occurred: {err}", ephemeral=True)
            else:
                await interaction.response.send_message(f"Can't send message. Have you typed command and channel ID correctly?", ephemeral=True)
    else:
        await interaction.response.send_message(not_allowed, ephemeral=True)
################################################ S L A S H   C O M M A N D S  - E N D #######################################################################################

try:
    client.run(os.getenv('TOKEN'))
except Exception as err:
    print(f"Can't load Bot Token!\nEnter valid Token in '.env' file!\nPossible cause: {err}")