from django_filters import CharFilter
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db.models import F
from .models import User, Nomination, Candidate, CandidateNomination, Vote
from .serializers import (
    UserSerializer,
    NominationSerializer,
    CandidateSerializer,
    CandidateNominationSerializer,
    VoteSerializer,
)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["tg_id"]


class NominationViewSet(ModelViewSet):
    queryset = Nomination.objects.all()
    serializer_class = NominationSerializer

    @action(detail=True, methods=["post"])
    def set_winner(self, request, pk=None):
        try:
            nomination = self.get_object()
            candidate_id = request.data.get("candidate_id")
            if not candidate_id:
                return Response({"error": "candidate_id is required"}, status=status.HTTP_400_BAD_REQUEST)
            candidate = Candidate.objects.get(pk=candidate_id)
            if not CandidateNomination.objects.filter(candidate=candidate, nomination=nomination).exists():
                return Response(
                    {"error": "Candidate is not part of this nomination"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            nomination.winner = candidate
            nomination.save()
            return Response(
                {"success": f"Winner for nomination '{nomination.name}' set to '{candidate.username}'"},
                status=status.HTTP_200_OK,
            )
        except Candidate.DoesNotExist:
            return Response({"error": "Candidate not found"}, status=status.HTTP_404_NOT_FOUND)


class CandidateViewSet(ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer


class CandidateNominationFilter(FilterSet):
    nomination_name = CharFilter(field_name="nomination__name", lookup_expr="exact")

    class Meta:
        model = CandidateNomination
        fields = ["nomination_name"]


class CandidateNominationViewSet(ModelViewSet):
    queryset = CandidateNomination.objects.all()
    serializer_class = CandidateNominationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CandidateNominationFilter


class VoteViewSet(ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer

    @action(detail=False, methods=["post"])
    def cast_vote(self, request):
        user_id = request.data.get("user_id")
        nomination_id = request.data.get("nomination_id")
        candidate_id = request.data.get("candidate_id")

        if not all([user_id, nomination_id, candidate_id]):
            return Response(
                {"error": "user_id, nomination_id, and candidate_id are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(pk=user_id)
            nomination = Nomination.objects.get(pk=nomination_id)
            candidate = Candidate.objects.get(pk=candidate_id)

            if not CandidateNomination.objects.filter(candidate=candidate, nomination=nomination).exists():
                return Response(
                    {"error": "Candidate is not part of this nomination"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if Vote.objects.filter(user=user, nomination=nomination).exists():
                return Response(
                    {"error": "User has already voted in this nomination"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            Vote.objects.create(user=user, nomination=nomination, candidate=candidate)
            candidate_nomination = CandidateNomination.objects.get(candidate=candidate, nomination=nomination)
            candidate_nomination.votes_count = F("votes_count") + 1
            candidate_nomination.save()

            return Response(
                {"success": f"Vote cast for '{candidate.username}' in '{nomination.name}'"},
                status=status.HTTP_201_CREATED,
            )

        except (User.DoesNotExist, Nomination.DoesNotExist, Candidate.DoesNotExist):
            return Response(
                {"error": "Invalid user, nomination, or candidate"},
                status=status.HTTP_404_NOT_FOUND,
            )
