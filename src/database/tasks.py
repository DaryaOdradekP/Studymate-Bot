from sqlalchemy import select

from src.database.db import SessionLocal
from src.database.models import Task, Subject

from sqlalchemy.orm import selectinload


def add_task(subject_name: str, title: str, description: str | None):
    session = SessionLocal()

    statement = select(Subject).where(Subject.name == subject_name)

    result = session.execute(statement)

    subject = result.scalar_one_or_none()

    if subject is None:
        session.close()
        return False
    
    statement = select(Task).where(
        Task.title == title,
        Task.subject_id == subject.id
    )

    result = session.execute(statement)

    existing_task = result.scalar_one_or_none()

    if existing_task is not None:
        session.close()
        return False

    task = Task(
        title=title,
        description=description,
        subject_id=subject.id,
    )

    session.add(task)
    session.commit()
    session.close()

    return True


def get_tasks():
    session = SessionLocal()

    statement = select(Task).options(selectinload(Task.subject))

    result = session.execute(statement)

    tasks = result.scalars().all()

    session.close()

    return tasks


def delete_task(title: str):
    session = SessionLocal()

    statement = select(Task).where(Task.title == title)

    result = session.execute(statement)

    task = result.scalar_one_or_none()

    if task is None:
        session.close()
        return False

    session.delete(task)
    session.commit()
    session.close()

    return True
