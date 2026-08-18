from aiogram.fsm.state import State, StatesGroup


class TaskState(StatesGroup):
    waiting_for_subject = State()
    waiting_for_title = State()
    waiting_for_description = State()
    waiting_for_priority = State()
    waiting_for_deadline = State()

    waiting_for_delete_title = State()
    waiting_for_complete_title = State()

    waiting_for_edit_title = State()
    waiting_for_edit_field = State()
    waiting_for_new_title = State()
    waiting_for_new_description = State()
    waiting_for_new_priority = State()
    waiting_for_new_deadline = State()
    