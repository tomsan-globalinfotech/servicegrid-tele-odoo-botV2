# utils/error_handler.py
from core.errors import BotBaseError
from telegram import Update
import logging

logger = logging.getLogger(__name__)

def handle_errors(f):
    async def wrapper(update: Update, context, *args, **kwargs):
        try:
            return await f(update, context, *args, **kwargs)
        except BotBaseError as e:
            await update.message.reply_text(e.user_message)
            logger.warning(f"Handled error: {e.message}")
        except Exception as e:
            await update.message.reply_text("⚠️ Internal server error")
            logger.error(f"Unhandled exception: {str(e)}", exc_info=True)
    return wrapper