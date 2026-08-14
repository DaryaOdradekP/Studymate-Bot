from aiogram import Router, F
from aiogram.types import Message

from src.database.statistics import get_statistics
from src.database.subjects import get_subjects
from src.database.tasks import (
    get_tasks_count,
    get_completed_tasks_count,
    get_tasks_with_deadline_count,
    get_tasks_without_deadline_count,
    get_overdue_tasks_count,
)


router = Router()


@router.message(F.text == "Statistics")
async def statistics_handler(message: Message):
    subjects_count = len(get_subjects())

    tasks_count = get_tasks_count()
    completed_count = get_completed_tasks_count()

    remaining_count = tasks_count - completed_count

    with_deadline = get_tasks_with_deadline_count()
    without_deadline = get_tasks_without_deadline_count()
    overdue_count = get_overdue_tasks_count()

    completion_rate = 0

    if tasks_count > 0:
        completion_rate = round(completed_count / tasks_count * 100)

    text = (
        "Statistics\n\n"
        f"Subjects: {subjects_count}\n\n"
        f"Tasks: {tasks_count}\n"
        f"Completed: {completed_count}\n"
        f"Remaining: {remaining_count}\n\n"
        f"Tasks with deadlines: {with_deadline}\n"
        f"Tasks without deadlines: {without_deadline}\n"
        f"Overdue tasks: {overdue_count}\n\n"
        f"Completion rate: {completion_rate}%"
    )

    await message.answer(text)
