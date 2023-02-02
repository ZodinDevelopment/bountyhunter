import os
import aiosqlite


DATABASE_PATH = f"{os.path.realpath(os.path.dirname(__file__))}/../database/database.db"


async def get_blacklisted_users() -> list:
    pass #TODO


async def is_blacklisted(user_id: int) -> bool:
    """
    Checks to see if user has been blacklisted.

    :param user_id: Id of the discord user to check
    :return: True if the user is blacklisted.
    """
    blacklist = [
        1,
        2,
        3,
        3
    ]