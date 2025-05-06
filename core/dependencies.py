import os
import odoorpc
from typing import NamedTuple
from telegram.ext import Application
from utils.storage import SQLiteStorage
from core.errors import OdooIntegrationError

# Auth module imports
from modules.auth.services import AuthService
from modules.auth.repository import AuthRepository
from modules.auth.handlers import AuthHandlers

# Timesheets module imports
from modules.timesheets.handlers import TimesheetHandlers

class Config(NamedTuple):
    telegram_token: str
    odoo_url: str
    odoo_db: str
    odoo_admin_login: str
    odoo_admin_password: str
    otp_expiry_seconds: int = 300  # 5 minutes by default

class Container:
    def __init__(self, config: Config):
        self.config = config
        
        # Core infrastructure
        self.storage = SQLiteStorage()
        self.odoo = self._init_odoo()
        self.bot_app = Application.builder().token(config.telegram_token).build()
        self.auth_handlers = AuthHandlers(self.auth_service)
        self.timesheet_handlers = TimesheetHandlers(self.timesheet_service)
        # Auth module dependencies
        self._init_auth_module()

    def _init_odoo(self):
        """Initialize Odoo connection with error handling"""
        try:
            odoo = odoorpc.ODOO(
                self.config.odoo_url,
                port=8069,
                protocol='jsonrpc',
                timeout=120
            )
            odoo.login(
                self.config.odoo_db,
                self.config.odoo_admin_login,
                self.config.odoo_admin_password
            )
            
            if 'x_telegram_id' not in odoo.env['hr.employee'].fields_get():
                raise OdooIntegrationError("Missing x_telegram_id field in hr.employee")
                
            return odoo
        except odoorpc.error.RPCError as e:
            raise OdooIntegrationError(f"Odoo RPC error: {str(e)}")
        except Exception as e:
            raise OdooIntegrationError(f"Connection failed: {str(e)}")

    def _init_auth_module(self):
        """Initialize authentication module components"""
        # Repository (data access)
        self.auth_repo = AuthRepository(
            odoo=self.odoo,
            storage=self.storage,
            otp_expiry=self.config.otp_expiry_seconds
        )
        
        # Business logic
        self.auth_service = AuthService(
            repository=self.auth_repo,
            email_sender=self._get_email_sender()  # Implement this
        )
        
        # Telegram handlers
        self.auth_handlers = AuthHandlers(service=self.auth_service)

    def _get_email_sender(self):
        """Lazy initialization of email service"""
        # Implement your email/SMS service here
        return ConsoleEmailSender()  # Default for development
   
    def register_handlers(self):
        from handlers import register_all_handlers
        register_all_handlers(self.bot_app, self)
class ConsoleEmailSender:
    """Mock email sender for development"""
    async def send_otp(self, email: str, otp: str):
        print(f"[DEV] OTP for {email}: {otp}")