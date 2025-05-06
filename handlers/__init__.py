# handlers/__init__.py
from .auth import setup_auth_handlers
from .timesheets import setup_timesheet_handlers

def register_all_handlers(application, container):
    setup_auth_handlers(application, container)
    setup_timesheet_handlers(application, container)