from aiogram import Router, F
from aiogram.types import Message
from src.keyboards.subjects_menu import subjects_menu
from src.keyboards.main_menu import main_menu
from aiogram.fsm.context import FSMContext
from src.states.subjects import SubjectState
from src.database.db import SessionLocal
from src.database.models import Subject
from sqlalchemy import select
from src.database.db import SessionLocal

router = Router()


@router.message(F.text == "Subjects")
async def subjects_handler(message: Message):
    await message.answer(
        text = "Subject menu",
        reply_markup=subjects_menu,
    )

@router.message(F.text == "Back")
async def back_handler(message: Message):
    await message.answer(
        text="Main menu",
        reply_markup=main_menu,
    )

@router.message(F.text == "Show Subject")
async def show_subject_handler(message: Message):
    session = SessionLocal()

    statement = select(Subject)

    result = session.execute(statement)

    subjects = result.scalars().all()

    session.close()

    if not subjects:
        await message.answer(
            text="Your subjects:\n\nNo subjects yet."
        )
        return
    
    text = "Your subjects:\n\n"
    for subject in subjects:
        text += f"• {subject.name}\n"

    await message.answer(text)

@router.message(F.text == "Add Subject")
async def add_subject_handler(message: Message, state: FSMContext):
    await state.set_state(SubjectState.waiting_for_name)
    await message.answer(
        text="Enter subject name",
    )

@router.message(SubjectState.waiting_for_name)
async def process_subject_name(message: Message, state: FSMContext):
    subject_name = message.text

    session = SessionLocal()

    subject = Subject(name=subject_name)

    session.add(subject)
    session.commit()
    session.close()

    await state.clear()

    await message.answer(
        text=f"Subject '{subject_name}' added!"
    )

