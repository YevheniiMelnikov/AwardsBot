from aiogram.fsm.state import StatesGroup, State


class States(StatesGroup):
    main_menu = State()
    vote_menu = State()
    get_vote = State()
    new_candidate = State()
    candidate_description = State()
    request_sent = State()
