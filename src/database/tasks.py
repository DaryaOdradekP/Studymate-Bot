from sqlalchemy import select

from src.database.db import SessionLocal
from src.database.models import Task, Subject

from sqlalchemy.orm import selectinload

from datetime import date

def add_task(
    subject_name: str,
    title: str,
    description: str | None,
    deadline: date | None,
):
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
        deadline=deadline,
        subject_id=subject.id,
    )

    session.add(task)
    session.commit()
    session.close()

    return True


def get_tasks():
    session = SessionLocal()

    statement = (
        select(Task)
        .join(Task.subject)
        .options(selectinload(Task.subject))
        .order_by(Subject.name, Task.title)
    )

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

def task_exists(subject_name: str, title: str):
    session = SessionLocal()

    statement = select(Subject).where(Subject.name == subject_name)
    result = session.execute(statement)

    subject = result.scalar_one_or_none()

    if subject is None:
        session.close()
        return False

    statement = select(Task).where(
        Task.subject_id == subject.id,
        Task.title == title
    )

    result = session.execute(statement)

    existing_task = result.scalar_one_or_none()

    session.close()

    return existing_task is not None


def complete_task(title: str):
    session = SessionLocal()

    statement = select(Task).where(Task.title == title)

    result = session.execute(statement)

    task = result.scalar_one_or_none()

    if task is None:
        session.close()
        return False

    if task.completed:
        session.close()
        return False

    task.completed = True
    session.commit()
    session.close()

    return True


def update_task_title(old_title: str, new_title: str):
    session = SessionLocal()

    statement = select(Task).where(Task.title == old_title)
    result = session.execute(statement)

    task = result.scalar_one_or_none()

    if task is None:
        session.close()
        return False

    statement = select(Task).where(
        Task.title == new_title,
        Task.subject_id == task.subject_id,
    )

    result = session.execute(statement)

    existing_task = result.scalar_one_or_none()

    if existing_task is not None:
        session.close()
        return False

    task.title = new_title

    session.commit()
    session.close()

    return True


def update_task_description(title: str, description: str | None):
    session = SessionLocal()

    statement = select(Task).where(Task.title == title)
    result = session.execute(statement)

    task = result.scalar_one_or_none()

    if task is None:
        session.close()
        return False

    task.description = description

    session.commit()
    session.close()

    return True


def update_task_deadline(title: str, deadline: date | None):
    session = SessionLocal()

    statement = select(Task).where(Task.title == title)
    result = session.execute(statement)

    task = result.scalar_one_or_none()

    if task is None:
        session.close()
        return False

    task.deadline = deadline

    session.commit()
    session.close()

    return True


def get_tasks_count():
    session = SessionLocal()

    statement = select(Task)

    result = session.execute(statement)

    count = len(result.scalars().all())

    session.close()

    return count


def get_completed_tasks_count():
    session = SessionLocal()

    statement = select(Task).where(Task.completed == True)

    result = session.execute(statement)

    count = len(result.scalars().all())

    session.close()

    return count


def get_tasks_with_deadline_count():
    session = SessionLocal()

    statement = select(Task).where(Task.deadline != None)

    result = session.execute(statement)

    count = len(result.scalars().all())

    session.close()

    return count


def get_tasks_without_deadline_count():
    session = SessionLocal()

    statement = select(Task).where(Task.deadline == None)

    result = session.execute(statement)

    count = len(result.scalars().all())

    session.close()

    return count


def get_overdue_tasks_count():
    session = SessionLocal()

    statement = select(Task).where(
        Task.deadline != None,
        Task.deadline < date.today(),
        Task.completed == False,
    )

    result = session.execute(statement)

    count = len(result.scalars().all())

    session.close()

    return count
