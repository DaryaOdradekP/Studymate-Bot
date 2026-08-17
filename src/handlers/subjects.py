from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.database.subjects import add_subject, get_subjects, delete_subject
from src.keyboards.main_menu import main_menu
from src.keyboards.subjects_menu import subjects_menu
from src.states.subjects import SubjectState

router = Router()


@router.message(F.text == "Subjects")
async def subjects_handler(message: Message, state: FSMContext):
    await state.clear()

    await message.answer(
        text="Subject menu",
        reply_markup=subjects_menu,
    )


@router.message(F.text == "Back")
async def back_handler(message: Message, state: FSMContext):
    await state.clear()

    await message.answer(
        text="Main menu",
        reply_markup=main_menu,
    )


@router.message(F.text == "Show Subject")
async def show_subject_handler(message: Message, state: FSMContext):
    await state.clear()

    user_id = message.from_user.id
    subjects = get_subjects(user_id)

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
    await state.clear()
    await state.set_state(SubjectState.waiting_for_name)

    await message.answer(
        text="Enter subject name",
    )


@router.message(F.text == "Delete Subject")
async def delete_subject_handler(message: Message, state: FSMContext):
    await state.clear()

    user_id = message.from_user.id
    subjects = get_subjects(user_id)

    if not subjects:
        await message.answer(
            text="There are no subjects yet."
        )
        return

    await state.set_state(SubjectState.waiting_for_delete_name)

    text = "Your subjects:\n\n"

    for subject in subjects:
        text += f"• {subject.name}\n"

    text += "\nEnter subject name to delete:"

    await message.answer(text)


@router.message(SubjectState.waiting_for_delete_name)
async def process_delete_subject(message: Message, state: FSMContext):
    subject_name = message.text.strip()
    user_id = message.from_user.id

    success = delete_subject(
        subject_name,
        user_id,
    )

    await state.clear()

    if success:
        await message.answer(
            text=f"Subject '{subject_name}' deleted."
        )
    else:
        await message.answer(
            text=f"Subject '{subject_name}' not found."
        )


@router.message(SubjectState.waiting_for_name)
async def process_subject_name(message: Message, state: FSMContext):
    subject_name = message.text.strip()
    user_id = message.from_user.id

    if not subject_name:
        await message.answer(
            text="Subject name cannot be empty."
        )
        return

    if len(subject_name) > 100:
        await message.answer(
            text="Subject name is too long."
        )
        return

    success = add_subject(
        subject_name,
        user_id,
    )

    await state.clear()

    if success:
        await message.answer(
            text=f"Subject '{subject_name}' added!"
        )
    else:
        await message.answer(
            text=f"Subject '{subject_name}' already exists."
        )
        