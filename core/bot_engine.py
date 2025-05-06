# core/bot_engine.py
from modules.auth import setup_auth_handlers
from modules.timesheets import setup_timesheet_handlers
from modules.tasks import setup_task_handlers  

class BotEngine:
    def __init__(self, container):
        self.app = container.bot_app
        self._setup_handlers(container)

    def _setup_handlers(self, container):
        setup_auth_handlers(self.app, container)
        setup_timesheet_handlers(self.app, container)
        setup_task_handlers(self.app, container)  