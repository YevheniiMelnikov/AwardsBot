from rest_framework import serializers
from .models import User, Nomination, Candidate, Vote


class CandidateSerializer(serializers.ModelSerializer):
    nominations = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Candidate
        fields = ["id", "username", "status", "nominations", "user"]


class NominationSerializer(serializers.ModelSerializer):
    candidates = CandidateSerializer(many=True, read_only=True)
    winner = CandidateSerializer(read_only=True)

    class Meta:
        model = Nomination
        fields = ["id", "name", "candidates", "winner"]


class UserSerializer(serializers.ModelSerializer):
    candidates = CandidateSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ["id", "tg_id", "username", "candidates"]


class VoteSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    nomination = serializers.PrimaryKeyRelatedField(queryset=Nomination.objects.all())
    candidate = serializers.PrimaryKeyRelatedField(queryset=Candidate.objects.all())

    class Meta:
        model = Vote
        fields = ["id", "user", "nomination", "candidate", "created_at"]
