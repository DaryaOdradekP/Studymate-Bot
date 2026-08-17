import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database.db import Base
from src.database.models import Subject, Task
from src.database import tasks


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)

    TestingSessionLocal = sessionmaker(bind=engine)
    test_session = TestingSessionLocal()

    original_session_local = tasks.SessionLocal
    tasks.SessionLocal = TestingSessionLocal

    yield test_session

    test_session.close()
    tasks.SessionLocal = original_session_local


def test_task_exists_returns_true_for_existing_task(session):
    subject = Subject(
        name="Math",
        user_id=1,
    )

    session.add(subject)
    session.commit()

    task = Task(
        title="Homework",
        subject_id=subject.id,
    )

    session.add(task)
    session.commit()

    assert tasks.task_exists("Math", "Homework", 1) is True


def test_task_exists_returns_false_for_missing_task(session):
    subject = Subject(
        name="Math",
        user_id=1,
    )

    session.add(subject)
    session.commit()

    assert tasks.task_exists("Math", "Homework", 1) is False


def test_task_exists_returns_false_for_task_in_another_subject(session):
    math = Subject(
        name="Math",
        user_id=1,
    )

    history = Subject(
        name="History",
        user_id=1,
    )

    session.add_all([math, history])
    session.commit()

    task = Task(
        title="Homework",
        subject_id=math.id,
    )

    session.add(task)
    session.commit()

    assert tasks.task_exists("History", "Homework", 1) is False


def test_task_exists_returns_false_for_another_user(session):
    subject = Subject(
        name="Math",
        user_id=1,
    )

    session.add(subject)
    session.commit()

    task = Task(
        title="Homework",
        subject_id=subject.id,
    )

    session.add(task)
    session.commit()

    assert tasks.task_exists("Math", "Homework", 2) is False
