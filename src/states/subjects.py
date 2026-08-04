from aiogram.fsm.state import State, StatesGroup


class SubjectState(StatesGroup):
    waiting_for_name = State()