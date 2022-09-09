from collections import UserList
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Sequence
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from setting import ENGINE, Base
from datetime import datetime
from uuid import uuid4
import sys


class User(Base):
    __tablename__ = "user"
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    email_address = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    loanItem = relationship("LoanItem", backref="user")

class Category(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    item = relationship("Item", backref="category")

class Manufacture(Base):
    __tablename__ = "manufacture"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    item = relationship("Item", backref="manufacture")

class Mount(Base):
    __tablename__ = "mount"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    item = relationship("Item", backref="mount")

class Item(Base):
    __tablename__ = "item"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)  
    is_consumable = Column(Boolean, nullable=False)
    category_id = Column(Integer, ForeignKey("category.id"), nullable=False)
    manufacture_id = Column(Integer, ForeignKey("manufacture.id"), nullable=False)
    mount_id = Column(Integer, ForeignKey("mount.id"), nullable=False)
    release_date = Column(DateTime)
    loanItem = relationship("LoanItem", backref="item")

class LoanItem(Base):
    __tablename__ = "loan_item"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_uuid = Column(UUID(as_uuid=True), ForeignKey("user.uuid"), nullable=False)
    item_id = Column(Integer, ForeignKey("item.id"), nullable=False)
    loan_date = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime)
    return_date = Column(DateTime)

def main(args):
    Base.metadata.create_all(bind=ENGINE)


if __name__ == "__main__":
    main(sys.argv)