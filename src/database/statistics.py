from src.database.subjects import get_subjects
from src.database.tasks import (
    get_tasks,
    get_completed_tasks_count,
    get_tasks_with_deadline_count,
    get_tasks_without_deadline_count,
    get_overdue_tasks_count,
)


def get_statistics(user_id: int):
    subjects = get_subjects(user_id)
    tasks = get_tasks(user_id)

    total_subjects = len(subjects)
    total_tasks = len(tasks)

    completed_tasks = get_completed_tasks_count(user_id)
    tasks_with_deadline = get_tasks_with_deadline_count(user_id)
    tasks_without_deadline = get_tasks_without_deadline_count(user_id)
    overdue_tasks = get_overdue_tasks_count(user_id)

    remaining_tasks = total_tasks - completed_tasks

    completion_rate = 0

    if total_tasks > 0:
        completion_rate = round(
            completed_tasks / total_tasks * 100
        )

    tasks_by_subject = {}

    for subject in subjects:
        tasks_by_subject[subject.name] = 0

    for task in tasks:
        tasks_by_subject[task.subject.name] += 1

    return {
        "total_subjects": total_subjects,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "remaining_tasks": remaining_tasks,
        "tasks_with_deadline": tasks_with_deadline,
        "tasks_without_deadline": tasks_without_deadline,
        "overdue_tasks": overdue_tasks,
        "completion_rate": completion_rate,
        "tasks_by_subject": tasks_by_subject,
    }
