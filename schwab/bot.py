from __future__ import annotations

import os

from loguru import logger
from telegram import Update
from telegram.ext import Application
from telegram.ext import CommandHandler
from telegram.ext import ContextTypes

from .client import Client


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
        chat_id = str(update.message.chat_id)
        if chat_id not in self.chat_ids:
            logger.info("chat_id: {} is not in the whitelist, skip")
            return

        symbols = update.message.text.lstrip("/cs").strip().upper().split(" ")

        resp = self.client.query_quotes(symbols)

        reply_text = "\n".join([str(v) for v in resp.values()])

        await update.message.reply_text(reply_text)

    async def show_chat_id(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text(update.message.chat_id)
