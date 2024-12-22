from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Nomination

from django.contrib.auth import get_user_model

User = get_user_model()


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


@receiver(post_migrate)
def create_default_superuser(sender, **kwargs):
    try:
        if not User.objects.filter(username="awards_admin").exists():
            User.objects.create_superuser(
                username="awards_admin",
                email="admin@example.com",
                password="awards_admin",
            )
    except Exception as e:
        print(f"Error creating default superuser: {e}")
