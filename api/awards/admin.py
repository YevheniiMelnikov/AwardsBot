from django.contrib import admin
from .models import User, Nomination, Candidate, CandidateNomination, Vote


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "tg_id", "username")


@admin.register(Nomination)
class NominationAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "winner")
    search_fields = ("name",)
    list_filter = ("winner",)


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "status")
    search_fields = ("username",)
    list_filter = ("status",)


@admin.register(CandidateNomination)
class CandidateNominationAdmin(admin.ModelAdmin):
    list_display = ("id", "candidate", "nomination", "votes_count")
    list_filter = ("nomination",)
    search_fields = ("candidate__username", "nomination__name")


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "nomination", "candidate", "created_at")
    list_filter = ("nomination", "candidate", "user")
    search_fields = ("user__tg_id", "candidate__username", "nomination__name")
