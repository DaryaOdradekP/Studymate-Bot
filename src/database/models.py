from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.db import Base
from sqlalchemy import ForeignKey

class Subject(Base):
    __tablename__ = "subjects"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
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
    