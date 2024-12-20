import os
from json import JSONDecodeError
from urllib.parse import urljoin

import httpx
import loguru
from aiogram.types import Message

from bot.core.models import User, Candidate
from bot.utils import singleton

logger = loguru.logger


@singleton
class ApiService:
    def __init__(self):
        self.backend_url = os.environ.get("BACKEND_URL")
        self.api_key = os.environ.get("API_KEY")
        self.client = httpx.AsyncClient()

    async def _api_request(self, method: str, url: str, data: dict | None = None, headers: dict = None) -> tuple:
        logger.debug(f"Executing {method.upper()} request to {url} with data: {data} and headers: {headers}")
        try:
            response = await self.client.request(method, url, json=data, headers=headers)
            if response.is_success:
                try:
                    json_data = response.json()
                    return response.status_code, json_data
                except JSONDecodeError:
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
        url = urljoin(self.backend_url, f"api/users/get_user_by_tg/")
        data = {"tg_id": telegram_id}
        status_code, profile_data = await self._api_request(
            "post", url, data, {"Authorization": f"Api-Key {self.api_key}"}
        )
        if status_code == 200 and profile_data:
            return User.from_dict(profile_data)

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

    async def get_candidates(self, nomination: str) -> list[Candidate]:
        url = urljoin(self.backend_url, f"api/candidates/{nomination}/")
        status_code, candidates = await self._api_request("get", url)
        if status_code == 200 and candidates:
            return candidates

        return []


api_service = ApiService()
