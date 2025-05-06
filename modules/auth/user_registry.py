from telegram.ext import CommandHandler, MessageHandler, filters
from utils.error_handlers import handle_errors

def setup_user_registry(app, storage):
    """Register user registry-related handlers"""
    from .services import UserRegistryService  # Local import to avoid circular dependency
    
    # Initialize service
    user_registry = UserRegistryService(storage)
    
    # Register handlers
    app.add_handler(CommandHandler("register", handle_registration))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_input))

@handle_errors
async def handle_registration(update, context):
    await update.message.reply_text("👤 Starting registration...")
    # Your registration logic here

@handle_errors
async def handle_user_input(update, context):
    # Process user input for registration
    pass