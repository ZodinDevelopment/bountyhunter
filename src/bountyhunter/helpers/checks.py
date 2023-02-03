import json
import os
from typing import Callable, TypeVar

from discord.ext import commands

from bountyhunter.exceptions import *
from bountyhunter.helpers import db_manager # TODO


T = TypeVar("T")


def is_owner() -> Callable[[T], T]:
    async def predicate(context: commands.Context) -> bool:
        with open(f"{os.path.realpath(os.path.dirname(__file__))}/../config.json", 'r') as file:
            data = json.load(file)
        if context.author.id not in data['owners']:
            raise UserNotOwner
        return True

    return commands.check(predicate)


def not_blacklisted() -> Callable[[T], T]:
    async def predicate(context: commands.Context) -> bool:
        if await db_manager.is_blacklisted(context.author.id):
            raise UserBlackListed
        return True

    return commands.check(predicate)


def already_registered() -> Callable[[T], T]:
    async def predicate(context: commands.Context) -> bool:
        if await db_manager.check_existing_user(context.author.id):
            raise UserAlreadyRegistered
        return True

    return commands.check(predicate)