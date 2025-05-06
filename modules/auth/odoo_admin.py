import os
import odoorpc
from dotenv import load_dotenv
from functools import lru_cache

load_dotenv()

class OdooAdminAuth:
    @staticmethod
    @lru_cache(maxsize=1)  # Cache the connection
    def get_connection():
        try:
            odoo = odoorpc.ODOO(
                os.getenv('ODOO_URL'),
                port=int(os.getenv('ODOO_PORT', 8069)),
                protocol=os.getenv('ODOO_PROTOCOL', 'jsonrpc'),
                timeout=120  # 2 minutes timeout
            )
            odoo.login(
                os.getenv('ODOO_DB'),
                os.getenv('ODOO_ADMIN_LOGIN'),
                os.getenv('ODOO_ADMIN_PASSWORD')
            )
            return odoo
        except Exception as e:
            raise ConnectionError(f"Odoo connection failed: {str(e)}")