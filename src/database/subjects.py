from sqlalchemy import select

from src.database.db import SessionLocal
from src.database.models import Subject, Task


def add_subject(name: str, user_id: int):
    session = SessionLocal()

    statement = select(Subject).where(
        Subject.name == name,
        Subject.user_id == user_id,
    )

    result = session.execute(statement)

    existing_subject = result.scalar_one_or_none()

    if existing_subject is not None:
        session.close()
        return False

    subject = Subject(
        name=name,
        user_id=user_id,
    )

    session.add(subject)
    session.commit()
    session.close()

    return True


def get_subjects(user_id: int):
    session = SessionLocal()

    statement = select(Subject).where(
        Subject.user_id == user_id
    )

    result = session.execute(statement)

    subjects = result.scalars().all()

    session.close()

    return subjects


def subject_exists(name: str, user_id: int):
    session = SessionLocal()

    statement = select(Subject).where(
        Subject.name == name,
        Subject.user_id == user_id,
    )

    result = session.execute(statement)

    subject = result.scalar_one_or_none()

    session.close()

    return subject is not None


def delete_subject(name, user_id):
    session = SessionLocal()

    subject = session.query(Subject).filter(
        Subject.name == name,
        Subject.user_id == user_id,
    ).first()

    if not subject:
        session.close()
        return False

    task_exists = session.query(Task).filter(
        Task.subject_id == subject.id,
    ).first()

    if task_exists:
        session.close()
        return False

    session.delete(subject)
    session.commit()
    session.close()

    return True
