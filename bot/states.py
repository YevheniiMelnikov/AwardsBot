from aiogram.fsm.state import StatesGroup, State


class States(StatesGroup):
    select_category = State()
    feedback = State()
