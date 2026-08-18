from aiogram import Router, F
from aiogram.types import Message

from src.database.statistics import get_statistics


router = Router()


@router.message(F.text == "Statistics")
async def statistics_handler(message: Message):
    user_id = message.from_user.id

    statistics = get_statistics(user_id)

    text = (
        "Statistics\n\n"
        f"Subjects: {statistics['total_subjects']}\n\n"
        f"Tasks: {statistics['total_tasks']}\n"
        f"Completed: {statistics['completed_tasks']}\n"
        f"Remaining: {statistics['remaining_tasks']}\n\n"
        f"Tasks with deadlines: {statistics['tasks_with_deadline']}\n"
        f"Tasks without deadlines: {statistics['tasks_without_deadline']}\n"
        f"Overdue tasks: {statistics['overdue_tasks']}\n\n"
        f"Completion rate: {statistics['completion_rate']}%\n"
    )

    if statistics["tasks_by_subject"]:
        text += "\nTasks by subject:\n"

        for subject, count in statistics["tasks_by_subject"].items():
            text += f"• {subject}: {count}\n"

    await message.answer(text)
    