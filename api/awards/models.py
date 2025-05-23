from django.db import models


class User(models.Model):
    tg_id = models.CharField(max_length=50, unique=True)
    username = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"User {self.tg_id}"


class Nomination(models.Model):
    name = models.CharField(max_length=100)
    winner = models.ForeignKey(
        "Candidate",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="won_nominations",
        help_text="The winner of the nomination",
    )

    def __str__(self):
        return self.name


class Candidate(models.Model):
    username = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=50, default="new")

    def __str__(self):
        return f"Candidate {self.username}"


class CandidateNomination(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name="candidate_nominations")
    nomination = models.ForeignKey(Nomination, on_delete=models.CASCADE, related_name="candidate_nominations")
    votes_count = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("candidate", "nomination")

    def __str__(self):
        return f"{self.candidate.username} in {self.nomination.name} - Votes: {self.votes_count}"


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="votes")
    nomination = models.ForeignKey(Nomination, on_delete=models.CASCADE, related_name="votes")
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name="votes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "nomination")

    def __str__(self):
        return f"Vote by {self.user} for {self.candidate} in {self.nomination}"
