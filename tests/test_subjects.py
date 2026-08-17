import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database.db import Base
from src.database.models import Subject
from src.database import subjects


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)

    TestingSessionLocal = sessionmaker(bind=engine)
    test_session = TestingSessionLocal()

    original_session_local = subjects.SessionLocal
    subjects.SessionLocal = TestingSessionLocal

    yield test_session

    test_session.close()
    subjects.SessionLocal = original_session_local


def test_add_subject_returns_true_for_new_subject(session):
    assert subjects.add_subject("Math", 1) is True

    result = session.query(Subject).all()

    assert len(result) == 1
    assert result[0].name == "Math"
    assert result[0].user_id == 1


def test_add_subject_returns_false_for_duplicate_subject(session):
    subjects.add_subject("Math", 1)

    assert subjects.add_subject("Math", 1) is False

    result = session.query(Subject).all()

    assert len(result) == 1


def test_same_subject_can_exist_for_different_users(session):
    assert subjects.add_subject("Math", 1) is True
    assert subjects.add_subject("Math", 2) is True

    result = session.query(Subject).all()

    assert len(result) == 2


def test_get_subjects_returns_only_users_subjects(session):
    subjects.add_subject("Math", 1)
    subjects.add_subject("Physics", 1)
    subjects.add_subject("History", 2)

    result = subjects.get_subjects(1)

    names = [subject.name for subject in result]

    assert names == ["Math", "Physics"]


def test_subject_exists_returns_true_for_existing_subject(session):
    subjects.add_subject("Math", 1)

    assert subjects.subject_exists("Math", 1) is True


def test_subject_exists_returns_false_for_missing_subject(session):
    assert subjects.subject_exists("Math", 1) is False


def test_subject_exists_returns_false_for_another_user(session):
    subjects.add_subject("Math", 1)

    assert subjects.subject_exists("Math", 2) is False


def test_delete_subject_returns_true_for_existing_subject(session):
    subjects.add_subject("Math", 1)

    assert subjects.delete_subject("Math", 1) is True

    result = session.query(Subject).all()

    assert len(result) == 0


def test_delete_subject_returns_false_for_missing_subject(session):
    assert subjects.delete_subject("Math", 1) is False
    