from aiogram import Router, F
from aiogram.types import Message

from src.database.statistics import get_statistics


router = Router()


@router.message(F.text == "Statistics")
async def statistics_handler(message: Message):
    statistics = get_statistics()

    text = "Statistics\n\n"

    text += f"Subjects: {statistics['total_subjects']}\n"
    text += f"Tasks: {statistics['total_tasks']}\n\n"

    text += "Tasks by subject\n\n"

    for subject, count in statistics["tasks_by_subject"].items():
        text += f"{subject}: {count}\n"

    await message.answer(text)
