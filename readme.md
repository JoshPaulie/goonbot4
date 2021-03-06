# Goonbot 4

![logo](https://media.discordapp.net/attachments/787711120026501152/933826376207847504/IMG_0355.png)

## Authors Note

I've learned a ton between this rewrite and now, just a few short months later. I will be doing a major refactor (again) in the coming months.

Fatal flaws of current generation:
- I didn't specify versions in my requirements.txt, resulting in breakage on new machines
- The project structure itself is messy and could be cleaned up by making the bot a proper package with `__init__.py` and `__main__.py`
- Not all third party packages are async, resulting in hangups and unexpected behavior

## About

🧰 GB4 is a small *swiss army knife* bot for my private discord. It's written using the "new" [PyCord]("https://github.com/Pycord-Development/pycord") library.

Feel free to copy and paste any of the code to make your own bot, or use the discussions tab for questions about making your own Discord bot with Pycord.

## Install

GB4 isn't made with other servers in mind, but is totally deployable. Repo is public for others to reference, local contributions/issues, and external help.

📂 If you are making a copy for whatever reason...
* `git clone https://github.com/JoshPaulie/goonbot4.git`
* rename .env.example -> .env
  * fill in relevant API keys
* add your server/guild in config.py
  * You can do this by _removing_ my private guilds from the all_servers list and _adding_ your own server(s).

## Special thanks / packages used 
- [Pycord](https://github.com/Pycord-Development/pycord) Discord API
- [Python-YouTube](https://github.com/sns-sdks/python-youtube) YouTube API
- [Twitch-Python](https://github.com/PetterKraabol/Twitch-Python) Twitch.tv API
- [Cassiopeia](https://github.com/meraki-analytics/cassiopeia) League of Legends API
- [Rich](https://github.com/Textualize/rich) Pretty console, logging, debugging
