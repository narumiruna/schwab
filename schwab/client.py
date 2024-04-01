from __future__ import annotations

import base64
import os
from datetime import datetime
from datetime import timedelta
from urllib.parse import urljoin

import httpx
from loguru import logger

from .quote import QuoteField
from .quote import QuoteResponse


def b64encode(s: str) -> str:
    return base64.b64encode(s.encode()).decode()


class Client:
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        refresh_token: str,
        base_url: str = "https://api.schwabapi.com/",
        refresh_time: timedelta = timedelta(minutes=20),
    ) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token
        self.base_url = base_url
        self.refresh_time = refresh_time

        self.refreshed_at = datetime(1, 1, 1)
        self.access_token = ""

    @classmethod
    def from_env(cls) -> Client:
        client_id = os.getenv("SCHWAB_CLIENT_ID")
        if not client_id:
            raise ValueError("SCHWAB_CLIENT_ID is not set")

        client_secret = os.getenv("SCHWAB_CLIENT_SECRET")
        if not client_secret:
            raise ValueError("SCHWAB_CLIENT_SECRET is not set")

        refresh_token = os.getenv("SCHWAB_REFRESH_TOKEN")
        if not refresh_token:
            raise ValueError("SCHWAB_REFRESH_TOKEN is not set")

        return cls(
            client_id=client_id,
            client_secret=client_secret,
            refresh_token=refresh_token,
        )

    def build_url(self, url: str) -> str:
        return urljoin(self.base_url, url)

    def append_access_token(self, headers: dict) -> dict:
        current_time = datetime.now()
        if current_time - self.refreshed_at > self.refresh_time:
            logger.info("refresh access token at: {}", current_time)
            self.access_token = self.get_access_token()
            self.refreshed_at = current_time

        headers["Authorization"] = f"Bearer {self.access_token}"

        return headers

    def get_access_token(self) -> str:
        url = self.build_url("/v1/oauth/token")

        data = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
        }

        auth_token = b64encode(f"{self.client_id}:{self.client_secret}")
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {auth_token}",
        }

        resp = httpx.post(url=url, data=data, headers=headers)
        resp.raise_for_status()

        data: dict = resp.json()
        return data.get("access_token")

    def get_quote(
        self, symbols: list[str], fields: list[QuoteField] | None = None, indicative: bool = False
    ) -> dict[str, QuoteResponse]:
        if fields is None:
            fields = ["quote", "reference"]

        url = self.build_url("/marketdata/v1/quotes")

        params = {
            "symbols": ",".join(symbols),
            "fields": ",".join(fields),
            "indicative": indicative,
        }

        headers = {"accept": "application/json"}
        headers = self.append_access_token(headers)

        resp = httpx.get(url=url, params=params, headers=headers)
        resp.raise_for_status()

        data = resp.json()

        if "errors" in data:
            raise httpx.HTTPError(str(data["errors"]))

        return {k: QuoteResponse.model_validate(v) for k, v in data.items()}
