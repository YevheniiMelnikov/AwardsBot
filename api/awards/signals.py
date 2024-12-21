from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Nomination


@receiver(post_migrate)
def create_nominations(sender, **kwargs):
    if sender.name == "api.awards":
        nominations = [
            "channel_nom",
            "admin_nom",
            "content_creator_nom",
            "blog_nom",
            "posting_bot_nom",
            "admin_chat_nom",
            "scam_nom",
            "theme_nom",
            "manager_nom",
            "welcome_bot_nom",
            "buyer_nom",
            "info_gypsy_nom",
            "clown_nom",
        ]

        for name in nominations:
            Nomination.objects.get_or_create(name=name)
