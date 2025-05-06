from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, filters
from telegram import Update
from shared.keyboards import TimesheetKeyboards
from modules.timesheets.creation import start_timesheet
from shared.constants import TimesheetStates

async def handle_project_selection(update: Update, context):
    query = update.callback_query
    await query.answer()
    project_id = int(query.data.split("_")[1])
    
    # Store project ID in context
    context.user_data['project_id'] = project_id
    
    # Show tasks keyboard
    keyboard = TimesheetKeyboards.tasks(context.bot_data['odoo_conn'], project_id)
    await query.edit_message_text(
        "📝 Select task:",
        reply_markup=keyboard
    )
    return TimesheetStates.TASK_SELECT.value

def setup_timesheet_handlers(application, container):
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('timesheet', start_timesheet)],
        states={
            TimesheetStates.PROJECT_SELECT.value: [
                MessageHandler(filters.TEXT, handle_project_selection)
            ],
            TimesheetStates.TASK_SELECT.value: [
                # Add task selection handler
            ]
        },
        fallbacks=[CommandHandler('cancel', lambda u,c: ConversationHandler.END)]
    )
    
    application.add_handler(conv_handler)