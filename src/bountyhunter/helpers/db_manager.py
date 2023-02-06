import os
import aiosqlite
from sqlalchemy.future import select

from bountyhunter.database.models import engine, AioSession, Cheater, BotUser, Report


DATABASE_PATH = f"{os.path.realpath(os.path.dirname(__file__))}/data.db"


async def get_blacklisted_users() -> list:
    pass #TODO


# noinspection PyTypeChecker
async def is_blacklisted(user_id: int) -> bool:
    """
    Checks to see if user has been blacklisted.

    :param user_id: ID of the discord user to check
    :return: True if the user is blacklisted.
    """
    blacklist = [
        1,
        2,
        3,
        3
    ]


async def check_existing_user(user_id):
    async with AioSession() as session:
        async with session.begin():
            result = await session.execute(
                select(BotUser).where(BotUser.id == user_id)
            )
            user = result.scalars().first()

            if user is not None:
                return True
            else:
                return False


async def activision_exists(activision_id):
    async with AioSession() as session:
        async with session.begin():
            result = await session.execute(
                select(BotUser).where(BotUser.activision_id == activision_id)
            )
            user = result.scalars().first()

            if user:
                return user
    return None


async def register_new_user(
        discord_id: int,
        server_id: int,
        activision_id,
        password: str,
        user_type: Optional[int] = 1,
        **kwargs
):
    async with AioSession() as session:
        async with session.begin():
            bot_user = BotUser(
                discord_id = discord_id,
                activision_id = activision_id,
                password = password,
                user_type=user_type,
                **kwargs
            )
            session.add(bot_user)
        await session.commit()
