from rest_framework import serializers
from .models import User, Nomination, Candidate, CandidateNomination, Vote


class CandidateNominationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateNomination
        fields = ["id", "candidate", "nomination", "votes_count"]


class CandidateSerializer(serializers.ModelSerializer):
    candidate_nominations = CandidateNominationSerializer(many=True, read_only=True)

    class Meta:
        model = Candidate
        fields = ["id", "username", "status", "candidate_nominations"]


class NominationSerializer(serializers.ModelSerializer):
    candidate_nominations = CandidateNominationSerializer(many=True, read_only=True)
    winner = CandidateSerializer(read_only=True)

    class Meta:
        model = Nomination
        fields = ["id", "name", "candidate_nominations", "winner"]


class UserSerializer(serializers.ModelSerializer):
    votes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ["id", "tg_id", "username", "votes"]


class VoteSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    nomination = serializers.PrimaryKeyRelatedField(queryset=Nomination.objects.all())
    candidate = serializers.PrimaryKeyRelatedField(queryset=Candidate.objects.all())

    class Meta:
        model = Vote
        fields = ["id", "user", "nomination", "candidate", "created_at"]
