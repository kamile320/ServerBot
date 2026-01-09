# ServerBot 

<a href="https://github.com/kamile320/ServerBot/releases">![GitHub Release](https://img.shields.io/github/v/release/kamile320/serverbot)</a>
<a href="https://github.com/kamile320/ServerBot/blob/main/LICENSE">![GitHub License](https://img.shields.io/github/license/kamile320/serverbot)</a>
<a href="">![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/kamile320/serverbot/total)</a>
<a href="https://github.com/kamile320/ServerBot/commits/main/">![GitHub commits since latest release](https://img.shields.io/github/commits-since/kamile320/serverbot/latest)</a>

<a href="https://github.com/kamile320/ServerBot/stargazers">![GitHub Repo stars](https://img.shields.io/github/stars/kamile320/serverbot)</a>  
<a href="https://github.com/kamile320/ServerBot/forks">![GitHub forks](https://img.shields.io/github/forks/kamile320/serverbot)</a>

ServerBot is a free project that shares ready code for Discord Bots.  
The goal is to create a great Discord Bot base that anyone can use, modify, install with ease and host for your own.  
Play music from YouTube URL's and your local files, talk with AI (gemini based), use administration/moderation commands and the most important - operate with files, directories, and run shellscripts on your hosting computer.[^1]  

Works with Linux and Windows operating systems (Linux/WSL recommended).

ServerBot is not a bot hosted by me - this is a project that can be hosted by you, by your own Discord Bot account with your bot token (need to be copied to .env file).<br>
Everything it needs (pip libraries, ffmpeg, packages etc.) can be installed automatically with setup.sh (Linux) or setup.bat (Windows).<br>
To run setup.sh you need to install 'dialog' command using apt, zypper etc.  
If you're using not-Ubuntu 22.04 based distros you need to create python3 virtual environment - easily using setup.sh  

## Features
- Basic discord commands
- Play music from YouTube/Your local files
- Move through directories and open (send) files on discord[^2]
- Run bash scripts[^2]
- Create systemd entry to start bot with your OS[^2]
- Show status of selected systemd services[^2]
- .ai command to talk with gemini-based AI
- Log messages sent by users on discord channels
- Save every message sent on available (for the bot) discord channels[^3]
- Use sqlite3 database to register users and grant bot moderators access to mod commands (+level system in future)

## Advantages of Linux
This Bot is also good for administrative tasks for your servers - saying servers I mean not only Discord Servers but real Servers.<br>
You can use a bot like a ssh connection - detect service failures/status, run shellscripts to automate processes or even detect hardware info and free/full space of your mounted volumes.  
Great for lazy game server admins! Because why you should open terminal, connect to the server, check something, log out...  
...when you can do it in your Discord chat.

You can use ServerBot like Linux command if you install it using .deb installer (see ServerBot releases).  
More information and instructions you can find in ***ServerBot Manual*** [[PL]](https://kamile320.github.io/ServerBot/manualPL.html) [[EN]](https://kamile320.github.io/ServerBot/manualEN.html)


## Programs that you need to install first (Linux):
- dialog
- python3 (3.9 or newer)
- python3-pip
- Discord Bot user (Application) created in [Discord Developer Portal](https://discord.com/developers/docs/intro)
- The rest will be installed automatically (Bot will tell if something is missing, or just install everything using setup.sh)

## Programs that you need to install first (Windows):
- Python 3 (3.9 or newer; add to PATH + pip)
- Discord Bot user (Application) created in [Discord Developer Portal](https://discord.com/developers/docs/intro)
- [Download FFmpeg](https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl-shared.zip) .exe files and add it to PATH (See [setup.bat](https://github.com/kamile320/ServerBot/blob/main/setup.bat) and HTML manuals)
- The rest will be installed automatically (setup.bat)


## Contributing
ServerBot is an open project - that means you can create your own version of a bot, or help me with making ServerBot better (better English, code improvements, bug report etc.).  

Ways to contribute:
- Create an [Issue](https://github.com/kamile320/ServerBot/issues)  
  - Tell me what should be added, fixed, improved, or if you have any problems with installation/running the bot.  
- Create a [Pull Request](https://github.com/kamile320/ServerBot/pulls)  
  1) Fork the repository
  2) Make your changes
  3) Test your modified version of bot
  4) If everything works without problems - create a Pull Request.  

You can also share your feedback or ask any questions on my [Discord](https://discord.gg/UMtYGAx5ac) server.

[^1]: No one without your permission can go to your host PC using Discord - user ID's of bot admins must be copied to .env file (more info in html manual)
[^2]: As said earlier, only bot administrators (typed in the .env file) can use these commands.  
[^3]: This works as a <a href="https://github.com/kamile320/AdvancedChannelListener">Advanced Channel Listener</a> module - you can turn it on and off.
