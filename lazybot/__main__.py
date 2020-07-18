import datetime
import logging
import os
import sys
import traceback

import discord
from discord.ext import commands

from lazybot import (
    config,
    self_updater,
    util
)
from lazybot.bot_help import StraightforwardHelp
from lazybot.commands import all_commands

# set up logger
log_filename = "discord.log"
working_dir = os.path.dirname(os.path.abspath(__file__))
log_filename = os.path.join(working_dir, log_filename)
logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename=log_filename, encoding="utf-8", mode="w")
handler.setFormatter(
    logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
)
logger.addHandler(handler)

#################
### Constants ###
#################

DEFAULT_COMMAND_PREFIX = "!"

# set up bot
description = """ A bot to fulfill your wildest dreams. """
bot = commands.Bot(
    command_prefix=DEFAULT_COMMAND_PREFIX,
    description=description,
    pm_help=False,
    help_command=StraightforwardHelp(),
)

######################
### Event handlers ###
######################


@bot.event
async def on_connect():
    print("Connected!")
    print("Username: {}".format(bot.user.name))
    print("ID: {}".format(bot.user.id))


@util.static_vars(is_first_call=True)
@bot.event
async def on_ready():
    """ Called when the bot is ready to do stuff. Can be called multiple times.
    """
    if on_ready.is_first_call:
        on_ready.is_first_call = False

        # remove a "restarting..." message to show bot has finished restarting
        last_minute = datetime.datetime.now() - datetime.timedelta(minutes=1)

        def delete_check(msg: discord.Message) -> bool:
            return msg.author == bot.user and msg.content.lower() == self_updater.RESTART_MSG.lower()

        await util.purge_in_all(bot, since=last_minute, check=delete_check)


@bot.event
async def on_command_error(ctx, exception):
    """ Logs and ignores errors in commands, unless that exception was from
        entering an invalid command, in which case this instead tells the
        user that they gave an invalid command.
    """
    if type(exception) == commands.errors.CommandNotFound:
        await ctx.send(str(exception))
    elif type(exception) == commands.errors.MissingRequiredArgument:
        await ctx.send(
            "Missing required argument. Please see '{}help'.".format(
                DEFAULT_COMMAND_PREFIX
            )
        )
    else:
        logger.error("Ignoring exception in command {}".format(ctx.command))
        print("Ignoring exception in command {}".format(ctx.command), file=sys.stderr)
        traceback.print_exception(
            type(exception), exception, exception.__traceback__, file=sys.stderr
        )


@bot.event
async def on_member_join(member):
    # give a message on join
    await member.send(
        "How goes it <@{id}>?\n\n".format(id=member.id)
        + "You can use '!gradyear <year>' if you would like to set your grad year."
        + " Use '!help' for more commands"
    )


################
### Commands ###
################

bot.add_cog(self_updater.UpdateChecker(bot))
for command in all_commands():
    bot.add_cog(command(bot))


print()
print("connecting...")
bot.run(config.secret_token())

# finally, after event loop terminated
self_updater.restart(logger)
