Buttery Biscuit Bot! This time in Python.

Add to a server (*should* be public, lmk if not):
https://discordapp.com/oauth2/authorize?client_id=<InsertClientIDHere>&scope=bot&permissions=8

---------------------------------
Dependencies:
discord
python-dotenv
psutil
pathlib
asyncio
youtube_dl
pytz
mutagen
pydub

Also needed:
ffmpeg installed on machine

---------------------------------

To run - navigate to bot's directory in cmd, then enter:
python main.py


The main.py file is always up and running, it loads various other cogs from different files
You can hot load/unload extensions with the !load <extension> or !unload <extension> or !reload <extension> commands
!restart will restart the whole bot

All other commands are inside extensions
The list of extensions which are auto loaded/unloaded is inside main.py (maybe i should move that out so it can be edited without requiring a restart oh well)

Theoretically will add more to this later