from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.db import Base
from sqlalchemy import ForeignKey

from datetime import date
from sqlalchemy import Date

class Subject(Base):
    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    user_id: Mapped[int] = mapped_column(nullable=False)

    tasks: Mapped[list["Task"]] = relationship(back_populates="subject")

class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(1000), nullable=True)
    subject_id: Mapped[int] = mapped_column(
        ForeignKey("subjects.id"),
        nullable=False
    )
    subject: Mapped["Subject"] = relationship(back_populates="tasks")
    deadline: Mapped[date | None] = mapped_column(Date, nullable=True)
    completed: Mapped[bool] = mapped_column(default=False)


class UserSettings(Base):
    __tablename__ = "user_settings"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(unique=True, nullable=False)
    notifications_enabled: Mapped[bool] = mapped_column(
        default=True,
        nullable=False,
    )
    