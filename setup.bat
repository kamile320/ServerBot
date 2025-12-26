@echo off
@echo ServerBot module auto-setup
@echo This .bat file will download all modules for Python script
@echo Make sure you have downloaded Python 3 with 'pip'

pause

pip install -r Files\setup\requirements.txt

pause

@echo To use music commands you have to add FFmpeg files to PATH. You can download it here: 
@echo https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl-shared.zip
@echo Extract files, rename folder to 'ffmpeg' and copy it to C:\ffmpeg

pause

@echo Now you have to manually add FFmpeg files to local user PATH (C:\ffmpeg\bin). FFmpeg '.exe' files should be placed in the 'bin' folder.
@echo In Windows GUI:
@echo 1. Open Start Menu and search for 'Environment Variables' - select 'Edit the system environment variables'
@echo 2. Select 'Path' variable in 'User variables' and click 'Edit'
@echo 3. Click 'New' and add 'C:\ffmpeg\bin' (without quotes)
@echo 4. Click OK to close all windows
@echo 5. Restart your computer to apply changes

pause