import datetime
import uuid
import random

from sqlalchemy import Integer, String, DateTime, Uuid
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


class Image(Base):
    __tablename__ = "image"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    path: Mapped[str] = mapped_column(String(30))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self) -> str:
        return f"Image(id={self.id!r}, path={self.path!r})"
    
    @classmethod
    def create(cls, path: str = ''):
        return cls(path=path)
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns if not isinstance(getattr(self, c.name), datetime.datetime)}
