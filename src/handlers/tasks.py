from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.database.subjects import get_subjects, subject_exists
from src.database.tasks import (
    add_task,
    get_tasks,
    get_overdue_tasks,
    delete_task,
    task_exists,
    complete_task,
    update_task_title,
    update_task_description,
    update_task_deadline,
)
from src.keyboards.main_menu import main_menu
from src.keyboards.tasks_menu import tasks_menu
from src.states.tasks import TaskState
from datetime import datetime, date

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
    user_id = message.from_user.id
    tasks = get_tasks(user_id)

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

        status = "✓" if task.completed else "•"

        text += f"{status} {task.title}\n"

        if task.description:
            text += f"  {task.description}\n"

        if task.deadline:
            text += f"  Deadline: {task.deadline.strftime('%Y-%m-%d')}\n"

        text += "\n"

    await message.answer(text)


@router.message(F.text == "Add Task")
async def add_task_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    subjects = get_subjects(user_id)

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

    user_id = message.from_user.id

    if not subject_exists(subject_name, user_id):
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

    data = await state.get_data()

    if task_exists(data["subject_name"], title):
        await message.answer(
            text="Task with this title already exists in this subject."
        )
        return

    await state.update_data(title=title)

    await state.set_state(TaskState.waiting_for_description)

    await message.answer(
        text="Enter task description\n(or send '-' to skip):"
    )


@router.message(TaskState.waiting_for_description)
async def process_task_description(message: Message, state: FSMContext):
    description = message.text

    if description == "-":
        description = None

    await state.update_data(description=description)

    await state.set_state(TaskState.waiting_for_deadline)

    await message.answer(
        text="Enter deadline (YYYY-MM-DD)\n(or send '-' to skip):"
    )


@router.message(F.text == "Delete Task")
async def delete_task_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    tasks = get_tasks(user_id)

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


@router.message(F.text == "Complete Task")
async def complete_task_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    tasks = get_tasks(user_id)

    if not tasks:
        await message.answer(
            text="There are no tasks yet."
        )
        return

    incomplete_tasks = [task for task in tasks if not task.completed]

    if not incomplete_tasks:
        await message.answer(
            text="All tasks are already completed."
        )
        return

    await state.set_state(TaskState.waiting_for_complete_title)

    text = "Your tasks:\n\n"

    current_subject = None

    for task in incomplete_tasks:
        if task.subject.name != current_subject:
            current_subject = task.subject.name
            text += f"\n{current_subject}\n"

        text += f"• {task.title}\n"

    text += "\nEnter task title to complete:"

    await message.answer(text)


@router.message(TaskState.waiting_for_complete_title)
async def process_complete_task(message: Message, state: FSMContext):
    task_title = message.text

    success = complete_task(task_title)

    await state.clear()

    if success:
        await message.answer(
            text=f"Task '{task_title}' marked as completed."
        )
    else:
        await message.answer(
            text=f"Task '{task_title}' not found."
        )
        

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
            text="Task not found or has already been completed."
        )


@router.message(TaskState.waiting_for_deadline)
async def process_task_deadline(message: Message, state: FSMContext):
    deadline = message.text

    if deadline == "-":
        deadline = None
    else:
        try:
            deadline = datetime.strptime(deadline, "%Y-%m-%d").date()
        except ValueError:
            await message.answer(
                text="Invalid date. Use YYYY-MM-DD or '-' to skip."
            )
            return

        if deadline < date.today():
            await message.answer(
                text="Deadline cannot be in the past."
            )
            return

    data = await state.get_data()

    success = add_task(
        data["subject_name"],
        data["title"],
        data["description"],
        deadline,
    )

    if success:
        await message.answer(
            text="Task has been added."
        )
    else:
        await message.answer(
            text="Task could not be added."
        )

    await state.clear()


@router.message(F.text == "Edit Task")
async def edit_task_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    tasks = get_tasks(user_id)

    if not tasks:
        await message.answer(
            text="There are no tasks yet."
        )
        return

    await state.set_state(TaskState.waiting_for_edit_title)

    text = "Your tasks:\n\n"

    current_subject = None

    for task in tasks:
        if task.subject.name != current_subject:
            current_subject = task.subject.name
            text += f"\n{current_subject}\n"

        text += f"• {task.title}\n"

    text += "\nEnter task title to edit:"

    await message.answer(text)


@router.message(TaskState.waiting_for_edit_title)
async def process_edit_title(message: Message, state: FSMContext):
    title = message.text.strip()

    user_id = message.from_user.id
    tasks = get_tasks(user_id)

    if not any(task.title == title for task in tasks):
        await message.answer(
            text="Task not found."
        )
        return

    await state.update_data(title=title)

    await state.set_state(TaskState.waiting_for_edit_field)

    await message.answer(
        text=(
            "What do you want to edit?\n\n"
            "1 - Title\n"
            "2 - Description\n"
            "3 - Deadline"
        )
    )


@router.message(TaskState.waiting_for_edit_field)
async def process_edit_field(message: Message, state: FSMContext):
    choice = message.text.strip()

    if choice == "1":
        await state.set_state(TaskState.waiting_for_new_title)
        await message.answer(
            text="Enter new task title:"
        )

    elif choice == "2":
        await state.set_state(TaskState.waiting_for_new_description)
        await message.answer(
            text="Enter new description\n(or send '-' to remove it):"
        )

    elif choice == "3":
        await state.set_state(TaskState.waiting_for_new_deadline)
        await message.answer(
            text="Enter new deadline (YYYY-MM-DD)\n(or send '-' to remove it):"
        )

    else:
        await message.answer(
            text="Choose 1, 2 or 3."
        )


@router.message(TaskState.waiting_for_new_title)
async def process_new_title(message: Message, state: FSMContext):
    new_title = message.text.strip()

    if not new_title:
        await message.answer(
            text="Task title cannot be empty."
        )
        return

    data = await state.get_data()

    success = update_task_title(
        data["title"],
        new_title,
    )

    await state.clear()

    if success:
        await message.answer(
            text="Task title updated."
        )
    else:
        await message.answer(
            text="Task title could not be updated."
        )

@router.message(TaskState.waiting_for_new_description)
async def process_new_description(message: Message, state: FSMContext):
    description = message.text.strip()

    if description == "-":
        description = None

    data = await state.get_data()

    success = update_task_description(
        data["title"],
        description,
    )

    await state.clear()

    if success:
        await message.answer(
            text="Task description updated."
        )
    else:
        await message.answer(
            text="Task description could not be updated."
        )


@router.message(TaskState.waiting_for_new_deadline)
async def process_new_deadline(message: Message, state: FSMContext):
    deadline = message.text.strip()

    if deadline == "-":
        deadline = None
    else:
        try:
            deadline = datetime.strptime(deadline, "%Y-%m-%d").date()
        except ValueError:
            await message.answer(
                text="Invalid date. Use YYYY-MM-DD or '-' to skip."
            )
            return

        if deadline < date.today():
            await message.answer(
                text="Deadline cannot be in the past."
            )
            return

    data = await state.get_data()

    success = update_task_deadline(
        data["title"],
        deadline,
    )

    await state.clear()

    if success:
        await message.answer(
            text="Task deadline updated."
        )
    else:
        await message.answer(
            text="Task deadline could not be updated."
        )


@router.message(F.text == "Overdue Tasks")
async def overdue_tasks_handler(message: Message):
    user_id = message.from_user.id
    tasks = get_tasks(user_id)

    if not tasks:
        await message.answer(
            text="There are no overdue tasks."
        )
        return

    text = "Overdue tasks:\n\n"

    current_subject = None

    for task in tasks:
        if task.subject.name != current_subject:
            current_subject = task.subject.name
            text += f"\n{current_subject}\n"

        text += f"• {task.title}\n"
        text += f"  Deadline: {task.deadline.strftime('%Y-%m-%d')}\n"

        if task.description:
            text += f"  {task.description}\n"

        text += "\n"

    await message.answer(text)
