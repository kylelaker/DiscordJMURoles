# LazyBot
A Discord bot for helping change roles in JMU Grad Discord

## Installation Requirements:
1. Python 3.7 or greater
1. Git

### Running
1. Install the bot by running `pip install -e .`
1. Create a configuration file, named `config.yml`. See `sample_config.yml` for an example.
1. Run `python -m lazybot.py`

## Developers
### Creating Commands
For an example of a set of created commands, see commands in lazybot/commands/MiscFun.py.

To begin to add a command, add a new or edit an existing class (like MiscFun) inheriting from discord.ext.commands.Cog, and put commands inside it. The doc comments for your function (command) are the command's help message, and the name of the your function is by default the name of the command (see docs linked in [Rapptz/discord.py](https://github.com/Rapptz/discord.py) for more info).
