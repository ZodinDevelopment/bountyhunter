from typing import Optional

from datetime import datetime

from sqlalchemy import Column, Integer, BigInteger, String, DateTime, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import relationship, sessionmaker


Base = declarative_base()


class Cheater(Base):
    __tablename__ = "cheater"
    id = Column(Integer, primary_key=True)
    activision_id = Column(String(32), index=True, unique=True)
    discord_id = Column(BigInteger, nullable=True)
    first_incident = Column(DateTime, index=True)
    reports = relationship("Report", back_populates="cheater")

    def __init__(self, activision_id: str, discord_id: Optional[int]):
        self.activision_id = activision_id
        self.discord_id = discord_id
        self.first_incident = datetime.utcnow()


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
    cheater = relationship("Cheater", back_popoulates="reports")

    def __init__(
            self,
            *,
            report_message_id: int,
            server_id: int,
            suspect_activision: str,
            platform: Literal["Playstation", "Xbox", "Battle.net"],
            reporter: BotUser,
            description: Optional[str],
            cheater: Optional[Cheater]
    ):
        self.id = report_message_id
        self.sever_id = server_id

