import odoorpc
import os
from dotenv import load_dotenv

load_dotenv()

try:
    odoo = odoorpc.ODOO(
        os.getenv('ODOO_URL'),
        port=8069,
        protocol='jsonrpc'
    )
    odoo.login(
        os.getenv('ODOO_DB'),
        os.getenv('ODOO_ADMIN_LOGIN'),
        os.getenv('ODOO_ADMIN_PASSWORD')
    )
    print("✅ Connection successful!")
    print("Odoo version:", odoo.version)
except Exception as e:
    print("❌ Connection failed:", str(e))