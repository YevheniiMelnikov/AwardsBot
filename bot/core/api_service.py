import os
from json import JSONDecodeError
from urllib.parse import urljoin

import httpx
import loguru
from aiogram.types import Message

from bot.core.models import User, CandidateNomination, Candidate, Nomination
from bot.utils import singleton

logger = loguru.logger


@singleton
class ApiService:
    def __init__(self):
        self.backend_url = os.environ.get("BACKEND_URL")
        self.api_key = os.environ.get("API_KEY")
        self.client = httpx.AsyncClient()

    async def _api_request(
        self, method: str, url: str, data: dict | None = None, headers: dict = None, params: dict = None
    ) -> tuple:
        logger.debug(
            f"Executing {method.upper()} request to {url} with data: {data}, params: {params}, and headers: {headers}"
        )
        try:
            response = await self.client.request(method, url, json=data, headers=headers, params=params)
            if response.is_success:
                try:
                    json_data = response.json()
                    return response.status_code, json_data
                except JSONDecodeError:
                    logger.error(f"Invalid JSON response from {url}: {response.text}")
                    return response.status_code, None
            else:
                try:
                    error_data = response.json()
                except JSONDecodeError:
                    error_data = {"error": response.text}

                if response.status_code == 404:
                    logger.info(f"Request to {url} returned 404: {error_data}")
                else:
                    logger.error(
                        f"Request to {url} failed with status code {response.status_code} and response: {error_data}"
                    )

                return response.status_code, error_data

        except Exception as e:
            logger.exception(f"Unexpected error occurred: {e}")

    async def get_user_by_tg(self, telegram_id: int) -> User | None:
        url = urljoin(self.backend_url, f"api/users/?tg_id={telegram_id}")
        status_code, users_data = await self._api_request(
            "get", url, headers={"Authorization": f"Api-Key {self.api_key}"}
        )
        if status_code == 200 and isinstance(users_data, list) and len(users_data) > 0:
            return User.from_dict(users_data[0])

        return None

    async def create_user(self, message: Message) -> User | None:
        url = urljoin(self.backend_url, "api/users/")
        username = message.from_user.username if message.from_user.username else ""
        data = {"tg_id": message.from_user.id, "username": username}
        status_code, profile_data = await self._api_request(
            "post", url, data=data, headers={"Authorization": f"Api-Key {self.api_key}"}
        )
        if status_code == 201 and profile_data:
            logger.info(f"User {message.from_user.id} added to database")
            return User.from_dict(profile_data)

        return None

    async def get_candidate_nominations(self, nomination: str) -> list[CandidateNomination]:
        url = urljoin(self.backend_url, f"api/candidatenominations/?nomination_name={nomination}")
        status_code, candidates = await self._api_request(
            "get", url, headers={"Authorization": f"Api-Key {self.api_key}"}
        )
        if status_code == 200 and isinstance(candidates, list):
            return [CandidateNomination.from_dict(candidate) for candidate in candidates]

        return []

    async def create_candidate_nomination(self, candidate_id: int, nomination_id: int) -> bool:
        url = urljoin(self.backend_url, "api/candidatenominations/")
        data = {"candidate": candidate_id, "nomination": nomination_id, "votes_count": 0}
        status_code, _ = await self._api_request(
            "post", url, data=data, headers={"Authorization": f"Api-Key {self.api_key}"}
        )
        return status_code == 201

    async def get_all_candidates(self) -> list[Candidate]:
        url = urljoin(self.backend_url, "api/candidates/")
        status_code, candidates = await self._api_request(
            "get", url, headers={"Authorization": f"Api-Key {self.api_key}"}
        )
        if status_code == 200 and isinstance(candidates, list):
            return [
                Candidate(
                    id=candidate["id"],
                    username=candidate["username"],
                    status=candidate["status"],
                    nominations=[
                        CandidateNomination(
                            id=nomination["id"],
                            candidate=nomination["candidate"],
                            nomination=nomination["nomination"],
                            votes_count=nomination["votes_count"],
                        )
                        for nomination in candidate.get("candidate_nominations", [])
                    ],
                )
                for candidate in candidates
            ]

        return []

    async def increment_vote(self, nomination_id: int, new_votes_count: int) -> bool:
        url = urljoin(self.backend_url, f"api/candidatenominations/{nomination_id}/")
        data = {"votes_count": new_votes_count}
        status_code, _ = await self._api_request(
            "patch", url, data=data, headers={"Authorization": f"Api-Key {self.api_key}"}
        )
        return status_code == 200

    async def get_all_nominations(self) -> list[Nomination]:
        url = urljoin(self.backend_url, "api/nominations/")
        status_code, nominations = await self._api_request(
            "get", url, headers={"Authorization": f"Api-Key {self.api_key}"}
        )
        if status_code == 200 and isinstance(nominations, list):
            return [Nomination.from_dict(nomination) for nomination in nominations]

        return []

    async def has_user_voted(self, user_tg_id: int, nomination_id: int) -> bool:
        url = urljoin(self.backend_url, f"api/votes/")
        params = {"user__tg_id": user_tg_id}
        status_code, votes = await self._api_request(
            "get", url, headers={"Authorization": f"Api-Key {self.api_key}"}, params=params
        )
        if status_code == 200 and isinstance(votes, list):
            return any(vote["nomination"] == nomination_id for vote in votes)
        return False

    async def create_vote(self, user_tg_id: int, nomination_id: int, candidate_id: int) -> bool:
        user = await self.get_user_by_tg(user_tg_id)
        assert user
        url = urljoin(self.backend_url, "api/votes/")
        data = {
            "user": user.id,
            "nomination": nomination_id,
            "candidate": candidate_id,
        }
        status_code, _ = await self._api_request(
            "post", url, data=data, headers={"Authorization": f"Api-Key {self.api_key}"}
        )
        return status_code == 201

    async def create_candidate(self, username: str) -> int | None:
        url = urljoin(self.backend_url, "api/candidates/")
        data = {"username": username}
        status_code, response = await self._api_request(
            "post", url, data=data, headers={"Authorization": f"Api-Key {self.api_key}"}
        )
        if status_code == 201 and response:
            return response.get("id")

        return None

    async def update_candidate_status(self, candidate_id: int, new_status: str) -> bool:
        url = urljoin(self.backend_url, f"api/candidates/{candidate_id}/")
        data = {"status": new_status}
        status_code, _ = await self._api_request(
            "patch", url, data=data, headers={"Authorization": f"Api-Key {self.api_key}"}
        )
        return status_code == 200

    async def get_nomination_by_name(self, nomination_name: str) -> Nomination | None:
        url = urljoin(self.backend_url, f"api/nominations/?name={nomination_name}")
        status_code, response = await self._api_request(
            "get", url, headers={"Authorization": f"Api-Key {self.api_key}"}
        )
        if status_code == 200 and isinstance(response, list) and len(response) > 0:
            return Nomination.from_dict(response[0])

        return None

    async def get_candidate_by_username(self, username: str) -> Candidate | None:
        url = urljoin(self.backend_url, f"api/candidates/?username={username}")
        status_code, response = await self._api_request(
            "get", url, headers={"Authorization": f"Api-Key {self.api_key}"}
        )
        if status_code == 200 and isinstance(response, list) and len(response) > 0:
            return Candidate.from_dict(response[0])

        return None


api_service = ApiService()
