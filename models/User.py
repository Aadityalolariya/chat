from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, Text
from sqlalchemy.orm import relationship
from db import Base
from datetime import datetime


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    phone_number = Column(String(15), unique=True, nullable=False)
    password = Column(String(150), nullable=False)
    email = Column(String(80))
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50))
    display_name = Column(String(50))
    profile_picture = Column(String(150))
    description = Column(Text)
    login_status_id = Column(Integer, ForeignKey("constant.id"))
    theme_id = Column(Integer, ForeignKey("constant.id"))
    last_opene_date = Column(TIMESTAMP)
    created_on = Column(TIMESTAMP, default=datetime.utcnow)
