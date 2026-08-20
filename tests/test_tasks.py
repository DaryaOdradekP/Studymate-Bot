import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database.db import Base
from src.database.models import Subject, Task
from src.database import tasks

from datetime import date

@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)

    TestingSessionLocal = sessionmaker(bind=engine)
    test_session = TestingSessionLocal()

    original_session_local = tasks.SessionLocal
    tasks.SessionLocal = TestingSessionLocal

    try:
        yield test_session
    finally:
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


def test_add_task_returns_true_for_new_task(session):
    subject = Subject(
        name="Math",
        user_id=1,
    )

    session.add(subject)
    session.commit()

    result = tasks.add_task(
        "Math",
        "Homework",
        None,
        "Medium",
        None,
        1,
    )

    assert result is True

    task = session.query(Task).one()

    assert task.title == "Homework"
    assert task.description is None
    assert task.subject_id == subject.id
    assert task.completed is False


def test_add_task_returns_false_for_missing_subject(session):
    result = tasks.add_task(
        "Math",
        "Homework",
        None,
        "Medium",
        None,
        1,
    )

    assert result is False
    assert session.query(Task).count() == 0


def test_add_task_returns_false_for_duplicate_task(session):
    subject = Subject(
        name="Math",
        user_id=1,
    )

    session.add(subject)
    session.commit()

    first_result = tasks.add_task(
        "Math",
        "Homework",
        None,
        "Medium",
        None,
        1,
    )

    second_result = tasks.add_task(
        "Math",
        "Homework",
        None,
        "Medium",
        None,
        1,
    )

    assert first_result is True
    assert second_result is False
    assert session.query(Task).count() == 1


def test_get_tasks_returns_only_user_tasks(session):
    math = Subject(
        name="Math",
        user_id=1,
    )

    history = Subject(
        name="History",
        user_id=2,
    )

    session.add_all([math, history])
    session.commit()

    math_task = Task(
        title="Math homework",
        subject_id=math.id,
    )

    history_task = Task(
        title="History homework",
        subject_id=history.id,
    )

    session.add_all([math_task, history_task])
    session.commit()

    result = tasks.get_tasks(1)

    assert len(result) == 1
    assert result[0].title == "Math homework"


def test_delete_task_returns_true_for_existing_task(session):
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

    result = tasks.delete_task("Homework", 1)

    assert result is True
    assert session.query(Task).count() == 0


def test_delete_task_returns_false_for_another_user(session):
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

    result = tasks.delete_task("Homework", 2)

    assert result is False
    assert session.query(Task).count() == 1


def test_complete_task_marks_task_as_completed(session):
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

    result = tasks.complete_task("Homework", 1)

    assert result is True

    session.refresh(task)

    assert task.completed is True


def test_complete_task_returns_false_for_completed_task(session):
    subject = Subject(
        name="Math",
        user_id=1,
    )

    session.add(subject)
    session.commit()

    task = Task(
        title="Homework",
        subject_id=subject.id,
        completed=True,
    )

    session.add(task)
    session.commit()

    result = tasks.complete_task("Homework", 1)

    assert result is False


def test_complete_task_returns_false_for_another_user(session):
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

    result = tasks.complete_task("Homework", 2)

    assert result is False
    assert task.completed is False


def test_update_task_title_changes_title(session):
    subject = Subject(
        name="Math",
        user_id=1,
    )

    session.add(subject)
    session.commit()

    task = Task(
        title="Old title",
        subject_id=subject.id,
    )

    session.add(task)
    session.commit()

    result = tasks.update_task_title(
        "Old title",
        "New title",
        1,
    )

    assert result is True

    session.refresh(task)

    assert task.title == "New title"


def test_update_task_title_returns_false_for_another_user(session):
    subject = Subject(
        name="Math",
        user_id=1,
    )

    session.add(subject)
    session.commit()

    task = Task(
        title="Old title",
        subject_id=subject.id,
    )

    session.add(task)
    session.commit()

    result = tasks.update_task_title(
        "Old title",
        "New title",
        2,
    )

    assert result is False

    session.refresh(task)

    assert task.title == "Old title"


def test_update_task_description_changes_description(session):
    subject = Subject(
        name="Math",
        user_id=1,
    )

    session.add(subject)
    session.commit()

    task = Task(
        title="Homework",
        description="Old description",
        subject_id=subject.id,
    )

    session.add(task)
    session.commit()

    result = tasks.update_task_description(
        "Homework",
        "New description",
        1,
    )

    assert result is True

    session.refresh(task)

    assert task.description == "New description"


def test_update_task_deadline_changes_deadline(session):
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

    deadline = date(2026, 9, 1)

    result = tasks.update_task_deadline(
        "Homework",
        deadline,
        1,
    )

    assert result is True

    session.refresh(task)

    assert task.deadline == deadline


def test_get_overdue_tasks_returns_only_overdue_incomplete_tasks(session):
    subject = Subject(
        name="Math",
        user_id=1,
    )

    session.add(subject)
    session.commit()

    overdue_task = Task(
        title="Overdue",
        subject_id=subject.id,
        deadline=date(2026, 1, 1),
        completed=False,
    )

    future_task = Task(
        title="Future",
        subject_id=subject.id,
        deadline=date(2030, 1, 1),
        completed=False,
    )

    completed_task = Task(
        title="Completed",
        subject_id=subject.id,
        deadline=date(2026, 1, 1),
        completed=True,
    )

    session.add_all([
        overdue_task,
        future_task,
        completed_task,
    ])
    session.commit()

    result = tasks.get_overdue_tasks(1)

    assert len(result) == 1
    assert result[0].title == "Overdue"


def test_get_overdue_tasks_returns_empty_for_user_without_overdue_tasks(session):
    subject = Subject(
        name="Math",
        user_id=1,
    )

    session.add(subject)
    session.commit()

    task = Task(
        title="Future",
        subject_id=subject.id,
        deadline=date(2030, 1, 1),
        completed=False,
    )

    session.add(task)
    session.commit()

    result = tasks.get_overdue_tasks(1)

    assert result == []


def test_get_tasks_count(session):
    subject = Subject(
        name="Math",
        user_id=1,
    )

    session.add(subject)
    session.commit()

    session.add_all([
        Task(title="Homework 1", subject_id=subject.id),
        Task(title="Homework 2", subject_id=subject.id),
        Task(title="Homework 3", subject_id=subject.id),
    ])
    session.commit()

    assert tasks.get_tasks_count(1) == 3


def test_get_completed_tasks_count(session):
    subject = Subject(
        name="Math",
        user_id=1,
    )

    session.add(subject)
    session.commit()

    session.add_all([
        Task(
            title="Completed",
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

    assert tasks.get_completed_tasks_count(1) == 1


def test_get_tasks_with_deadline_count(session):
    subject = Subject(
        name="Math",
        user_id=1,
    )

    session.add(subject)
    session.commit()

    session.add_all([
        Task(
            title="With deadline",
            subject_id=subject.id,
            deadline=date(2026, 9, 1),
        ),
        Task(
            title="Without deadline",
            subject_id=subject.id,
            deadline=None,
        ),
    ])
    session.commit()

    assert tasks.get_tasks_with_deadline_count(1) == 1


def test_get_tasks_without_deadline_count(session):
    subject = Subject(
        name="Math",
        user_id=1,
    )

    session.add(subject)
    session.commit()

    session.add_all([
        Task(
            title="With deadline",
            subject_id=subject.id,
            deadline=date(2026, 9, 1),
        ),
        Task(
            title="Without deadline",
            subject_id=subject.id,
            deadline=None,
        ),
    ])
    session.commit()

    assert tasks.get_tasks_without_deadline_count(1) == 1


def test_get_overdue_tasks_count(session):
    subject = Subject(
        name="Math",
        user_id=1,
    )

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
    ])
    session.commit()

    assert tasks.get_overdue_tasks_count(1) == 1


def test_add_task_allows_same_title_in_different_subjects(session):
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

    first_result = tasks.add_task(
        "Math",
        "Homework",
        None,
        "Medium",
        None,
        1,
    )

    second_result = tasks.add_task(
        "History",
        "Homework",
        None,
        "Medium",
        None,
        1,
    )

    assert first_result is True
    assert second_result is True
    assert session.query(Task).count() == 2


def test_add_task_returns_false_for_another_user_subject(session):
    subject = Subject(
        name="Math",
        user_id=1,
    )

    session.add(subject)
    session.commit()

    result = tasks.add_task(
        "Math",
        "Homework",
        None,
        "Medium",
        None,
        2,
    )

    assert result is False
    assert session.query(Task).count() == 0


def test_add_task_saves_deadline(session):
    subject = Subject(
        name="Math",
        user_id=1,
    )

    session.add(subject)
    session.commit()

    deadline = date(2026, 9, 1)

    result = tasks.add_task(
        "Math",
        "Homework",
        None,
        "Medium",
        deadline,
        1,
    )

    assert result is True

    task = session.query(Task).one()

    assert task.deadline == deadline


def test_get_tasks_returns_all_user_tasks(session):
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

    session.add_all([
        Task(title="Math homework", subject_id=math.id),
        Task(title="Math project", subject_id=math.id),
        Task(title="History essay", subject_id=history.id),
    ])
    session.commit()

    result = tasks.get_tasks(1)

    assert len(result) == 3


def test_get_tasks_returns_empty_for_user_without_tasks(session):
    subject = Subject(
        name="Math",
        user_id=1,
    )

    session.add(subject)
    session.commit()

    assert tasks.get_tasks(1) == []


def test_delete_task_returns_false_for_missing_task(session):
    subject = Subject(
        name="Math",
        user_id=1,
    )

    session.add(subject)
    session.commit()

    result = tasks.delete_task("Missing", 1)

    assert result is False
    assert session.query(Task).count() == 0


def test_complete_task_returns_false_for_missing_task(session):
    subject = Subject(
        name="Math",
        user_id=1,
    )

    session.add(subject)
    session.commit()

    result = tasks.complete_task("Missing", 1)

    assert result is False


def test_update_task_title_returns_false_for_missing_task(session):
    result = tasks.update_task_title(
        "Missing",
        "New title",
        1,
    )

    assert result is False


def test_update_task_title_returns_false_for_duplicate_title(session):
    subject = Subject(
        name="Math",
        user_id=1,
    )

    session.add(subject)
    session.commit()

    first_task = Task(
        title="Homework 1",
        subject_id=subject.id,
    )

    second_task = Task(
        title="Homework 2",
        subject_id=subject.id,
    )

    session.add_all([first_task, second_task])
    session.commit()

    result = tasks.update_task_title(
        "Homework 1",
        "Homework 2",
        1,
    )

    assert result is False

    session.refresh(first_task)

    assert first_task.title == "Homework 1"


def test_update_task_description_can_remove_description(session):
    subject = Subject(
        name="Math",
        user_id=1,
    )

    session.add(subject)
    session.commit()

    task = Task(
        title="Homework",
        description="Some description",
        subject_id=subject.id,
    )

    session.add(task)
    session.commit()

    result = tasks.update_task_description(
        "Homework",
        None,
        1,
    )

    assert result is True

    session.refresh(task)

    assert task.description is None


def test_update_task_description_returns_false_for_missing_task(session):
    result = tasks.update_task_description(
        "Missing",
        "Description",
        1,
    )

    assert result is False


def test_update_task_deadline_can_remove_deadline(session):
    subject = Subject(
        name="Math",
        user_id=1,
    )

    session.add(subject)
    session.commit()

    task = Task(
        title="Homework",
        deadline=date(2026, 9, 1),
        subject_id=subject.id,
    )

    session.add(task)
    session.commit()

    result = tasks.update_task_deadline(
        "Homework",
        None,
        1,
    )

    assert result is True

    session.refresh(task)

    assert task.deadline is None


def test_update_task_deadline_returns_false_for_missing_task(session):
    result = tasks.update_task_deadline(
        "Missing",
        date(2026, 9, 1),
        1,
    )

    assert result is False


def test_get_overdue_tasks_does_not_include_today_deadline(session):
    subject = Subject(
        name="Math",
        user_id=1,
    )

    session.add(subject)
    session.commit()

    task = Task(
        title="Today",
        subject_id=subject.id,
        deadline=date.today(),
        completed=False,
    )

    session.add(task)
    session.commit()

    result = tasks.get_overdue_tasks(1)

    assert result == []


def test_get_overdue_tasks_does_not_return_another_users_tasks(session):
    subject = Subject(
        name="Math",
        user_id=2,
    )

    session.add(subject)
    session.commit()

    task = Task(
        title="Overdue",
        subject_id=subject.id,
        deadline=date(2026, 1, 1),
        completed=False,
    )

    session.add(task)
    session.commit()

    assert tasks.get_overdue_tasks(1) == []


def test_get_tasks_count_isolated_by_user(session):
    user_one_subject = Subject(
        name="Math",
        user_id=1,
    )

    user_two_subject = Subject(
        name="Math",
        user_id=2,
    )

    session.add_all([
        user_one_subject,
        user_two_subject,
    ])
    session.commit()

    session.add_all([
        Task(title="Task 1", subject_id=user_one_subject.id),
        Task(title="Task 2", subject_id=user_one_subject.id),
        Task(title="Task 3", subject_id=user_two_subject.id),
    ])
    session.commit()

    assert tasks.get_tasks_count(1) == 2
    assert tasks.get_tasks_count(2) == 1


def test_get_completed_tasks_count_isolated_by_user(session):
    user_one_subject = Subject(
        name="Math",
        user_id=1,
    )

    user_two_subject = Subject(
        name="Math",
        user_id=2,
    )

    session.add_all([
        user_one_subject,
        user_two_subject,
    ])
    session.commit()

    session.add_all([
        Task(
            title="Completed 1",
            subject_id=user_one_subject.id,
            completed=True,
        ),
        Task(
            title="Completed 2",
            subject_id=user_two_subject.id,
            completed=True,
        ),
    ])
    session.commit()

    assert tasks.get_completed_tasks_count(1) == 1
    assert tasks.get_completed_tasks_count(2) == 1


def test_get_tasks_with_deadline_count_isolated_by_user(session):
    user_one_subject = Subject(
        name="Math",
        user_id=1,
    )

    user_two_subject = Subject(
        name="Math",
        user_id=2,
    )

    session.add_all([
        user_one_subject,
        user_two_subject,
    ])
    session.commit()

    session.add_all([
        Task(
            title="Task 1",
            subject_id=user_one_subject.id,
            deadline=date(2026, 9, 1),
        ),
        Task(
            title="Task 2",
            subject_id=user_two_subject.id,
            deadline=date(2026, 9, 1),
        ),
    ])
    session.commit()

    assert tasks.get_tasks_with_deadline_count(1) == 1
    assert tasks.get_tasks_with_deadline_count(2) == 1


def test_get_tasks_without_deadline_count_isolated_by_user(session):
    user_one_subject = Subject(
        name="Math",
        user_id=1,
    )

    user_two_subject = Subject(
        name="Math",
        user_id=2,
    )

    session.add_all([
        user_one_subject,
        user_two_subject,
    ])
    session.commit()

    session.add_all([
        Task(
            title="Task 1",
            subject_id=user_one_subject.id,
            deadline=None,
        ),
        Task(
            title="Task 2",
            subject_id=user_two_subject.id,
            deadline=None,
        ),
    ])
    session.commit()

    assert tasks.get_tasks_without_deadline_count(1) == 1
    assert tasks.get_tasks_without_deadline_count(2) == 1


def test_get_overdue_tasks_count_does_not_include_today(session):
    subject = Subject(
        name="Math",
        user_id=1,
    )

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
            title="Today",
            subject_id=subject.id,
            deadline=date.today(),
            completed=False,
        ),
    ])
    session.commit()

    assert tasks.get_overdue_tasks_count(1) == 1


def test_get_overdue_tasks_count_isolated_by_user(session):
    user_one_subject = Subject(
        name="Math",
        user_id=1,
    )

    user_two_subject = Subject(
        name="Math",
        user_id=2,
    )

    session.add_all([
        user_one_subject,
        user_two_subject,
    ])
    session.commit()

    session.add_all([
        Task(
            title="Overdue 1",
            subject_id=user_one_subject.id,
            deadline=date(2026, 1, 1),
            completed=False,
        ),
        Task(
            title="Overdue 2",
            subject_id=user_two_subject.id,
            deadline=date(2026, 1, 1),
            completed=False,
        ),
    ])
    session.commit()

    assert tasks.get_overdue_tasks_count(1) == 1
    assert tasks.get_overdue_tasks_count(2) == 1


def test_get_upcoming_tasks_returns_only_incomplete_tasks_within_next_7_days(
    session,
):
    from datetime import date, timedelta

    subject = Subject(
        name="Math",
        user_id=1,
    )

    session.add(subject)
    session.commit()

    session.add_all([
        Task(
            title="Tomorrow",
            subject_id=subject.id,
            deadline=date.today() + timedelta(days=1),
        ),
        Task(
            title="Next week",
            subject_id=subject.id,
            deadline=date.today() + timedelta(days=7),
        ),
        Task(
            title="Too far",
            subject_id=subject.id,
            deadline=date.today() + timedelta(days=8),
        ),
        Task(
            title="Completed",
            subject_id=subject.id,
            deadline=date.today() + timedelta(days=2),
            completed=True,
        ),
    ])
    session.commit()

    result = tasks.get_upcoming_tasks(1)

    titles = [task.title for task in result]

    assert titles == ["Tomorrow", "Next week"]


def test_get_upcoming_tasks_ignores_other_users(session):
    subject_one = Subject(
        name="Math",
        user_id=1,
    )

    subject_two = Subject(
        name="Physics",
        user_id=2,
    )

    session.add_all([subject_one, subject_two])
    session.commit()

    from datetime import date, timedelta

    session.add_all([
        Task(
            title="My task",
            subject_id=subject_one.id,
            deadline=date.today() + timedelta(days=1),
        ),
        Task(
            title="Other task",
            subject_id=subject_two.id,
            deadline=date.today() + timedelta(days=1),
        ),
    ])
    session.commit()

    result = tasks.get_upcoming_tasks(1)

    assert len(result) == 1
    assert result[0].title == "My task"


def test_get_tasks_without_deadline_returns_only_incomplete_tasks(session):
    from datetime import date, timedelta

    subject = Subject(
        name="Math",
        user_id=1,
    )

    session.add(subject)
    session.commit()

    session.add_all([
        Task(
            title="No deadline",
            subject_id=subject.id,
            deadline=None,
        ),
        Task(
            title="With deadline",
            subject_id=subject.id,
            deadline=date.today() + timedelta(days=3),
        ),
        Task(
            title="Completed no deadline",
            subject_id=subject.id,
            deadline=None,
            completed=True,
        ),
    ])
    session.commit()

    result = tasks.get_tasks_without_deadline(1)

    titles = [task.title for task in result]

    assert titles == ["No deadline"]


def test_get_tasks_without_deadline_ignores_other_users(session):
    subject_one = Subject(
        name="Math",
        user_id=1,
    )

    subject_two = Subject(
        name="Physics",
        user_id=2,
    )

    session.add_all([subject_one, subject_two])
    session.commit()

    session.add_all([
        Task(
            title="My task",
            subject_id=subject_one.id,
            deadline=None,
        ),
        Task(
            title="Other task",
            subject_id=subject_two.id,
            deadline=None,
        ),
    ])
    session.commit()

    result = tasks.get_tasks_without_deadline(1)

    assert len(result) == 1
    assert result[0].title == "My task"


def test_add_task_with_priority(session):
    subject = Subject(
        name="Math",
        user_id=1,
    )

    session.add(subject)
    session.commit()

    result = tasks.add_task(
        "Math",
        "Homework",
        "Chapter 3",
        "High",
        None,
        1,
    )

    assert result is True

    task = session.query(Task).one()

    assert task.title == "Homework"
    assert task.priority == "High"


def test_task_priority_defaults_to_medium(session):
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

    result = session.query(Task).one()

    assert result.priority == "Medium"


def test_update_task_priority(session):
    subject = Subject(
        name="Math",
        user_id=1,
    )

    session.add(subject)
    session.commit()

    task = Task(
        title="Homework",
        subject_id=subject.id,
        priority="Medium",
    )

    session.add(task)
    session.commit()

    result = tasks.update_task_priority(
        "Homework",
        "High",
        1,
    )

    assert result is True

    updated_task = session.query(Task).one()

    assert updated_task.priority == "High"


def test_update_task_priority_returns_false_for_missing_task(session):
    result = tasks.update_task_priority(
        "Missing",
        "High",
        1,
    )

    assert result is False


def test_update_task_priority_ignores_other_users(session):
    subject_one = Subject(
        name="Math",
        user_id=1,
    )

    subject_two = Subject(
        name="Physics",
        user_id=2,
    )

    session.add_all([
        subject_one,
        subject_two,
    ])
    session.commit()

    session.add(
        Task(
            title="Homework",
            subject_id=subject_two.id,
            priority="Medium",
        )
    )
    session.commit()

    result = tasks.update_task_priority(
        "Homework",
        "High",
        1,
    )

    assert result is False

    task = session.query(Task).one()

    assert task.priority == "Medium"       


def test_update_task_description_returns_false_for_another_user(session):
    subject = Subject(
        name="Math",
        user_id=1,
    )

    session.add(subject)
    session.commit()

    task = Task(
        title="Homework",
        description="Old description",
        subject_id=subject.id,
    )

    session.add(task)
    session.commit()

    result = tasks.update_task_description(
        "Homework",
        "New description",
        2,
    )

    assert result is False

    session.refresh(task)

    assert task.description == "Old description"


def test_update_task_deadline_returns_false_for_another_user(session):
    subject = Subject(
        name="Math",
        user_id=1,
    )

    session.add(subject)
    session.commit()

    task = Task(
        title="Homework",
        deadline=date(2026, 9, 1),
        subject_id=subject.id,
    )

    session.add(task)
    session.commit()

    result = tasks.update_task_deadline(
        "Homework",
        date(2026, 10, 1),
        2,
    )

    assert result is False

    session.refresh(task)

    assert task.deadline == date(2026, 9, 1)
