from typing import Optional, Literal

import hashlib
from datetime import datetime

from sqlalchemy import Column, Integer, BigInteger, String, DateTime, Float, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.future import select


Base = declarative_base()
engine = create_async_engine(
    "sqlite+aiosqlite:///data.db"
)
AioSession = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base.metadata.bind = engine
AioSession.configure(bind=engine)


class Cheater(Base):
    __tablename__ = "cheater"
    id = Column(Integer, primary_key=True)
    activision_id = Column(String(32), index=True, unique=True)
    discord_id = Column(BigInteger, nullable=True)
    first_incident = Column(DateTime, index=True)
    reports = relationship("Report", back_populates="cheater")

    def __init__(self, *, activision_id: str, discord_id: Optional[int]):
        self.activision_id = activision_id
        self.discord_id = discord_id
        self.first_incident = datetime.utcnow()




class BotUser(Base):
    __tablename__ = "bot_user"
    id = Column(BigInteger, primary_key=True, autoincrement=False)
    activision_id = Column(String(32), index=True, unique=True)
    twitter_handle = Column(String(64), nullable=True)
    cmg_handle = Column(String(64), unique=True, nullable=True)
    gb_handle = Column(String(64), unique=True, nullable=True)
    server_id = Column(BigInteger)
    joined_at = Column(DateTime)
    password_hash = Column(String(128))
    user_type = Column(Integer, default=1)  # 1: reg user  2: Trustbase user  3: mod  4: Admin

    bounty_score = Column(Float, default=100.0)
    current_bounty = Column(Float, default=0.0)
    mailing_list = Column(Boolean, default=False)
    reports = relationship("Report", back_populates="reporter")

    def __init__(
            self,
            discord_id: int,
            activision_id: str,
            server_id: int,
            password: str,
            twitter_handle: Optional[str],
            cmg_handle: Optional[str],
            gb_handle: Optional[str],
            user_type: Optional[int] = 1
    ):
        self.id = discord_id
        self.activision_id = activision_id
        self.server_id = server_id
        self.password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        self.twitter_handle = twitter_handle
        self.cmg_handle = cmg_handle
        self.gb_handle = gb_handle
        self.user_type = user_type

        self.joined_at = datetime.utcnow()


class Report(Base):
    __tablename__ = "report"
    id = Column(BigInteger, primary_key=True, autoincrement=False)  # Is id of message that made report
    timestamp = Column(DateTime, index=True)
    server_id = Column(BigInteger, index=True)

    vouchers = Column(Integer, default=0)
    disputes = Column(Integer, default=0)

    description = Column(String(256))

    suspect_activision = Column(String(32), index=True)
    platform = Column(String(32))

    reporter_id = Column(ForeignKey("bot_user.id"))
    reporter = relationship("BotUser", back_populates="reports")

    cheater_id = Column(ForeignKey("cheater.id"))
    cheater = relationship("Cheater", back_populates="reports")

    def __init__(
            self,
            *,
            report_message_id: int,
            report_message_timestamp: datetime,
            server_id: int,
            suspect_activision: str,
            platform: Literal["Playstation", "Xbox", "Battle.net"],
            reporter: BotUser,
            description: Optional[str],
            cheater: Optional[Cheater]
    ):
        self.id = report_message_id
        self.timestamp = report_message_timestamp
        self.server_id = server_id
        self.platform =  platform
        self.reporter = reporter
        self.description = description
        self.suspect_activision = suspect_activision
        if cheater is None:
            cheater = init_or_fetch_cheater(suspect_activision)
        self.cheater = cheater



async def connect_db():
    """
    Create the tables and columns if they don't exist. Creates .db file as well.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    await engine.dispose()


async def init_or_fetch_cheater(activision_id: str):
    async with AioSession() as session:
        async with session.begin():
            result = await session.execute(
                select(Cheater).where(Cheater.activision_id == activision_id)

            )
            cheater = result.scalars().first()
            if cheater is None:
                cheater = Cheater(activision_id=activision_id)
                session.add(cheater)

        await session.commit()


if __name__ == "__main__":
    import asyncio
    asyncio.run(connect_db())
    print("Database connection established.")