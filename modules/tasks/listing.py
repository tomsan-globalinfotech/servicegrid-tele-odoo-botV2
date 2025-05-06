# modules/tasks/listing.py
from telegram.ext import CommandHandler
from shared.keyboards import TaskKeyboards

def setup_task_listing_handlers(app, container):
    @app.add_handler(CommandHandler("mytasks", handle_my_tasks))
    async def handle_my_tasks(update, context):
        employee_id = container.user_registry.get_employee_id(update.effective_user.id)
        tasks = container.odoo.env['project.task'].search_read(
            [('user_id', '=', employee_id)],
            ['name', 'stage_id']
        )
        
        await update.message.reply_text(
            "📋 Your Tasks:",
            reply_markup=TaskKeyboards.task_list(tasks)
        )