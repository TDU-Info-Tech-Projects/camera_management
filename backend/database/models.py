from dataclasses import dataclass
from typing import Any
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database import engine, Base
from datetime import datetime
from uuid import uuid4
import sys


@dataclass
class User(Base):
    __tablename__ = "users"
    email_address: Any
    password_hash: Any
    password_salt: Any
    first_name: Any
    last_name: Any

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    email_address = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    password_salt = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    rentItem = relationship("RentItem", backref="users")

# class Category(Base):
#     __tablename__ = "category"
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String, nullable=False,  unique=True)
#     item = relationship("Item", backref="category")

# class Manufacture(Base):
#     __tablename__ = "manufacture"
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String, nullable=False,  unique=True)
#     item = relationship("Item", backref="manufacture")

@dataclass
class Mount(Base):
    __tablename__ = "mounts"
    name: Any

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False,  unique=True)
    item = relationship("Item", backref="mounts")

@dataclass
class Item(Base):
    __tablename__ = "items"
    id: Any
    name: Any
    image_url: Any
    stock: Any
    is_consumable: Any
    is_lens: Any
    mount_id: Any
    release: Any

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False,  unique=True)
    image_url = Column(String, nullable=False)
    stock = Column(Integer, default=1, nullable=False)
    is_consumable = Column(Boolean, nullable=False)
    is_lens=Column(Boolean, nullable=False)
    # category_id = Column(Integer, ForeignKey("category.id"), nullable=False)
    # manufacture_id = Column(Integer, ForeignKey("manufacture.id"), nullable=False)
    mount_id = Column(Integer, ForeignKey("mounts.id"), nullable=False)
    release = Column(DateTime)
    rentItem = relationship("RentItem", backref="items")

@dataclass
class RentItem(Base):
    __tablename__ = "loan_items"
    id: Any
    user_id: Any
    item_id: Any
    loan_date: Any
    due_date: Any
    return_date: Any

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    loan_date = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime)
    return_date = Column(DateTime)

def main(args):
    print(Base.metadata.tables)
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    main(sys.argv)