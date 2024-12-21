from aiogram.fsm.state import StatesGroup, State


class States(StatesGroup):
    select_nomination = State()
    vote_menu = State()
    get_vote = State()
    new_candidate = State()
    candidate_description = State()
