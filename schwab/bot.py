from __future__ import annotations

import os

from telegram import Update
from telegram.ext import Application
from telegram.ext import CommandHandler
from telegram.ext import ContextTypes

from .client import Client
from .quote import QuoteRequest


class SchwabBot:
    def __init__(self, client: Client, token: str, chat_id: str) -> None:
        self.client = client

        self.app = Application.builder().token(token).build()
        self.app.add_handler(CommandHandler("show_chats", self.show_chats))
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
        return cls(client=client, token=token, chat_id=chat_id)

    async def quote(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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

    async def show_chats(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Shows which chats the bot is in"""
        user_ids = ", ".join(str(uid) for uid in context.bot_data.setdefault("user_ids", set()))
        group_ids = ", ".join(str(gid) for gid in context.bot_data.setdefault("group_ids", set()))
        channel_ids = ", ".join(str(cid) for cid in context.bot_data.setdefault("channel_ids", set()))
        text = (
            f"@{context.bot.username} is currently in a conversation with the user IDs {user_ids}."
            f" Moreover it is a member of the groups with IDs {group_ids} "
            f"and administrator in the channels with IDs {channel_ids}."
        )
        await update.effective_message.reply_text(text)
