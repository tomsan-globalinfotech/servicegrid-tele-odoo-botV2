# handlers/base.py
from telegram import Update
from telegram.error import TelegramError
from core.errors import BotBaseError  # Updated import
from utils.error_handlers import handle_errors  # Add this import

class SafeHandler:
    @staticmethod
    @handle_errors
    async def send_message(update: Update, text: str):
        try:
            await update.message.reply_text(text)
        except TelegramError as e:
            raise BotBaseError(
                f"Telegram API error: {str(e)}",
                user_message="📢 Message sending failed"
            )