import json
from typing import List
import sqlalchemy as db
from sqlalchemy import Integer, Boolean, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from config import Session
from datetime import datetime


class Base(DeclarativeBase):
    pass


class CRUD:
    id = None

    def save(self, session):
        if self.id is None:
            session.add(self)
        return session.commit()

    def destroy(self, session):
        session.delete(self)
        return session.commit()


class User(Base, CRUD):
    __tablename__ = "user_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int] = mapped_column(Integer())

    '''messages: Mapped[List["Record"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )'''


class Document(Base, CRUD):
    __tablename__ = "document_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(100000))
    text_embedding: Mapped[str] = mapped_column(String(100000))
