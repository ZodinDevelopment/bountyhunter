from discord.ext import commands



class UserBlackListed(commands.CheckFailure):
    def __init__(self, message="User is blacklisted."):
        self.message = message
        super().__init__(self.message)



class UserNotOwner(commands.CheckFailure):
    def __init__(self, message="User is not owner."):
        self.message = message
        super().__init__(self.message)

