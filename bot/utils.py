import os

from aiogram.types import FSInputFile

from bot.core.models import Candidate, CandidateNomination


def singleton(cls):
    instances = {}

    class Wrapper(cls):
        def __new__(cls, *args, **kwargs):
            if cls not in instances:
                instances[cls] = super(Wrapper, cls).__new__(cls)
            return instances[cls]

    return Wrapper


def get_photo(file_name: str) -> FSInputFile:
    file_path = os.path.join(os.path.dirname(__file__), "static", f"{file_name}.png")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_name} not found")

    return FSInputFile(file_path)


def get_nomination_verbose(nomination: str) -> str:
    nominations = {
        "channel_nom": "Канал року",
        "admin_nom": "Адмін року",
        "content_creator_nom": "Контентщик року",
        "blog_nom": "Блог року",
        "posting_bot_nom": "Постинг бот року",
        "admin_chat_nom": "Адмінський чат року",
        "scam_nom": "Скам року",
        "theme_nom": "Тематика року",
        "manager_nom": "Менеджер року",
        "welcome_bot_nom": "Привітальний бот року",
        "buyer_nom": "Закупщик року",
        "info_gypsy_nom": "Інфоциган року",
        "clown_nom": "Клоун року",
    }
    return nominations[nomination]


def map_candidates_to_votes(
    candidates: list[Candidate], candidate_nominations: list[CandidateNomination]
) -> dict[str, int]:
    candidate_map = {candidate.id: candidate.username for candidate in candidates}
    result = {}
    for nomination in candidate_nominations:
        username = candidate_map.get(nomination.candidate)
        if username:
            result[username] = nomination.votes_count
    return result
