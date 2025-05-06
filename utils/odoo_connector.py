# utils/odoo_connector.py
import odoorpc  # Add missing import
from core.errors import OdooIntegrationError  # Corrected import
from utils.error_handlers import handle_errors  # Add import

class OdooConnector:
    def __init__(self, config):
        self.config = config

    @handle_errors
    def get_connection(self):
        """Connect to Odoo with error handling"""
        try:
            odoo = odoorpc.ODOO(
                self.config.odoo_url,
                port=8069,
                protocol='jsonrpc'
            )
            odoo.login(
                self.config.odoo_db,
                self.config.odoo_admin_login,
                self.config.odoo_admin_password
            )
            return odoo
        except odoorpc.error.RPCError as e:
            raise OdooIntegrationError(
                f"Odoo connection failed: {str(e)}",
                user_message="🔌 Couldn't connect to company systems"
            )