from sqlalchemy import (
    Column,
    Integer,
    String
)


#СЛИТ В https://t.me/end_soft
from utils.database import Base


class Sessions(Base):
    __tablename__ = 'sessions'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True)
    phone = Column(String)
    password = Column(String)
