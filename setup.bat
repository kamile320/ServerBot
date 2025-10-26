@echo off
@echo ServerBot module auto-setup
@echo This .bat file will download all modules for Python script
@echo Make sure you have downloaded Python 3 with 'pip'

pause

pip install discord
pip install discord.py[voice]
pip install pyfiglet
pip install datetime
pip install psutil
pip install asyncio
pip install google-genai
pip install ffmpeg
pip install python-dotenv
pip install requests
pip install yt_dlp

pause

@echo To use music commands you need to add FFmpeg files to PATH. You can download it here: 
@echo https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl-shared.zip
@echo Extract files, rename folder to 'ffmpeg' and copy it to C:\ffmpeg
@echo Now script will automatically add this files to local user PATH (C:\ffmpeg\bin). In the 'bin' folder must be .exe files of FFmpeg. Add /M to add FFmpeg files to PATH for all users

pause

setx PATH "%PATH%;C:\ffmpeg\bin"
@echo If adding to PATH was successful, you should now restart your computer.

pause