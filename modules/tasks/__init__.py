# modules/tasks/__init__.py
from .listing import setup_task_listing_handlers
from .management import setup_task_management_handlers

def setup_task_handlers(app, container):
    """Central export point for all task-related handlers"""
    setup_task_listing_handlers(app, container)
    setup_task_management_handlers(app, container)