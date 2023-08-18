import datetime
import uuid
from uuid import UUID, uuid4

from sqlalchemy import DateTime, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


class Image(Base):
    __tablename__ = "image"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    path: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())

    def __repr__(self) -> str:
        return f"Image(id={self.id!r}, path={self.path!r})"

    @classmethod
    def create(cls, base_path: str = ''):
        image_id = uuid.uuid4()
        path = f'{base_path}/{image_id}.jpg'
        return cls(id=image_id, path=path)
