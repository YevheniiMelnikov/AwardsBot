import os

import yaml

from bot.resources.texts import MessageText, ButtonText

ResourceType = str | MessageText | ButtonText


if os.getenv("ENVIRONMENT", "dev") == "dev":
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    RESOURCES = {
        "messages": f"{PROJECT_ROOT}/resources/messages.yaml",
        "buttons": f"{PROJECT_ROOT}/resources/buttons.yaml",
        "commands": f"{PROJECT_ROOT}/resources/commands.yaml",
    }
else:
    RESOURCES = {
        "messages": "/app/resources/messages.yaml",
        "buttons": "/app/resources/buttons.yaml",
        "commands": "/app/resources/commands.yaml",
    }


class TextManager:
    def __init__(self) -> None:
        self.messages = self.load_messages()
        self.commands = self.load_commands()

    def get_text(self, key: ResourceType) -> str:
        key_str = str(key)
        if key_str in self.messages:
            return self.messages[key_str]
        else:
            raise ValueError(f"Key {key.name} not found in messages.")

    @staticmethod
    def load_messages() -> dict[str, str]:
        result = {}
        for type_, path in RESOURCES.items():
            if type_ == "commands":
                continue
            with open(path, "r", encoding="utf-8") as file:
                data = yaml.safe_load(file)
            for key, value in data.items():
                result[f"{type_}.{key}"] = value
        return result

    @staticmethod
    def load_commands() -> dict[str, str]:
        result = {}
        with open(RESOURCES["commands"], "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)
            for key, value in data.items():
                result[key] = value
        return result


resource_manager = TextManager()
