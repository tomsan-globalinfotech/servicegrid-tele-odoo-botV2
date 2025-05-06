from typing import Optional
from core.errors import OdooIntegrationError
from modules.auth.exceptions import EmailNotRegisteredError

class AuthRepository:
    def __init__(self, odoo, storage, otp_expiry: int):
        self.odoo = odoo
        self.storage = storage
        self.otp_expiry = otp_expiry

    def find_employee_by_email(self, email: str) -> dict:
        """Odoo query with error handling"""
        employees = self.odoo.env['hr.employee'].search_read(
            [('work_email', '=', email)],
            ['id', 'name'],
            limit=1
        )
        if not employees:
            raise EmailNotRegisteredError(email)
        return employees[0]

    # ... other data access methods