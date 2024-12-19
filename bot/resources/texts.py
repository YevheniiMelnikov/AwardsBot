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
    channel_of_the_year = auto()
    admin_of_the_year = auto()
    content_creator_of_the_year = auto()
    blog_of_the_year = auto()
    posting_bot_of_the_year = auto()
    admin_chat_of_the_year = auto()
    scam_of_the_year = auto()
    theme_of_the_year = auto()
    manager_of_the_year = auto()
    welcome_bot_of_the_year = auto()
    buyer_of_the_year = auto()
    info_gypsy_of_the_year = auto()
    clown_of_the_year = auto()

    def __str__(self) -> str:
        return f"buttons.{self.name}"
