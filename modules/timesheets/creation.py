# modules/timesheets/creation.py
from shared.constants import TimesheetStates
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from shared.keyboards import TimesheetKeyboards  # Updated import

async def start_timesheet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Entry point for timesheet creation"""
    try:
        # Get Odoo connection from bot data
        odoo_conn = context.bot_data['odoo_conn']
        
        # Generate projects keyboard
        keyboard = TimesheetKeyboards.projects(odoo_conn)
        
        # Send message with keyboard
        await update.message.reply_text(
            "🏗 Select a project:",
            reply_markup=keyboard  # Use the generated keyboard directly
        )
        return TimesheetStates.PROJECT_SELECT.value
        
    except Exception as e:
        await update.message.reply_text("🚧 Couldn't load projects")
        return ConversationHandler.END