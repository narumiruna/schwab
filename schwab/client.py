from __future__ import annotations

import base64
import os
from urllib.parse import urljoin

import httpx

from .quote import QuoteRequest
from .quote import QuoteResponse

BASE_URL = "https://api.schwabapi.com/"


def b64encode(s: str) -> str:
    return base64.b64encode(s.encode()).decode()


class Client:
    def __init__(self, client_id: str, client_secret: str, refresh_token: str) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token

        self.http_client = httpx.Client()
        self.headers = {}

        self.auth()

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

    def auth(self) -> None:
        url = urljoin(BASE_URL, "/v1/oauth/token")

        auth_token = b64encode(f"{self.client_id}:{self.client_secret}")
        resp = httpx.post(
            url=url,
            data={
                "grant_type": "refresh_token",
                "refresh_token": self.refresh_token,
            },
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": f"Basic {auth_token}",
            },
        )

        data: dict = resp.json()
        access_token = data.get("access_token")

        self.http_client.headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

    def get_quote(self, req: QuoteRequest) -> dict[str, QuoteResponse]:
        url = urljoin(BASE_URL, "/marketdata/v1/quotes")
        params = {
            "symbols": ",".join(req.symbols),
            "fields": ",".join(req.fields),
            "indicative": req.indicative,
        }

        resp = self.http_client.get(url=url, params=params)
        resp.raise_for_status()

        data = resp.json()

        if "errors" in data:
            raise httpx.HTTPError(str(data["errors"]))

        return {k: QuoteResponse.model_validate(v) for k, v in data.items()}
