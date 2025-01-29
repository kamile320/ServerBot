# ServerBot
Ready Discord Bot

ServerBot is a free project that shares ready code for Discord Bots.<br>
Plays music from YouTube URL's and your local files, have some administration, and the most important - operates with files, directories, and runs shellscripts on your hosting computer.*  
*No one without your permission can go to your host PC using Discord - user ID's of bot admins must be copied to .env file (more info in html manual)

Best to work with Linux-based systems. (Also works with Windows 10/11)

ServerBot is not a Bot hosted by me - this is a project that can be hosted by you, by your own Discord Bot account with your bot token (need to be copied to .env file).<br>
Everything it needs (pip libraries, ffmpeg, repositories etc.) can be installed automatically with setup.sh (Linux) or setup.bat (Windows).<br>
To run setup.sh you need install 'dialog' command using apt, zypper etc.  
If you're using not-Ubuntu 22.04 based distros you need to create python3 virtual environment - easily using setup.sh  

This Bot is also good for administrative tasks for your servers - saying servers I mean not only Discord Servers but real Servers.<br>
You can use a bot like a ssh connection - detect service failures/status, run shellscripts to automate processes or even detect hardware info and free/full space of your mounted volumes.  
Great for lazy game server admins! Because why you should open terminal, connect to the server, check something, log out...  
...when you can do everything in your Discord chat.

More information and instructions you can find in *ServerBot Manual* [[PL]](https://kamile320.github.io/ServerBot/manual.html) [[EN]](https://kamile320.github.io/ServerBot/manualEN.html)

ServerBot is an open project - that means you can make your own version of bot, or help me with making ServerBot way better - better english translations/text, code improvements, bug report etc.

## Commands/Programs that you need to install first (Linux):
- dialog
- python3 (3.9 or newer)
- python3-pip
- Discord Bot user created in [Discord Developer Portal](https://discord.com/developers/docs/intro)
- ffmpeg files and add it to PATH (If you want to use Music Bot features; Windows only)

Every ideas, bug reports or helping in code improvement you can send me on [Discord](https://discord.gg/UMtYGAx5ac)
