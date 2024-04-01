from __future__ import annotations

import os

from telegram import Update
from telegram.ext import Application
from telegram.ext import CommandHandler
from telegram.ext import ContextTypes

from .client import Client
from .quote import QuoteRequest


class SchwabBot:
    def __init__(self, client: Client, token: str, chat_ids: list[str]) -> None:
        self.client = client
        self.chat_ids = chat_ids

        self.app = Application.builder().token(token).build()
        self.app.add_handler(CommandHandler("chat_id", self.show_chat_id))
        self.app.add_handler(CommandHandler("cs", self.quote))
        self.app.run_polling(allowed_updates=Update.ALL_TYPES)

    @classmethod
    def from_env(cls):
        client = Client.from_env()

        token = os.getenv("BOT_TOKEN")
        if token is None:
            raise ValueError("BOT_TOKEN is not set")

        chat_id = os.getenv("BOT_CHAT_ID")
        if chat_id is None:
            raise ValueError("BOT_CHAT_ID is not set")

        return cls(client=client, token=token, chat_ids=chat_id.split(","))

    async def quote(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if str(update.message.chat_id) not in self.chat_ids:
            return

        s = update.message.text.lstrip("/cs").strip().upper()

        req = QuoteRequest(symbols=s.split(" "))
        resp = self.client.get_quote(req)

        reply_text = ""
        for symbol, data in resp.items():
            reply_text += (
                f"▪️Symbol: {symbol}\n"
                f"▪️Type: {data.asset_main_type}\n"
                f"▪️Last: {data.quote.last_price} "
                f"▪️Net Change: {data.quote.net_percent_change}\n"
                f"▪️52 Week High: {data.quote.field_52_week_high} "
                f"▪️52 Week Low: {data.quote.field_52_week_low}\n"
                "\n"
            )
        await update.message.reply_text(reply_text)

    async def show_chat_id(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text(update.message.chat_id)
