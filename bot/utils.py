import os

from aiogram.types import FSInputFile


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
    # TODO: MAP Nominations
    nominations = {}
