from sqlalchemy import select

from src.database.db import SessionLocal
from src.database.models import Subject, Task


def add_subject(name: str, user_id: int):
    with SessionLocal() as session:
        statement = select(Subject).where(
            Subject.name == name,
            Subject.user_id == user_id,
        )

        result = session.execute(statement)
        existing_subject = result.scalar_one_or_none()

        if existing_subject is not None:
            return False

        subject = Subject(
            name=name,
            user_id=user_id,
        )

        session.add(subject)
        session.commit()

        return True


def get_subjects(user_id: int):
    with SessionLocal() as session:
        statement = select(Subject).where(
            Subject.user_id == user_id
        )

        result = session.execute(statement)
        subjects = result.scalars().all()

        return subjects


def subject_exists(name: str, user_id: int):
    with SessionLocal() as session:
        statement = select(Subject).where(
            Subject.name == name,
            Subject.user_id == user_id,
        )

        result = session.execute(statement)
        subject = result.scalar_one_or_none()

        return subject is not None


def delete_subject(name, user_id):
    with SessionLocal() as session:
        subject = session.query(Subject).filter(
            Subject.name == name,
            Subject.user_id == user_id,
        ).first()

        if not subject:
            return False

        task_exists = session.query(Task).filter(
            Task.subject_id == subject.id,
        ).first()

        if task_exists:
            return False

        session.delete(subject)
        session.commit()

        return True
