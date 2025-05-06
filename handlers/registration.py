# handlers/registration.py
from telegram import Update
from modules.auth.services import EmailAuth

async def handle_telegram_link(update: Update, context):
    telegram_id = update.effective_user.id
    email = context.user_data['pending_email']
    
    auth = EmailAuth(context.bot_data['odoo'], context.bot_data['storage'])
    if await auth.confirm_verification(email, telegram_id):
        await update.message.reply_text(
            "✅ Successfully linked to your Odoo account!\n"
            f"Your Telegram ID: {telegram_id} is now associated with {email}"
        )
    else:
        await update.message.reply_text("❌ Failed to update Odoo record")