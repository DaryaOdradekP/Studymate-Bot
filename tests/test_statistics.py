import sys
from pathlib import Path
from datetime import date

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database.db import Base
from src.database.models import Subject, Task
from src.database import statistics, subjects, tasks


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)

    TestingSessionLocal = sessionmaker(bind=engine)
    test_session = TestingSessionLocal()

    original_subjects_session_local = subjects.SessionLocal
    original_tasks_session_local = tasks.SessionLocal

    subjects.SessionLocal = TestingSessionLocal
    tasks.SessionLocal = TestingSessionLocal

    yield test_session

    test_session.close()

    subjects.SessionLocal = original_subjects_session_local
    tasks.SessionLocal = original_tasks_session_local


def test_get_statistics_returns_total_subjects_and_tasks(session):
    math = Subject(name="Math", user_id=1)
    history = Subject(name="History", user_id=1)

    session.add_all([math, history])
    session.commit()

    session.add_all([
        Task(title="Math homework", subject_id=math.id),
        Task(title="Math project", subject_id=math.id),
        Task(title="History essay", subject_id=history.id),
    ])
    session.commit()

    result = statistics.get_statistics(1)

    assert result["total_subjects"] == 2
    assert result["total_tasks"] == 3


def test_get_statistics_counts_completed_and_remaining_tasks(session):
    subject = Subject(name="Math", user_id=1)
    session.add(subject)
    session.commit()

    session.add_all([
        Task(
            title="Completed 1",
            subject_id=subject.id,
            completed=True,
        ),
        Task(
            title="Completed 2",
            subject_id=subject.id,
            completed=True,
        ),
        Task(
            title="Incomplete",
            subject_id=subject.id,
            completed=False,
        ),
    ])
    session.commit()

    result = statistics.get_statistics(1)

    assert result["completed_tasks"] == 2
    assert result["remaining_tasks"] == 1


def test_get_statistics_counts_tasks_with_and_without_deadline(session):
    subject = Subject(name="Math", user_id=1)
    session.add(subject)
    session.commit()

    session.add_all([
        Task(
            title="With deadline 1",
            subject_id=subject.id,
            deadline=date(2026, 9, 1),
        ),
        Task(
            title="With deadline 2",
            subject_id=subject.id,
            deadline=date(2026, 10, 1),
        ),
        Task(
            title="Without deadline",
            subject_id=subject.id,
            deadline=None,
        ),
    ])
    session.commit()

    result = statistics.get_statistics(1)

    assert result["tasks_with_deadline"] == 2
    assert result["tasks_without_deadline"] == 1


def test_get_statistics_counts_overdue_tasks(session):
    subject = Subject(name="Math", user_id=1)
    session.add(subject)
    session.commit()

    session.add_all([
        Task(
            title="Overdue",
            subject_id=subject.id,
            deadline=date(2026, 1, 1),
            completed=False,
        ),
        Task(
            title="Completed overdue",
            subject_id=subject.id,
            deadline=date(2026, 1, 1),
            completed=True,
        ),
        Task(
            title="Future",
            subject_id=subject.id,
            deadline=date(2030, 1, 1),
            completed=False,
        ),
        Task(
            title="No deadline",
            subject_id=subject.id,
            deadline=None,
            completed=False,
        ),
    ])
    session.commit()

    result = statistics.get_statistics(1)

    assert result["overdue_tasks"] == 1


def test_get_statistics_calculates_completion_rate(session):
    subject = Subject(name="Math", user_id=1)
    session.add(subject)
    session.commit()

    session.add_all([
        Task(
            title="Completed 1",
            subject_id=subject.id,
            completed=True,
        ),
        Task(
            title="Completed 2",
            subject_id=subject.id,
            completed=True,
        ),
        Task(
            title="Incomplete 1",
            subject_id=subject.id,
            completed=False,
        ),
        Task(
            title="Incomplete 2",
            subject_id=subject.id,
            completed=False,
        ),
    ])
    session.commit()

    result = statistics.get_statistics(1)

    assert result["completion_rate"] == 50


def test_get_statistics_rounds_completion_rate(session):
    subject = Subject(name="Math", user_id=1)
    session.add(subject)
    session.commit()

    session.add_all([
        Task(
            title="Completed",
            subject_id=subject.id,
            completed=True,
        ),
        Task(
            title="Incomplete 1",
            subject_id=subject.id,
            completed=False,
        ),
        Task(
            title="Incomplete 2",
            subject_id=subject.id,
            completed=False,
        ),
    ])
    session.commit()

    result = statistics.get_statistics(1)

    assert result["completion_rate"] == 33


def test_get_statistics_counts_tasks_by_subject(session):
    math = Subject(name="Math", user_id=1)
    history = Subject(name="History", user_id=1)
    physics = Subject(name="Physics", user_id=1)

    session.add_all([math, history, physics])
    session.commit()

    session.add_all([
        Task(title="Math 1", subject_id=math.id),
        Task(title="Math 2", subject_id=math.id),
        Task(title="Math 3", subject_id=math.id),
        Task(title="History 1", subject_id=history.id),
        Task(title="Physics 1", subject_id=physics.id),
        Task(title="Physics 2", subject_id=physics.id),
    ])
    session.commit()

    result = statistics.get_statistics(1)

    assert result["tasks_by_subject"] == {
        "Math": 3,
        "History": 1,
        "Physics": 2,
    }


def test_get_statistics_includes_subject_without_tasks(session):
    math = Subject(name="Math", user_id=1)
    history = Subject(name="History", user_id=1)

    session.add_all([math, history])
    session.commit()

    session.add(
        Task(
            title="Math homework",
            subject_id=math.id,
        )
    )
    session.commit()

    result = statistics.get_statistics(1)

    assert result["tasks_by_subject"] == {
        "Math": 1,
        "History": 0,
    }


def test_get_statistics_ignores_other_users_data(session):
    user_one_subject = Subject(
        name="Math",
        user_id=1,
    )

    user_two_subject = Subject(
        name="Physics",
        user_id=2,
    )

    session.add_all([
        user_one_subject,
        user_two_subject,
    ])
    session.commit()

    session.add_all([
        Task(
            title="Math homework",
            subject_id=user_one_subject.id,
        ),
        Task(
            title="Physics homework",
            subject_id=user_two_subject.id,
            completed=True,
        ),
    ])
    session.commit()

    result = statistics.get_statistics(1)

    assert result["total_subjects"] == 1
    assert result["total_tasks"] == 1
    assert result["completed_tasks"] == 0
    assert result["remaining_tasks"] == 1
    assert result["tasks_by_subject"] == {
        "Math": 1,
    }


def test_get_statistics_returns_zero_completion_rate_for_no_tasks(session):
    subject = Subject(
        name="Math",
        user_id=1,
    )

    session.add(subject)
    session.commit()

    result = statistics.get_statistics(1)

    assert result["total_subjects"] == 1
    assert result["total_tasks"] == 0
    assert result["completed_tasks"] == 0
    assert result["remaining_tasks"] == 0
    assert result["tasks_with_deadline"] == 0
    assert result["tasks_without_deadline"] == 0
    assert result["overdue_tasks"] == 0
    assert result["completion_rate"] == 0
    assert result["tasks_by_subject"] == {
        "Math": 0,
    }
    