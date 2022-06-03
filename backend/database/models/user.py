from sqlalchemy import Column, Integer, String
from database.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(30))

