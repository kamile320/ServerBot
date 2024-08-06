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
pip install openai==0.28.1
pip install python-dotenv
pip install requests

pause

@echo remember to add FFmpeg .exe files to PATH

pause