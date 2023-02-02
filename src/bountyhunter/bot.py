import asyncio
import json
import logging
import asyncio
import os
import platform
import random
import sys

import discord
from discord.ext import commands, tasks
from discord.ext.commands import Bot, Context

import bountyhunter.exceptions as exceptions
from bountyhunter.config import initial_config


RED = 0xE02B2B
error_warning = "A command error was raised! This error hasn't been handled properly in this project!"


if len(sys.argv) < 2:
    sys.exit("Please provide path to config file as an argument!")

else:
    config_path = str(sys.argv[1])
    if os.path.isfile(config_path):
        print("Using defaults found in .env file to initialize config.json file, since it doesn't exist yet. Overwriting file")
        try:

            config = initial_config(os.path.dirname(config_path))
        except Exception as e:
            print(str(e))
            sys.exit("Could not initialize config.json")
    elif os.path.isdir(config_path):
        print("Saving config file as 'bot_config.json' at the path you specified.")
        try:
            config = initial_config(os.path.dirname(config_path))

        except Exception as e:
            print(str(e))
            sys.exit("Could not initialize config.json file.")

    else:
        sys.exit("Fatal Error line 45")


intents = discord.Intents.default()
intents.message_content = True
intents.members = True


bot = Bot(
    command_prefix=commands.when_mentioned_or(config['prefix']),
    intents=intents,
    help_command=None
)

class LoggingFormatter(logging.Formatter):
    # Colors
    black = "\x1b[30m"
    red = "\x1b[31m"
    green = "\x1b[32m"
    yellow = "\x1b[33m"
    blue = "\x1b[34m"
    gray = "\x1b[38m"
    # Styles
    reset = "\x1b[0m"
    bold = "\x1b[1m"

    COLORS = {
        logging.DEBUG: gray + bold,
        logging.INFO: blue + bold,
        logging.WARNING: yellow + bold,
        logging.ERROR: red,
        logging.CRITICAL: red + bold
    }

    def format(self, record):
        log_color = self.COLORS[record.levelno]
        format = "(black){asctime}(reset) (levelcolor){levelname:<8}(reset) (green){name}(reset) {message}"
        format = format.replace("(black)", self.black + self.bold)
        format = format.replace("(reset)", self.reset)
        format = format.replace("(levelcolor)", log_color)
        format = format.replace("(green)", self.green + self.bold)
        formatter = logging.Formatter(format, "%Y-%m-%d %H:%M:%S", style="{")
        return formatter.format(record)
logger = logging.getLogger("discord_bot")
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setFormatter(LoggingFormatter())

file_handler = logging.FileHandler(
    filename="discord.log",
    encoding="utf-8",
    mode="w"
)
file_handler_formatter = logging.Formatter(
    "[{asctime}] [{levelname:<8}] {name}: {message}", "%Y-%m-%d %H:%M:%S", style="{"
)
file_handler.setFormatter(file_handler_formatter)


logger.addHandler(console_handler)
logger.addHandler(file_handler)
bot.logger = logger


async def init_db():
    pass


bot.config = config


@bot.event
async def on_ready() -> None:
    """
    The code in this event executes when bot is finished starting up.
    """
    bot.logger.info(f"Logged in as {bot.user.name}")
    bot.logger.info(f"discord.py API version: {discord.__version__}")
    bot.logger.info(f"Python version: {platform.python_version()}")
    bot.logger.info(
    f"Running on: {platform.system()} {platform.release()} ({os.name})"
    )
    bot.logger.info("-----------------")
    status_task.start()
    if config['sync_commands_globally']:
        bot.logger.info("Syncing commands globally...")
        await bot.tree.sync()


@tasks.loop(minutes=1.0)
async def status_task() -> None:
    """
    Randomly change the bot's presence
    """
    statuses = ["Playing CoD", "Chillin", "Panic Attack"]
    await bot.change_presence(activity=discord.Game(random.choice(statuses)))


@bot.event
async def on_message(message: discord.Message) -> None:
    """
    Called everytime a message is sent by anyone

    :param message: The message that ws sent
    """
    if message.author == bot.user or message.author.bot:
        return

    await bot.process_commands(message)


@bot.event
async def on_command_completion(context: Context) -> None:
    """
    Gets called everytime a command is successfully executed.

    :param context: The command context.
    """
    full_command_name = context.command.qualified_name
    split = full_command_name.split(" ")
    executed_command = str(split[0])
    if context.guild is not None:
        bot.logger.info(
            f"Executed {executed_command} in {context.guild.name} (ID: {context.guild.id}) by {context.author} (ID: {context.author.id})"
        )
    else:
        bot.logger.info(
            f"Executed {executed_command} by {context.author} (ID: {context.author.id}"
        )


@bot.event
async def on_command_error(context: Context, error) -> None:
    """
    This executes everytime a command fails and raises and error

    :param context: The command context.
    :param error: The error it raised.
    """
    default_embed = discord.Embed(
        description="This error is not properly handled yet. Check the logs for details.",
        color=RED
    )
    if isinstance(error, commands.CommandOnCooldown):
        # TODO
        embed = default_embed
        embed.title = "Cooldown"
        await context.send(embed=embed)
        bot.logger.warning(error_warning)
        bot.logger.error(str(error))
    elif isinstance(error, exceptions.UserBlackListed):
        # TODO
        embed = default_embed
        embed.title = "Blacklisted"
        await context.send(embed=embed)
        bot.logger.warning(error_warning)
        bot.logger.error(str(error))

    elif isinstance(error, exceptions.UserNotOwner):
        # TODO
        embed = default_embed
        embed.title = "Not Owner"
        await context.send(embed=embed)
        bot.logger.warning(error_warning)
        bot.logger.error(str(error))
        await context.send(embed=embed)
        bot.logger.error(str(error))

    elif isinstance(error, commands.MissingPermissions):
        # TODO
        embed = default_embed
        embed.title = "Permisssions"
        await context.send(embed=embed)
        bot.logger.warning(error_warning)
        bot.logger.error(str(error))

    elif isinstance(error, commands.BotMissingPermissions):
        # TODO
        embed = default_embed
        embed.title = "Bot Permissions"
        await context.send(embed=embed)
        bot.logger.warning(error_warning)
        bot.logger.error(str(error))

    elif isinstance(error, commands.MissingRequiredArgument):
        # TODO
        embed = default_embed
        embed.title = "Missing Argument(s)"
        await context.send(embed=embed)
        bot.logger.warning(error_warning)
        bot.logger.error(str(error))
    else:
        raise error


async def load_cogs() -> None:
    for file in os.listdir(f"{os.path.realpath(os.path.dirname(__file__))}/cogs"):
        if file.endswith(".py"):
            extension = file[:-3]
            try:
                await bot.load_extension(f"cogs.{extension}")
                bot.logger.info(f"Loaded extension '{extension}'")

            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                bot.logger.error(
                    f"failed to load extension '{extension}'\n{exception}"
                )


if __name__ == "__main__":
    asyncio.run(load_cogs())
    bot.run(config['token'])