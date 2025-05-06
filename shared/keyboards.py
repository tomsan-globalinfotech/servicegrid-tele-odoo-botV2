# shared/keyboards.py
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

class TimesheetKeyboards:
    @staticmethod
    def projects(odoo_conn, active_only=True):
        """Generate projects keyboard with optional active filter"""
        Project = odoo_conn.env['project.project']
        domain = [('active', '=', True)] if active_only else []
        projects = Project.search_read(
            domain,
            ['name'],
            limit=10
        )
        buttons = [
            [InlineKeyboardButton(p['name'], callback_data=f"project_{p['id']}")]
            for p in projects
        ]
        return InlineKeyboardMarkup(buttons)

    @staticmethod
    def tasks(odoo_conn, project_id):
        """Generate tasks keyboard for a specific project"""
        Task = odoo_conn.env['project.task']
        tasks = Task.search_read(
            [('project_id', '=', project_id)],
            ['name'],
            limit=10
        )
        buttons = [
            [InlineKeyboardButton(t['name'], callback_data=f"task_{t['id']}")]
            for t in tasks
        ]
        return InlineKeyboardMarkup(buttons)