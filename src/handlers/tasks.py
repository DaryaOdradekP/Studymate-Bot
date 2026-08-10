from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.database.subjects import get_subjects, subject_exists
from src.database.tasks import add_task, delete_task, get_tasks
from src.keyboards.main_menu import main_menu
from src.keyboards.tasks_menu import tasks_menu
from src.states.tasks import TaskState

router = Router()


@router.message(F.text == "Tasks")
async def tasks_handler(message: Message):
    await message.answer(
        text="Task menu",
        reply_markup=tasks_menu,
    )


@router.message(F.text == "Back")
async def back_handler(message: Message):
    await message.answer(
        text="Main menu",
        reply_markup=main_menu,
    )


@router.message(F.text == "Show Tasks")
async def show_tasks_handler(message: Message):
    tasks = get_tasks()

    if not tasks:
        await message.answer(
            text="Your tasks:\n\nNo tasks yet."
        )
        return

    text = "Your tasks:\n\n"

    current_subject = None

    for task in tasks:
        if task.subject.name != current_subject:
            current_subject = task.subject.name
            text += f"\n{current_subject}\n"

        text += f"• {task.title}\n"

        if task.description:
            text += f"  {task.description}\n"

        text += "\n"

    await message.answer(text)


@router.message(F.text == "Add Task")
async def add_task_handler(message: Message, state: FSMContext):
    subjects = get_subjects()

    if not subjects:
        await message.answer(
            text="There are no subjects yet."
        )
        return

    await state.set_state(TaskState.waiting_for_subject)

    text = "Choose subject:\n\n"

    for subject in subjects:
        text += f"• {subject.name}\n"

    text += "\nEnter subject name:"

    await message.answer(text)


@router.message(TaskState.waiting_for_subject)
async def process_subject_name(message: Message, state: FSMContext):
    subject_name = message.text.strip()

    if not subject_exists(subject_name):
        await message.answer(
            text="Subject not found. Please enter an existing subject."
        )
        return

    await state.update_data(subject_name=subject_name)

    await state.set_state(TaskState.waiting_for_title)

    await message.answer(
        text="Enter task title:"
    )


@router.message(TaskState.waiting_for_title)
async def process_task_title(message: Message, state: FSMContext):
    title = message.text.strip()

    if not title:
        await message.answer(
            text="Task title cannot be empty."
        )
        return

    if len(title) > 100:
        await message.answer(
            text="Task title is too long."
        )
        return

    await state.update_data(title=title)

    await state.set_state(TaskState.waiting_for_description)

    await message.answer(
        text="Enter task description\n(or send '-' to skip):"
    )


@router.message(TaskState.waiting_for_description)
async def process_task_description(message: Message, state: FSMContext):
    description = message.text.strip()

    if description == "-":
        description = None

    data = await state.get_data()

    success = add_task(
        data["subject_name"],
        data["title"],
        description,
    )

    await state.clear()

    if success:
        await message.answer(
            text="Task has been added."
        )
    else:
        await message.answer(
            text="Task with this title already exists in this subject."
        )


@router.message(F.text == "Delete Task")
async def delete_task_handler(message: Message, state: FSMContext):
    tasks = get_tasks()

    if not tasks:
        await message.answer(
            text="There are no tasks yet."
        )
        return

    await state.set_state(TaskState.waiting_for_delete_title)

    text = "Your tasks:\n\n"

    current_subject = None

    for task in tasks:
        if task.subject.name != current_subject:
            current_subject = task.subject.name
            text += f"\n{current_subject}\n"

        text += f"• {task.title}\n"

    text += "\nEnter task title to delete:"

    await message.answer(text)


@router.message(TaskState.waiting_for_delete_title)
async def process_delete_task(message: Message, state: FSMContext):
    task_title = message.text.strip()

    success = delete_task(task_title)

    await state.clear()

    if success:
        await message.answer(
            text=f"Task '{task_title}' deleted."
        )
    else:
        await message.answer(
            text=f"Task '{task_title}' not found."
        )
