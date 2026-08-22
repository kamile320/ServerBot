import subprocess
import os
import sys
import datetime
import sqlite3

# Bot Version
ver = "1.12.0"
# Bot Name
displayname = "ServerBot"
# Name of service in systemd; change if needed, WITHOUT .service file extension
servicename = "ServerBot"


#Directory
maindir = os.path.dirname(os.path.abspath(__file__))
SBbytes = os.path.getsize(f'{maindir}/ServerBot.py')
DB_PATH = f'{maindir}/Files/serverbot.db' # Database path
ai_chat = f'{maindir}/Files/AI_chat'      # Directory where longer Gemini responses are saved

#Directory for music files; If you set ForceMediaDir to True, bot will be able to use local sounds only from this dir.
medialib = f'{maindir}/Media' 

#List of modules/cogs you want to load at start; cogs from subdirectories (like 'modules/custom') you have to type like 'subdirName.cogName' - WITHOUT .py
#If LoadAllModules is True, this list will nothing do; bot will load every cog from 'modules' directory (not from subdirs!)
#If you use cogs from 'modules' directory or subdirectories and you want to load them all on start, type here all your modules and set LAM to False
loadList = [] # ['cog1', 'custom.cog2'] <- example; custom is the name of a directory inside 'modules' dir


# .env file template - if .env not exists, bot will automatically create a new one
# Do not type values here!
def create_env():
    try:
        with open(f'{maindir}/.env', 'w', encoding='utf-8') as env:
            env.write(f"""#ServerBot v{ver} config file
TOKEN=''
admin_usr = ['']
custom_prefix = ''
addBot = 'inviteLink'

#AI
AI_token = ''
AI_model = 'gemini-2.5-flash'
instructions = ['Always answer in users language','Be precise and truthseeking','Do not answer to illegal, harmful, sexual or violent content']

#Music
JoinLeaveSounds = True
ForceMediaDir = False

#Command_dscserv
dscserv_link = 'https://discord.gg/UMtYGAx5ac'

#Modules
LoadAllModules = False

#ExtendedErrorMessages
extendedErrMess = False

#Service_module
service_list = ','""")

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
    print(f"ServerBot v{ver}")
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
    exit()



#Automatic .env creation
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
    from dotenv import load_dotenv
    import asyncio
    import psutil
    import requests
    import random
    import shutil
    import pyfiglet
    import platform
    import yt_dlp as youtube_dl
    from google import genai
    from google.genai import types
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



#Loading .env
try:
    load_dotenv()
    ############# token/intents/etc ################
    TOKEN = os.getenv('TOKEN') or ''
    prefix = os.getenv('custom_prefix') or '.'
    
    ai_token = os.getenv('AI_token')
    if ai_token == '': ai_token = None

    admin_usr = os.getenv('admin_usr')
    ai_model = f"{os.getenv('AI_model')}" or 'gemini-2.5-flash'
    ai_client = genai.Client(api_key=f"{ai_token}")
    extendedErrMess = str(os.getenv('extendedErrMess')).lower()
    JLS = str(os.getenv('JoinLeaveSounds')).lower()
    FMD = str(os.getenv('ForceMediaDir')).lower()
    LAM = str(os.getenv('LoadAllModules')).lower()
    ################################################
except Exception as err:
    print(f"CAN'T LOAD .env FILE!\nCreate .env file using setup.sh and fill it with proper values!\nException: {err}")



#Intents
intents = discord.Intents.default()
intents.message_content = True
status = ['Windows 98 SE', 'Minesweeper', f'{platform.system()} {platform.release()}', 'system32', 'Fallout 2', 'Windows Vista', 'MS-DOS', 'Team Fortress 2', 'Discord Moderator Simulator', 'Arch Linux', f'ServerBot v{ver}', displayname]
choice = random.choice(status)
client = commands.Bot(command_prefix=prefix, intents=intents, activity=discord.Game(name=choice))
testbot_cpu_type = platform.machine() or 'Unknown'
accept_value = ['true', 'enabled', 'ena', 'yes', 'y', '1', 1, True]
start_time = datetime.datetime.now()



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
def createlogs():
    with open(f'{maindir}/Logs.txt', 'w', encoding='utf-8') as logs:
        logs.write(f"""S E R V E R  B O T
LOGS
Time: {datetime.datetime.now().strftime('%H:%M:%S, %d.%m.%Y')}
Info: Remember to shut down bot by .ShutDown command or log will be empty.
=============================================================================\n\n""")
createlogs()

#LogMessage
def logMessage(info):
    time = datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')
    with open(f'{maindir}/Logs.txt', 'a', encoding='utf-8') as logs:
        logs.write(f'[{time}] {info}\n')

#PrintMessage
def printMessage(info):
    time = datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')
    print(f'[{time}] {info}')



#Database - create if not exists
if os.path.exists(f"{maindir}/Files/serverbot.db") == True:
    if extendedErrMess in accept_value:
        print("Database found.")
else:
    print("Database not found. Creating new database...")
    db_create = sqlite3.connect(f"{maindir}/Files/serverbot.db")
    cur = db_create.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users(
                id integer not null primary key AUTOINCREMENT, 
                discord_id integer unique not null, 
                username text, 
                SBrole text default None, 
                exp_points integer default 0, 
                level integer default 0)""")
    db_create.commit()
    db_create.close()

#Database
SB_DB = sqlite3.connect(DB_PATH, check_same_thread=False, timeout=10)

#User registration
def register_user(id, name):
    cur = SB_DB.cursor()
    #SELECT
    cur.execute('SELECT 1 FROM users WHERE discord_id=?', (id,))
    if cur.fetchone() is None:
        #INSERT
        cur.execute(f"INSERT INTO users (discord_id, username) VALUES (?, ?) ON CONFLICT(discord_id) DO NOTHING", (id, f"{name}"))
        SB_DB.commit()

#Check if mod
def is_mod(id):
    cur = SB_DB.cursor()
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
file_error                  = "Error: File not found"
file_large                  = "Error: File too large"
dir_error                   = "Error: Directory not found"
create_dir_fail             = "Error: Can't create directory."
create_file_fail            = "Error: Can't create file."
file_incomplete_cmd         = "Incomplete command. Usage: .file { open | mkdir | size | create } <filename> [content]"
touch_incomplete_cmd        = "Incomplete command. Usage: .touch <filename> [content]"
chksize_error               = "Error occurred while checking file size."
copiedlog                   = f"Information[ServerLog]: Copied Log to {maindir}/Files"
ffmpeg_error                = "FFmpeg is not installed or File not found"
voice_not_connected_error   = "You must be connected to VC first!"
not_playing                 = "Music is not playing right now."
leave_error                 = "How can I left, when I'm not in VC?"
thread_error                = "Something went wrong. Try to type:\n.thread <NameWithoutSpaces> [Reason]\nReason is optional"
not_allowed                 = "You're not allowed to use this command."
SBservice                   = "Run post installation commands to enable ServerBot.service to start with system startup:\nsudo chmod 775 -R /BotDirectory/*\nsudo systemctl enable ServerBot -> Enables automatic startup\nsudo systemctl start ServerBot -> Optional (turns on Service)\nsudo systemctl daemon-reload -> if you're running this command second time\nREMEBER about Reading/Executing permissions for others!"
badsite                     = "Something went wrong.\nHave you typed the correct address?\n..Or maybe the website just doesn't exist?"
random_err                  = 'Something went wrong. Have you typed correct min/max values?'



#ClientEvent
@client.event
async def on_ready():
    print(f'Logged as {client.user}')
    print(f'Welcome in ServerBot v{ver}')
    
    #Load_cog_modules_on_ready
    #   Load all built-in modules from 'modules' directory; cogs from subdirectories you have to load manually, or add to loading list as 'subdirName.cogName'
    if LAM in accept_value:
        for i in os.listdir(f'{maindir}/modules'):
            try:
                if i.endswith('.py'):
                    await client.load_extension(f"modules.{i[:-3]}")
                    if extendedErrMess in accept_value:
                        message = f"Loaded {i[:-3]} module."
                        print(message)
                        logMessage(message)
            except Exception as err:
                message = f"Failed to load {i} module: {err}"
                print(message)
                logMessage(message)
    #   If LAM is False, bot will load only modules selected in loadList variable
    else:
        if loadList != []:
            for i in loadList:
                try:
                    await client.load_extension(f"modules.{i}")
                    if extendedErrMess in accept_value:
                        message = f"Loaded {i} module."
                        print(message)
                        logMessage(message)
                except Exception as err:
                    message = f"Failed to load {i} module: {err}"
                    print(message)
                    logMessage(message)

    #Slash_command_sync
    try:
        syncd = await client.tree.sync()
        print(f'Synced {len(syncd)} slash command(s)')
    except Exception as err:
        print("Can't sync slash commands\nSee Logs.txt for details.")
        logMessage(f"Information[SlashCommandSync]: Error occurred while syncing slash commands: {err}")

    print(start_time.strftime('Time: %H:%M:%S\nDay:  %d.%m.%Y'))
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

    for cog in client.cogs.values():
        if hasattr(cog, 'on_message_hook'):
            await cog.on_message_hook(message)

    register_user(userid, username)

    await client.process_commands(message)

#ClientEvent-END



#Commands
        #Random/Fun
#1
@client.hybrid_command(
    name        = 'random', 
    description = "Shows your random number. Usage: .random <min> <max>"
    )
@app_commands.describe(
    min='Minimum value', 
    max='Maximum value'
    )
async def random_num(
    ctx, 
    min = commands.parameter(description="- Minimum value", default=int(1)), 
    max = commands.parameter(description="- Maximum value", default=int(100))
    ):
    import random
    await ctx.defer()
    try:
        random_num = random.randint(min, max)
        await ctx.reply(f'This is your random number: {random_num}')
    except Exception as err:
        if extendedErrMess in accept_value:
            await ctx.reply(f'{random_err}\nPossible cause: {err}')
        else:
            await ctx.reply(random_err)


#2
@client.hybrid_command(
    name        = 'botbanner', 
    description = "Show bot's banner"
    )
async def botbanner(ctx):
    await ctx.send(f'```{banner}```')


#3
@client.hybrid_command(
    name        = 'banner', 
    description = "Show your text as a Banner"
    )
@app_commands.describe(
    text='Text to convert to banner'
    )
async def userbanner(
    ctx, *, 
    text = commands.parameter(description='Text to convert to banner', default=None)):
    if text is not None:
        userbanner = pyfiglet.figlet_format(text)
        await ctx.send(f'```{userbanner}```')
    else:
        await ctx.send("Incomplete command.\nType text to convert to banner.")


#4
@client.hybrid_command(
    name        = 'ai', 
    description = f"Talk with AI. Uses {ai_model} model."
    )
@app_commands.describe(
    question='Prompt/question for AI'
    )
async def ai(
    ctx, *, 
    question = commands.parameter(description="- Your prompt/question", default=None)
    ):
    await ctx.defer()
    if ai_token is None:
        await ctx.reply("AI token not found. Enter valid Gemini API token in the .env file to use this command.")
        return
    if question is None:
        await ctx.reply("Incomplete command.\nType your question after command.")
        return
    try:
        response = ai_client.models.generate_content(
            model=f"{ai_model}", 
            contents=f"{question}",
            config=types.GenerateContentConfig(
                system_instruction=[f'{os.getenv("instructions")}', f'You are a {displayname} Discord Bot based on your language model ({ai_model}) and ServerBot v{ver} from GitHub project (https://github.com/kamile320/serverbot).'],
                tools=[
                    types.Tool(
                        google_search=types.GoogleSearch()
                    )
                ]
            )
        )
        message = response.text
        if message is None:
            await ctx.send("AI couldn't answered for that question; returned None.\nMaybe it cannot find information.")
            return
        if extendedErrMess in accept_value:
            length = f"Information[AI]: Length of the bot's response is {len(message)}."
            printMessage(length)
            logMessage(length)
        if len(message) <= 2000:
            await ctx.reply(message)
        else:
            if os.path.exists(ai_chat) == False:
                os.makedirs(ai_chat)
            name = f"ai_response_{datetime.datetime.now().strftime('%d.%m.%Y_%H-%M-%S')}.txt"
            with open(f"{ai_chat}/{name}", 'w', encoding='utf-8') as file:
                file.write(message)
            await ctx.reply(file=discord.File(f"{ai_chat}/{name}"))
    except Exception as err:
        await ctx.reply(f"Something went wrong, possible cause:\n{err}")
        
        error_message = f"DiscordCommandException[AI]: {err}"
        printMessage(error_message)
        logMessage(error_message)


#5
@client.hybrid_command(
    name        = 'badge', 
    description = "Shows user badges. Usage: .badge @user"
    )
@app_commands.describe(
    member = 'Mention user to check badges'
    )
async def badge(
    ctx, 
    member: discord.Member = commands.parameter(description="- Mention user to check badges")
    ):
    try:
        user_flags = member.public_flags.all()
        badges = [flag.name for flag in user_flags]
        await ctx.send(f'{member} has the following badges: {", ".join(badges)}')
    except:
        await ctx.reply("Incorrect user or incomplete command. Use '.badge @user'")
        #Random/Fun-END



        #BotInfo
#1
@client.hybrid_command(
    name        = 'manual', 
    help        = "Sends HTML manual\n'web' - see manual in browser\n'local' - download HTML manual from Discord", 
    description = "Sends HTML manual"
    )
@app_commands.describe(
    type = "{web | local} to see in browser or download from discord"
    )
async def manual(
    ctx, 
    type = commands.parameter(description="- {web | local} to see in browser or download from discord")
    ):
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
@client.hybrid_command(
    name        = 'credits', 
    description = "See credits"
    )
async def credits(ctx):
    embed = discord.Embed(
        title="***S e r v e r B o t***",
        description=f"Version: **{ver}**\nCreated By: [Kamile320](https://github.com/kamile320)",
        color=0xd6930c
    )
    embed.set_author(name=ctx.bot.user.name, icon_url=ctx.bot.user.display_avatar.url)
    embed.add_field(
        name="Links:",
        value="[Discord](https://discord.gg/UMtYGAx5ac)\n"
              "[Source code](https://github.com/kamile320/ServerBot)"
    )
    embed.add_field(
        name="Thanks to:",
        value="- friends for testing Bot",
        inline=False
    )
    embed.add_field(
        name="Used sounds:",
        value="- WinXP/98 sounds - files from OG OS by Microsoft\n"
              "- [TF2 upgrade station](https://youtube.com/watch?v=Q7eJg7hRvqE)",
        inline=False
    )
    await ctx.send(embed=embed)


#3
@client.hybrid_command(
    name        = 'time', 
    description = "Shows local time"
    )
async def time(ctx):
    now = datetime.datetime.now()
    await ctx.send(now.strftime("Time: %H:%M:%S\nDay: %d.%m.%Y"))


#4
@client.hybrid_command(
    name        = 'ping', 
    description = "Pings the bot"
    )
async def ping(ctx):
    await ctx.send(f':tennis: Pong! ({round(client.latency * 1000)}ms)')


#5
@client.hybrid_command(
    name        = 'release', 
    description = "View the latest changes made to the bot's code"
    )
async def newest_update(ctx):
    await ctx.send(f"""
[ServerBot v{ver}]
    Changelog:
- Enhanced pingip: added count parameter, OS detection and better error handling; changed to hybrid command
- Updated .module command - now synces slash commands after every load/reload/unload
- Updated .service command; moved to separate module (service.py) and changed to hybrid command (prefix and slash at once)
- Changed .testbot .ping .random .ai to hybrid commands; removed separate slash versions of these commands
- Updating structure of Admin and Mod only commands - in progress
- Moving most of the commands to hybrid commands (supporting prefix and slash commands at once) - in progress
- Updated .env file scheme
- Updated ACL to v5.0
- Updated file manager/directory commands
- Removed old unused/useless commands
- Updated template cog
- Updated converter commands to v2.0 and moved to separate module (converters.py)
- Fixes and improvements

To see older releases, read 'updates.txt' in the 'Files' directory.
""")


#6
@client.hybrid_command(
    name        = 'next_update', 
    description = "Shows future functions/updates"
    )
async def next_update(ctx):
    await ctx.send("""
Ideas for Future Updates
- Better Informations/Errors
- More embed messages
- Database support and leveling system (sqlite3)
- More advanced module system (cogs) or whole code rewrite to make it more modular and easier to update
You can give your own ideas on my [Discord Server](https://discord.gg/UMtYGAx5ac)
""")
        #BotInfo-END



        #AdminOnly
#1
@client.command(
    name='ShutDown', 
    help="Turn off the Bot"
    )
async def ShutDown(ctx):
    if str(ctx.message.author.id) not in admin_usr:
        await ctx.reply(not_allowed)
        return

    await ctx.send(f'Shutting down...')
    print("Information[ShutDown]: Started turning off the Bot")
    await asyncio.sleep(1)

    try:
        print("Saving Logs.txt...")
        with open(f'{maindir}/Logs.txt', 'r') as src:
            append = f"\n\n{src.read()}"
        with open(f'{maindir}/Files/Logs.txt', 'a') as logs:
            logs.write(append)
    except:
        print("Error occurred while saving log.")

    try:
        print("Closing Discord connection...")
        await client.close()
    except Exception as err:
        message = f"Information[ShutDown]: Failed to disconnect from Discord.\nPossible cause: {err}"
        printMessage(message)
        logMessage(message)
        await ctx.send("Failed to disconnect from Discord. See Logs.txt or console for details.")

    try:
        print("Closing database...")
        SB_DB.close()
    except:
        print("Failed to close databse.")

    print("Information[ShutDown]: Shutting down...")


#2
@client.hybrid_command(
    name='copylog', 
    help="Copies Bot Log file\nappend   -> adds new value to older in Files/Logs.txt\nreplace  -> clears old Files/Logs.txt and adds new content\nclearall -> clears all Logs")
@app_commands.describe(
    mode="{ append | replace | clearall }"
    )
async def copylog(
    ctx, 
    mode = commands.parameter(description="- { append | replace | clearall }")
    ):

    if str(ctx.message.author.id) not in admin_usr:
        await ctx.reply(not_allowed)
        return

    await ctx.defer()
    if mode == 'append':
        try:
            with open(f'{maindir}/Logs.txt', 'r') as src:
                append = f"\n\n{src.read()}"
            with open(f'{maindir}/Files/Logs.txt', 'a') as logs:
                logs.write(append)
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
            with open(f"{maindir}/Logs.txt", 'w', encoding='utf-8') as l1:
                l1.write("")
            with open(f"{maindir}/Files/Logs.txt", 'w', encoding='utf-8') as l2:
                l2.write("")
            await ctx.send("Successfully cleared Logs.")
        except:
            await ctx.send("Can't clear logs.")
    else:
        await ctx.send("Wrong copylog mode.")


#3
@client.command(
    name='bash', 
    help="Runs Bash like scripts on hosting computer (Linux only)\nUses .sh extensions\nBest to work with .touch command"
    )
async def bash(ctx, file=None):
    if str(ctx.message.author.id) not in admin_usr:
        await ctx.reply(not_allowed)
        return

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


#4
@client.hybrid_command(
    name='rebuild', 
    help="Rebuilds files and directories"
    )
async def rebuild(ctx):
    if str(ctx.message.author.id) not in admin_usr:
        await ctx.reply(not_allowed)
        return

    await ctx.defer()
    await ctx.send('Trying to rebuild files...')
    message = "Information[Rebuild]: Started rebuilding files and directories."
    printMessage(message)
    logMessage(message)

    try:
        print("Creating 'Logs.txt'...")
        os.chdir(maindir)
        logs1 = open('Logs.txt', 'w')
        logs1.close()

        print("Creating 'Files' directory...")
        os.makedirs(f'{maindir}/Files')
        os.chdir(f'{maindir}/Files')
            
        print("Creating 'updates.txt'...")
        updates = open('updates.txt', 'w')
        updates.close()

        print("Creating 'Files/Logs.txt'...")
        logs2 = open('Logs.txt', 'w')
        logs2.close()
            
        print("Creating 'Files/setup' directory...")
        os.makedirs(f'{maindir}/Files/setup')

        print("Creating 'Media' directory...")
        os.makedirs(f'{maindir}/Media')
            
        os.chdir(maindir)

        print("Creating 'modules' directory...")
        os.makedirs(f'{maindir}/modules')

        message = "Information[Rebuild]: Successfully rebuilded files and directories."
        printMessage(message)
        logMessage(message)
        await ctx.send("Success.\nRebuilded Files with no content")
    except Exception as error:
        await ctx.send(f"Rebuilding files failed.\nException: {error}")


#5
@client.hybrid_command(
    name='mkshortcut', 
    help="Creates a shortcut on your Desktop. (Linux (Ubuntu 22.04 based) only)\nType: .mkshortcut [Name of your Desktop Folder (Desktop/Pulpit etc.)]"
    )
@app_commands.describe(
    desk="Name of your desktop folder/directory"
    )
async def mkshortcut(
    ctx, 
    desk = commands.parameter(description="- Name of your desktop folder/directory")
    ):

    if str(ctx.message.author.id) not in admin_usr:
        await ctx.reply(not_allowed)
        return

    await ctx.defer()
    try:
        home_dir = os.path.expanduser('~')
        os.chdir(home_dir)
        os.chdir(desk)
        with open('ServerBot.sh', 'w', encoding='utf-8') as shrt:
            shrt.write(f'cd {maindir}\npython3 ServerBot.py')
        os.chdir(maindir)
        await ctx.send('Done.')

        message = f"Information[mkshortcut]: Created desktop shortcut ({home_dir})"
        printMessage(message)
        logMessage(message)
    except:
        await ctx.send('Something went wrong, please try again.')


#6
@client.hybrid_command(
    name='mkservice', 
    help="Adds ServerBot to systemd to start with system startup (Bot needs to be running as root)\nMode:\n'def'  -> creates default autorun entry (python3)\n'venv' -> creates autorun entry that uses python virtual environment created by setup.sh (mkvenv.sh)\n.venv directory is located in the ServerBot main directory\nIt's recommended to save bot files into main (root) directory (/ServerBot) with 775 permissions (chmod 775 recursive). Without these permissions to bot files, systemd startup will not work. Do not place bot in your home dir."
    )
@app_commands.describe(
    mode="'def' for default autorun entry; 'your venv name' for entry in selected venv"
    )
async def mkservice(
    ctx, 
    mode = commands.parameter(description="- { 'def' | 'your venv name' }")
    ):

    if str(ctx.message.author.id) not in admin_usr:
        await ctx.reply(not_allowed)
        return

    await ctx.defer()
    try:
        if mode == 'def':
            try:
                await ctx.send("Making autorun.sh file..")
                try:
                    with open(f'{maindir}/Files/autorun.sh', 'w', encoding='utf-8') as auto:
                        auto.write(f"#!/bin/bash\ncd {maindir}\npython3 ServerBot.py")
                    os.chmod(f'{maindir}/Files/autorun.sh', 0o775)
                    await ctx.send('Done.')

                    message = f"Information[mkservice]: Created autorun.sh file (Files/autorun.sh)"
                    logMessage(message)
                    printMessage(message)
                except:
                    await ctx.send("Can't create file!")

                await ctx.send(f'Making {servicename}.service in /etc/systemd/system..')
                try:
                    with open(f'/etc/systemd/system/{servicename}.service', 'w', encoding='utf-8') as sys:
                        sys.write(f"[Unit]\nDescription=ServerBot autorun service\n\n[Service]\nExecStart={maindir}/Files/autorun.sh\n\n[Install]\nWantedBy=multi-user.target")
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
                    with open(f'{maindir}/Files/autorun.sh', 'w', encoding='utf-8') as auto:
                        auto.write(f'#!/bin/bash\ncd {maindir}\n.venv/bin/python3 ServerBot.py')
                    os.chmod('Files/autorun.sh', 0o775)
                    await ctx.send('Done.')

                    message = f"Information[mkservice]: Created autorun.sh file (Files/autorun.sh)"
                    logMessage(message)
                    printMessage(message)
                except:
                    await ctx.send("Can't create file!")

                await ctx.send(f'Making {servicename}.service in /etc/systemd/system..')
                try:
                    with open(f'/etc/systemd/system/{servicename}.service', 'w', encoding='utf-8') as sys:
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


#7
@client.hybrid_command(
    name        = 'pingip', 
    description = "Pings selected IPv4 address. Usage: .pingip <ip address> [count]"
    )
@app_commands.describe(
    ip    = "IP address or domain/hostname", 
    count = "How many pings/ICMP packets to send"
    )
async def pingip(
    ctx, 
    ip    = commands.parameter(description="- IP address or domain/hostname"), 
    count = commands.parameter(description="- How many pings/ICMP packets to send", default=1)
    ):

    if str(ctx.message.author.id) not in admin_usr:
        await ctx.reply(not_allowed)
        return

    await ctx.defer()
    ipaddr = ip
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    cmd = f'ping {ipaddr} {param} {count}'
    await ctx.send(f"```{subprocess.getoutput(cmd)}```")

@pingip.error
async def pingip_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send("Invalid argument. Usage: .pingip <ip_address> [count]")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing argument. Usage: .pingip <ip_address> [count]")
    else:
        await ctx.send(f'Something went wrong: {error}')


#8
@client.hybrid_command(
    name='module', 
    help="Manage built-in and additional modules (cogs).\nload   -> loads module\nunload -> unloads module\nreload -> reload module\nlist   -> lists available modules from 'modules' directory. Add 'active' to list only active modules."
    )
@app_commands.describe(
    mode="{ load | unload | reload | list }", 
    name="Name of your cog/module or 'active' to see active modules when 'list' mode selected"
    )
async def module(
    ctx, 
    mode = commands.parameter(description="- { load | unload | reload | list }", default=None), *, 
    name = commands.parameter(description="- Cog/module name or 'active' when using 'list'", default=None)
    ):

    if str(ctx.message.author.id) not in admin_usr:
        await ctx.reply(not_allowed)
        return

    await ctx.defer()
    async def sync_cmd():
        try:
            sync = await ctx.bot.tree.sync()
            message = f"Synced {len(sync)} slash commands."
            printMessage(message)
            logMessage(message)
        except Exception as err:
            message = f"Failed to sync slash commands.\nPossible cause: {err}"
            printMessage(message)
            logMessage(message)

    if mode is not None: mode = mode.lower()
    if mode == 'list':
        try:
            br = '\n- '

            if name == 'active':
                loaded_modules = [cog for cog in client.cogs.keys()]
                if not loaded_modules:
                    await ctx.send("There's no active modules.")
                    return
                else:
                    await ctx.send(f"========== **Active modules:** ==========\n- {br.join(loaded_modules)}")
                
            else:
                listdir = []
                for f in os.listdir(f'{maindir}/modules'):
                    if f.endswith('.py'):
                        listdir.append(f.replace('.py', ''))

                await ctx.send(f"""
========== **ServerBot modules: **==========
Available modules:\n- {br.join(listdir)}""")
        except Exception as e:
            await ctx.send(f'Unexpected error occurred. See Logs.txt for details.')
            message = f'Information[modules]: Failed to list modules: {e}'
            printMessage(message)
            logMessage(message)
        return
        
    if mode is None: # If user executed command without selecting mode
        await ctx.reply("Incomplete command. Select mode [load/unload/reload/list].\nSee '.help module' for more information.")
        return
    if name is None: # If user executed command without typing name
        await ctx.reply("Incomplete command. Enter module name.")
        return

    try:
        if mode == 'load':
            opt = 'loaded'
            await client.load_extension(f'modules.{name}')
        elif mode == 'unload':
            opt = 'unloaded'
            await client.unload_extension(f'modules.{name}')
        elif mode == 'reload':
            opt = 'reloaded'
            await client.reload_extension(f'modules.{name}')
        else:
            await ctx.reply("Incorrect mode selected. Use '.help module' for more information.")
            return
            
        await sync_cmd()
        await ctx.reply(f"{name} module {opt}.")
        message = f"Information[modules]: {name} module {opt}."
        printMessage(message)
        logMessage(message)
    except Exception as e:
        await ctx.reply(f"Failed to {mode} {name} module: {e}")
        message = f'Information[modules]: Failed to {opt} {name} module: {e}'
        printMessage(message)
        logMessage(message)


#9
@client.hybrid_command(
    name='sync', 
    description="Sync slash commands"
    )
async def sync(ctx):
    if str(ctx.message.author.id) not in admin_usr:
        await ctx.send(not_allowed)
        return

    await ctx.defer()
    try:
        await ctx.bot.tree.sync()
        await ctx.send("Synced slash commands.")
    except Exception as err:
        await ctx.reply(f"Failed to sync slash commands.\nPossible cause: {err}")
        #AdminOnly-END



        #Database
#1
@client.hybrid_command(
    name='db', 
    help="Database commands\n.db register {userID} {nickname} - manually registers user in database. Nickname is optional.\n.db remove {userID} - removes user from database.\n.db op {userID} - gives Moderator role to user (Discord bot mod).\n.db deop {userID} - removes Mod role from user.\n.db select {userID} - search user data in database.\n.db setnickname {nickname} {userID} - updates user nickname."
    )
@app_commands.describe(
    mode     = "{ register | remove | op | deop | select | setnickname }", 
    user     = "UserID", 
    nickname = "Nickname (optional)"
    )
async def db(
    ctx, 
    mode     = commands.parameter(description="{ register | remove | op | deop | select | setnickname }"), 
    user     = commands.parameter(description="UserID"), *, 
    nickname = commands.parameter(description="Nickname (optional)", default=None)
    ):

    if str(ctx.message.author.id) not in admin_usr:
        await ctx.send(not_allowed)
        return
    
    cur = SB_DB.cursor()

    if mode == 'register':
        try:
            if nickname is None:
                nickname = "No nickname"
            #INSERT
            cur.execute(f"INSERT INTO users (discord_id, username) VALUES (?, ?)", (user, nickname,))
            SB_DB.commit()
            #SELECT
            res = cur.execute(f"SELECT * FROM users WHERE discord_id=?", (user,))

            await ctx.reply(f"Registered user <@{user}>.\n{res.fetchall()}")
        except Exception as err:
            await ctx.reply(f"Error: {err}")

    elif mode == 'remove':
        try:
            #DELETE
            cur.execute(f"DELETE FROM users WHERE discord_id = ?", (user,))
            SB_DB.commit()
            #SELECT
            res = cur.execute(f"SELECT * FROM users WHERE discord_id=?", (user,))

            await ctx.reply(f"Removed user with ID {user}.")
        except Exception as err:
            await ctx.reply(f"Error: {err}")

    elif mode == 'op':
        try:
            #UPDATE
            cur.execute(f"UPDATE users SET SBrole='mod' WHERE discord_id=?", (user,))
            SB_DB.commit()

            gained = f"User <@{user}> gained Moderator privileges."
            await ctx.reply(gained)
            logMessage(gained)
            printMessage(gained)
        except Exception as err:
            await ctx.reply(f"Error: {err}")

    elif mode == 'deop':
        try:
            #UPDATE
            cur.execute(f"UPDATE users SET SBrole='None' WHERE discord_id=?", (user,))
            SB_DB.commit()

            revoked = f"Revoked Moderator privileges from <@{user}>"
            await ctx.reply(revoked)
            logMessage(revoked)
            printMessage(revoked)
        except Exception as err:
            await ctx.reply(f"Error: {err}")

    elif mode == 'select':
        try:
            #SELECT
            res = cur.execute(f"SELECT * FROM users WHERE discord_id=?", (user,))

            await ctx.reply(f"Data of user <@{user}>:\n{res.fetchall()}")
        except Exception as err:
            await ctx.reply(f"Error: {err}")

    elif mode == 'setnickname':
        try:
            if nickname is None:
                nickname = ctx.message.author.id
            #UPDATE
            cur.execute(f"UPDATE users SET username=? WHERE discord_id=?", (user, nickname,))
            SB_DB.commit()

            #SELECT
            res = cur.execute(f"SELECT username, discord_id FROM users WHERE discord_id=?", (nickname,))

            await ctx.reply(f"Updated nickname of <@{nickname}> in the database.\n{res.fetchall()}")
        except Exception as err:
            await ctx.reply(f"Error: {err}")

    else:
        await ctx.reply("Wrong mode selected. Use '.help db' for help.")


#2
@client.hybrid_command(
    name='showdb', 
    help="Save and send database content in .txt file"
    )
async def showdb(ctx):
    if str(ctx.message.author.id) not in admin_usr:
        await ctx.reply(not_allowed)
        return
    
    cur = SB_DB.cursor()
    #SELECT
    result = cur.execute("SELECT * FROM users")
    #SAVE
    with open(f"{maindir}/tempDB.txt", 'w', encoding='utf-8') as save:
        save.write(str(result.fetchall()))

    await ctx.reply("Database content saved in tempDB.txt file.", file=discord.File(f"{maindir}/tempDB.txt"))
        #Database-END



        #ModeratorOnly
#1
@client.hybrid_command(name='testbot', help="Test some functions of Host and Bot")
async def testbot(ctx):
    await ctx.defer()
    if str(ctx.message.author.id) in admin_usr or is_mod(ctx.message.author.id):
        now = datetime.datetime.now()
        loaded_modules = [cog for cog in client.cogs.keys()]
        await ctx.send(f"""
***S e r v e r  B o t***  *test*:
========================================================
Time: **{now.strftime('%H:%M:%S, %d.%m.%Y')} [Day {(now - start_time).days}]**
Bot name: **{client.user}**
DisplayName: **{displayname}**
Version: **{ver}**
Prefix: **{prefix}**
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
Loaded modules: **{len(loaded_modules)}**
File size: **{os.path.getsize(f'{maindir}/ServerBot.py')} B**
Floppy: **{'Yes' if os.path.exists('/dev/fd0') else 'No'}**
========================================================""")
    else:
        await ctx.send(not_allowed)

#2
@client.command(name='testos', help="Check information about Operating System and Hardware")
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
@client.command(name='disks', help="Shows mounted disks with free disk space (Linux only - uses 'df -h' command)")
async def disk(ctx):
    if str(ctx.message.author.id) in admin_usr or is_mod(ctx.message.author.id):
        try:
            await ctx.send(f"```{subprocess.getoutput(['df -h'])}```")
        except:
            await ctx.send('Something went wrong\nDo you use Linux?')
    else:
        await ctx.send(not_allowed)

#4
@client.command(name='delete', help="Deletes set amount of messages\n.delete 6 -> will delete 6 messages")
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
@client.command(name='cleaner', help="Wipes out last 100 messages on channel")
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
@client.command(name='webreq', help="Sends website request codes and headers\n.webreq {get/getheader} {website}")
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
@client.command(name='kick', help="Kick Members\n.kick @member {reason} - reason is optional")
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
@client.command(name='ban', help="Ban Members\n.ban @member {reason} - reason is optional")
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
@client.command(name='unban', help="Unban Members\n.unban @member {reason} - reason is optional")
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



        #VoiceChannel
#1 - connect
@client.command(name='join', help="Join Voice Channel")
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
@client.command(name='leave', help="Leave Voice Channel")
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
            if extendedErrMess in accept_value:
                await ctx.reply(f"Can't play music.\nPossible cause: {err}")
            else:
                await ctx.reply("Can't play music.\nSource exist?")
    
    except Exception as err:
        if extendedErrMess in accept_value:
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
@client.command(name='stop', help="Stop playing audio")
async def stop(ctx):
    voice = ctx.guild.voice_client
    if voice.is_playing():
        voice.stop()
    else:
        await ctx.reply(not_playing)

#7 - pause
@client.command(name='pause', help="Pause/Resume playing audio")
async def pause(ctx):
    voice = ctx.guild.voice_client
    if voice.is_playing():
        voice.pause()
    elif voice.is_paused():
        voice.resume()
    else:
        await ctx.reply(not_playing)

#8 - resume
@client.command(name='resume', help="Resume playing audio")
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
@client.command(name='cd', help="Changes directory.\nYou can go back using '.dir <return>'.")
async def chdir(ctx, *, directory = commands.parameter(description="- Directory name or path.")):
    if str(ctx.message.author.id) not in admin_usr:
        await ctx.send(not_allowed)
        return

    try:
        os.chdir(directory)
        await ctx.send(f"Changed directory to {os.getcwd()}")
    except:
        await ctx.send("You can't go to this directory; make it or enter existing one")

#2
@client.command(name='dir', help="Directory commands\n.dir return  -> Go back to main dir.\n.dir check   -> Check where you are.\n.dir list    -> List of files and directories in your current dir.\n.dir listall -> Same but easier to read.")
async def dir(ctx, *, mode = commands.parameter(default=None, description="- { return | check | list | listall }")):
    if str(ctx.message.author.id) not in admin_usr:
        await ctx.send(not_allowed)
        return
    
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

#3
@client.command(name='file', help="Manage/open/create files and directories.\n.file open   <filename> -> Sends selected file (REMEMBER to add extension - .py/.png/etc.).\n.file mkdir  <dir_name> -> Create directory (folder).\n.file size   <filename> -> Check size of selected file.\n.file create <filename> [content] -> Create file with content (like .touch command).")
async def file(
    ctx, 
    mode        = commands.parameter(default=None, description="- { open | mkdir | size | create }"), 
    filename    = commands.parameter(default=None, description="- Name of the file or complete path."), 
 *, value       = commands.parameter(default=None, description="- The content you want to write while creating a file.")
    ):
    if str(ctx.message.author.id) not in admin_usr:
        await ctx.send(not_allowed)
        return

    if mode is None:
        await ctx.send(file_incomplete_cmd)
        return

    if mode == 'open':#open
        if filename is None:
            await ctx.send(file_incomplete_cmd)
            return
        try:
            await ctx.send(file=discord.File(filename))
        except Exception as err:
            if extendedErrMess in accept_value:
                await ctx.send(f"{file_error}\nPossible cause: {err}")
            else:
                await ctx.send(file_error)

    elif mode == 'mkdir':#mkdir
        if filename is None:
            await ctx.send(file_incomplete_cmd)
            return
        try:
            directory = os.getcwd()
            message = f"Information[FileManager]: Created directory {filename}, in directory {directory}."
                
            os.makedirs(filename)
                
            await ctx.send("Created new directory.\nUse '.dir list' to check this")
            printMessage(message)
            logMessage(message)
        except Exception as err:
            if extendedErrMess in accept_value:
                await ctx.send(f"{create_dir_fail}\nPossible cause: {err}")
            else:
                await ctx.send(create_dir_fail)

    elif mode == 'size':#size
        if filename is None:
            await ctx.send(file_incomplete_cmd)
            return
        try:
            size = os.path.getsize(filename)
            await ctx.send(f"Size of {filename} is {size} bytes")
        except Exception as err:
            if extendedErrMess in accept_value:
                await ctx.send(f"{chksize_error}\nPossible cause: {err}")
            else:
                await ctx.send(f"{chksize_error} File exist?")

    elif mode == 'create':#create
        if filename is None:
            await ctx.send(file_incomplete_cmd)
            return
        try:
            directory = os.getcwd()
            response = f"Created '{filename}'.\nUse '.file open {filename}' to see content."
            response_empty = "Created new empty file.\nUse '.dir list' to check this"
            message = f"Information[FileManager]: Created file {filename}, in directory {directory}.\nContent: {value}"

            if value is not None:    
                with open(filename, 'wt', encoding='utf-8') as mkfile:
                    mkfile.write(value)

                await ctx.send(response)
                printMessage(message)
                logMessage(message)
            else:
                mkfile = open(filename, 'wt', encoding='utf-8')
                mkfile.close()

                await ctx.send(response_empty)
                printMessage(message)
                logMessage(message)
        except Exception as err:
            if extendedErrMess in accept_value:
                await ctx.send(f"{create_file_fail}\nPossible cause: {err}")
            else:
                await ctx.send(create_file_fail)

    else:#else
        await ctx.send("Incorrect mode selected.\nSee '.help file' for more information.")

#4
@client.command(name='touch', help="Create files with selected extension and content.\n.touch <filename> [content]")
async def makefile(
    ctx, 
    filename = commands.parameter(default=None, description="- Filename or complete path to file."), 
 *, content  = commands.parameter(default=None, description="- File content you want to write.")
    ):
    if str(ctx.message.author.id) not in admin_usr:
        await ctx.send(not_allowed)
        return

    if filename is None:
        await ctx.send(touch_incomplete_cmd)
        return

    try:
        directory = os.getcwd()
        response = f"Created file {filename}, in directory {directory}."
        message = f"Information[FileManager]: Created file {filename}, in directory {directory}.\nContent: {content}"
            
        if content is not None:
            with open(filename, 'wt', encoding='utf-8') as mkfile:
                mkfile.write(content)

            await ctx.send(response)
            printMessage(message)
            logMessage(message)
        else:
            mkfile = open(filename, 'wt', encoding='utf-8')
            mkfile.close()

            await ctx.send(response)
            printMessage(message)
            logMessage(message)
    except Exception as err:
        await ctx.send(f"Something went wrong while creating file: {err}")
        #FileManager/Directory-END



        #Other
#1
@client.command(name='thread', help="Create server threads\n.thread {name} {reason}")
async def thread(ctx, name, *, reason=None):
    try:
        channel = ctx.channel
        await channel.create_thread(name=name, auto_archive_duration=60, slowmode_delay=None, reason=reason)
        await ctx.send(f"Created new thread [{name}]")
        
        message = f"Information[Threads]: Created new thread [{name}] on {channel}. Reason: {reason}"
        printMessage(message)
        logMessage(message)
    except Exception as err:
        if extendedErrMess in accept_value:
            await ctx.send(f"{thread_error}\nPossible cause: {err}")
        else:
            await ctx.send(thread_error)
        #Other-END
 


        #Links_and_Servers
#1
@client.command(name='mcservs', help="Shows Addresses to Minecraft Servers\nYou need to enter your own addresses")
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
@client.command(name='dscserv', help="Show link to Discord Server")
async def dscserv(ctx):
    await ctx.send(os.getenv('dscserv_link'))

#3
@client.command(name='addbot', help="Send invite link to add Bot to other Servers")
async def addbot(ctx):
    try:
        await ctx.reply(os.getenv('addBot'))
    except Exception as err:
        if extendedErrMess in accept_value:
            await ctx.send(f"Something went wrong.\nException: {err}")
        else:
            await ctx.send("Something went wrong.")

#4
@client.command(name='yt', help="Sends link to YouTube channels\ntest1\ntest2")
async def yt(ctx, YTname):
    # You can add more if/elif's as you need
    if YTname == 'test1':
        await ctx.send(f'test1') # Replace test1 with link to YouTube channel
    elif YTname == 'test2':
        await ctx.send(f'test2')
    else:
        await ctx.send("Wrong name")
        #Links_and_Servers-END



        #Portal
#1 - link channels
@client.command(name='portal', help="Manage connections between channels. Portal creates connection between two channels, allowing to communicate between them. Bot will send message to other channel after using .psend command in one of connected channels.\n.portal create {id1} {id2} -> creates connection\n.portal remove {id} -> removes connection that contains selected channel ID.\n.portal search {id} -> search for connection with selected channel ID\n.portal show -> saves database with all connections in tempDB.txt file")
async def portal(ctx, mode=None, channel1=None, channel2=None):
    if str(ctx.message.author.id) in admin_usr:
        if mode is None:
            await ctx.reply("Incomplete command. See '.help portal' for more information.")
            return

        try:
            channel1 = int(channel1) if channel1 is not None else None
            channel2 = int(channel2) if channel2 is not None else None
        except:
            await ctx.reply("Please enter valid channel IDs")
            return

        #Create database if not exist
        def check_portal_db():
            if os.path.exists(DB_PATH) == True:
                if extendedErrMess in accept_value:
                    print("Information[portal/create]: Database found.")

                #CREATE TABLE
                cur = SB_DB.cursor()
                cur.execute("""CREATE TABLE IF NOT EXISTS portal(
                            id integer not null primary key AUTOINCREMENT, 
                            channel1 integer unique not null, 
                            channel2 integer unique not null)""")
                SB_DB.commit()
            else:
                print("DATABASE NOT FOUND! Restart bot to create a new one!")

        #Create connection
        def portal_connect(c1, c2):
            cur = SB_DB.cursor()
            #SELECT
            cur.execute('SELECT 1 FROM portal WHERE channel1 IN (?, ?) OR channel2 IN (?, ?)', (c1, c2, c1, c2))
            if cur.fetchone() is not None:
                return False
            else:
                #INSERT
                cur.execute(f"INSERT INTO portal (channel1, channel2) VALUES (?, ?)", (c1, c2))
                SB_DB.commit()
                return True

        #Remove connection
        def portal_disconnect(c1):
            cur = SB_DB.cursor()
            #SELECT
            cur.execute('SELECT 1 FROM portal WHERE channel1=? OR channel2=?', (c1, c1))
            if cur.fetchone() is not None:
                #DELETE
                cur.execute(f"DELETE FROM portal WHERE channel1=? OR channel2=?", (c1, c1))
                SB_DB.commit()
                return True
            else:
                return False


        if mode == 'create':#create
            if not client.get_channel(channel1):
                await ctx.reply(f"Channel '{channel1}' is not accessible by bot.")
                return
            if not client.get_channel(channel2):
                await ctx.reply(f"Channel '{channel2}' is not accessible by bot.")
                return

            await ctx.reply("Creating connection...")
            try:
                check_portal_db()
                if portal_connect(channel1, channel2) == False:
                    await ctx.reply("One of selected channels are already in use.")
                else:
                    await ctx.reply("Success!")
            except Exception as err:
                await ctx.reply(f"Error occurred: {err}")

        elif mode == 'remove':#remove
            await ctx.reply("Removing connection...")
            try:
                rm = portal_disconnect(channel1)
                if rm is True:
                    await ctx.reply("Success!")
                elif rm is False:
                    await ctx.reply("No connection found for your channel.")
            except Exception as err:
                await ctx.reply(f"Error occurred: {err}")

        elif mode == 'search':#search
            cur = SB_DB.cursor()

            res = cur.execute(f"SELECT channel1, channel2 FROM portal WHERE channel1=? OR channel2=?", (channel1, channel1))
            results = res.fetchall()

            if results:
                #ChannelName
                ch1 = client.get_channel(results[0][0])
                ch2 = client.get_channel(results[0][1])
                #ServerName
                ch1guild = ch1.guild.name if ch1 is not None else "DM_Unknown"
                ch2guild = ch2.guild.name if ch2 is not None else "DM_Unknown"

                await ctx.reply(f"Found connection for selected channel:\n\n//{ch1guild}/{ch1} ({results[0][0]})\n//{ch2guild}/{ch2} ({results[0][1]})")
            else:
                await ctx.reply("No connection found for your channel.")

        elif mode == 'show':#show
            cur = SB_DB.cursor()
            #SELECT
            result = cur.execute("SELECT * FROM portal")
            #SAVE
            with open(f"{maindir}/tempDB.txt", 'w', encoding='utf-8') as save:
                save.write(str(result.fetchall()))

            await ctx.reply("Database content saved in tempDB.txt file.")
            await ctx.send(file=discord.File(f"{maindir}/tempDB.txt"))

        else:#else
            await ctx.reply("Wrong mode selected or incomplete command.\nSee .help portal for more info.")
    else:
        await ctx.send(not_allowed)

#2 - send message
@client.command(name='psend', help="Send message to another channel.")
async def portal_send(ctx, *, mess):
    cur = SB_DB.cursor()

    channel_in_id = ctx.channel.id

    def get_output(ch_in):
        try:
            #SELECT
            res = cur.execute(f"SELECT channel1, channel2 FROM portal WHERE channel1=? OR channel2=?", (ch_in, ch_in))
            row = res.fetchone()

            if row[0] == ch_in:
                return row[1]
            elif row[1] == ch_in:
                return row[0]
            else:
                print(f"Information[portal/psend]: No connected channel found for {ch_in}")
                return None
        except Exception as err:
            print(f"Information[portal/psend]: Error while fetching data from database: {err}")

    channel_out_id = get_output(channel_in_id)
    channel_out = client.get_channel(channel_out_id)

    try:
        if channel_out is not None:
            await channel_out.send(f"[{ctx.author}]: {mess}")
        else:
            await ctx.reply("You're using command on a not linked channel, or one of the channels are not accessible by bot.")
    except Exception as err:
        await ctx.reply(f"Error while sending message: {err}")
        #Portal-END



        #Test_Commands
#1
#@client.command(name='test', help="test", tts=True)
#async def test(ctx):
#    await ctx.send(f'test {ctx.author.mention}')

#2
#@client.command(name='ServerKiller', help="Don't use this")
#async def kill(ctx):
#    while True:
#        await ctx.send('@everyone')

        #Test_Commands-END



################################################ S L A S H   C O M M A N D S ################################################
#1
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
############################################ S L A S H   C O M M A N D S - E N D ############################################

try:
    client.run(TOKEN)
except Exception as err:
    print(f"Can't load bot token!\nEnter valid token in the '.env' file!\nPossible cause: {err}")
