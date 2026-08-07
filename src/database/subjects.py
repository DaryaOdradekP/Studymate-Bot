from sqlalchemy import select

from src.database.db import SessionLocal
from src.database.models import Subject

def add_subject(name: str):
    session = SessionLocal()

    statement = select(Subject).where(Subject.name == name)

    result = session.execute(statement)

    existing_subject = result.scalar_one_or_none()

    if existing_subject is not None:
        session.close()
        return False

    session.add(subject)
    session.commit()
    session.close()

    return True


def get_subjects():
    session = SessionLocal()

    statement = select(Subject)

    result = session.execute(statement)

    subjects = result.scalars().all()

    session.close()

    return subjects


def delete_subject(name: str):
    session = SessionLocal()

    statement = select(Subject).where(Subject.name == name)

    result = session.execute(statement)

    subject = result.scalar_one_or_none()

    if subject is None:
        session.close()
        return False

    session.delete(subject)
    session.commit()
    session.close()

    return True
