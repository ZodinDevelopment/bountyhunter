from discord.ext import commands
from discord.ext.commands import Context


from bountyhunter.helpers import checks  # TODO


class Template(commands.Cog, name="template"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="testcommand",
        description="A test command that does nothing."
    )
    @checks.not_blacklisted()  # TODO
    async def testcommand(self, context: Context):
        """
        This is a test command taht does nothing.

        :param context: The command context
        """
        await context.send("Hooray, the command worked!")


async def setup(bot):
    await bot.add_cog(Template(bot))
