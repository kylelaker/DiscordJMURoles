from typing import List
import yaml

from discord.ext.commands import NotOwner
from yaml.error import YAMLError

CONFIG_LOCATION = "config.yml"
_CONFIG_DATA = {}


def bot_owners() -> List[int]:
    """
    Provides the list of bot owners from the config.
    """
    return list(_CONFIG_DATA.get('owners', []))


def secret_token() -> str:
    return _CONFIG_DATA['secret_token']


def is_bot_owner(ctx) -> bool:
    """
    Check whether the message author is also a bot owner.

    This is similar to the built-in is_owner(); however, it allows for multiple
    owners.
    """
    if ctx.author.id not in bot_owners():
        raise NotOwner()
    return True

# Load the config if it hasn't been done already.
if not _CONFIG_DATA:
    try:
        with open(CONFIG_LOCATION) as config_file:
            _CONFIG_DATA.update(yaml.safe_load(config_file))
    except IOError as io_err:
        print(f"The configuration must be placed at {CONFIG_LOCATION}.")
    except YAMLError as yaml_err:
        print(f"Invald configuration: {yaml_err}")