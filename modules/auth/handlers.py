# modules/auth/handlers.py
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

class AuthHandlers:
    def __init__(self, auth_service):
        self.service = auth_service

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("🔑 Welcome! Use /login")

    def register(self, application):
        application.add_handler(CommandHandler("start", self.start))