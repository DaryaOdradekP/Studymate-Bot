from aiogram.fsm.state import State, StatesGroup


class TaskState(StatesGroup):
    waiting_for_subject = State()
    waiting_for_title = State()
    waiting_for_description = State()
    waiting_for_deadline = State()
    waiting_for_delete_title = State()
    waiting_for_complete_title = State()
    