from enum import Enum, auto


class MessageText(Enum):
    greetings = auto()
    help = auto()
    feedback_sent = auto()
    incoming_feedback = auto()
    select_category = auto()

    def __str__(self) -> str:
        return f"messages.{self.name}"


class ButtonText(Enum):
    ok = auto()
    vote = auto()
    launch = auto()
    channel_nom = auto()
    admin_nom = auto()
    content_creator_nom = auto()
    blog_nom = auto()
    posting_bot_nom = auto()
    admin_chat_nom = auto()
    scam_nom = auto()
    theme_nom = auto()
    manager_nom = auto()
    welcome_bot_nom = auto()
    buyer_nom = auto()
    info_gypsy_nom = auto()
    clown_nom = auto()

    def __str__(self) -> str:
        return f"buttons.{self.name}"
