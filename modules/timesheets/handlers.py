# modules/timesheets/handlers.py
from telegram.ext import CommandHandler

class TimesheetHandlers:
    def __init__(self, timesheet_service):
        self.service = timesheet_service

    def register(self, application):
        application.add_handler(CommandHandler("timesheet", self.handle_timesheet))
    
    async def handle_timesheet(self, update, context):
        await update.message.reply_text("🕒 Timesheet feature coming soon!")