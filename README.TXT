Buttery Biscuit Bot! This time in Python.

Add to a server (*should* be public, lmk if not):
https://discordapp.com/oauth2/authorize?client_id=<InsertClientIDHere>&scope=bot&permissions=8

---------------------------------
Dependencies (can add flag '-U' = upgrade, which will replace previous versions if any are installed): 

FFMPEG - https://github.com/adaptlearning/adapt_authoring/wiki/Installing-FFmpeg
^Make sure that FFmpeg is included in the environment path for the system!

Assuming you have a recent edition of python it'll come bundled with pip, so you'll want to install the following libraries with these commands:
pip install discord-py
pip install discord.py[voice]
pip install python-dotenv

---------------------------------

To run - navigate to bot's directory in cmd, then enter:
python main.py


The main.py file is always up and running, it loads various other cogs from different files
You can hot load/unload extensions with the !load <extension> or !unload <extension> or !reload <extension> commands
!restart will restart the whole bot

All other commands are inside extensions
The list of extensions which are auto loaded/unloaded is inside main.py (maybe i should move that out so it can be edited without requiring a restart oh well)

Theoretically will add more to this later