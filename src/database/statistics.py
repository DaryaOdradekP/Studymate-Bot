from src.database.subjects import get_subjects
from src.database.tasks import get_tasks


def get_statistics(user_id: int):
    subjects = get_subjects(user_id)
    tasks = get_tasks(user_id)

    total_subjects = len(subjects)
    total_tasks = len(tasks)

    tasks_by_subject = {}

    for subject in subjects:
        tasks_by_subject[subject.name] = 0

    for task in tasks:
        tasks_by_subject[task.subject.name] += 1

    return {
        "total_subjects": total_subjects,
        "total_tasks": total_tasks,
        "tasks_by_subject": tasks_by_subject,
    }
