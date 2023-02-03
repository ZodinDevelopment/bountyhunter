import discord
from discord.ext import commands



class UserBlackListed(commands.CheckFailure):
    def __init__(self, message="User is blacklisted."):
        self.message = message
        super().__init__(self.message)



class UserNotOwner(commands.CheckFailure):
    def __init__(self, message="User is not owner."):
        self.message = message
        super().__init__(self.message)


class UserAlreadyRegistered(commands.CheckFailure):
    def __init__(self, message="User is already registered with that id!"):
        self.message = message
        super().__init__(self.message)


class ActivisionIdConflict(discord.DiscordException):
    def __init__(self, message="There is a conflict with that Activision ID, multiple are claiming to own the name!"):
        self.message = message
        super().__init__(self.message)