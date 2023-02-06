import discord
from discord.ext import commands
from discord.ext.commands import Context

from bountyhunter.helpers import checks
from bountyhunter.helpers import db_manager
from bountyhunter.bot import RED
from bountyhunter import exceptions

class Hunter(commands.Cog, name="hunter"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="register",
        description="Begins the registration workflow for a new user of the bot."
    )
    @checks.not_blacklisted()
    @checks.already_registered()
    async def register(self, context: Context, *, activision_id: str):
        """
        Begins the registration workflow, this is basically a way to have some level of governance and accountability.

        :param context: The context of the command.
        :param activision_id: Activision Username

        :return:
        """
        '''
        if db_manager.user_with_activision_id is not None:
            embed = discord.Embed(
                description=f"Uh oh, looks like you've already registered with this activision id (or someone has.) If this was not you please, file a report.",
                color=RED
            )
            await context.send(embed=embed)
            raise exceptions.ActivisionIdConflict
        '''
        existing_user = await db_manager.activision_exists(activision_id)
        if existing_user is not None:
            embed = discord.Embed(
                description=f"Uh oh, looks like you've already registered with this activision id. If this wasn't you, please contact the moderators.",
                color=RED
            )
            bot.logger.warning(f"{context.author} (ID: {context.author.id}) tried to register with an activision ({activision_id} but it's already registered to a user with ID {existing_user.id}")
            await context.send(embed=embed)
            return

        # embed = discord.Embed(
        #     title="Under Construction",
        #     description="This command is currently under construction, but this is to confirm that it is functioning!"
        # )

        await context.send(embed=embed)
        return


async def setup(bot):
    await bot.add_cog(Hunter(bot))