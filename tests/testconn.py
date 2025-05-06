import os
from dotenv import load_dotenv
import odoorpc

# Load environment variables
load_dotenv()

class OdooTester:
    @staticmethod
    def test_connection():
        try:
            print("🔄 Attempting Odoo connection...")
            
            # Establish connection
            odoo = odoorpc.ODOO(
                os.getenv('ODOO_URL'),
                port=int(os.getenv('ODOO_PORT', 8069)),
                protocol=os.getenv('ODOO_PROTOCOL', 'jsonrpc')
            )
            
            # Login
            odoo.login(
                os.getenv('ODOO_DB'),
                os.getenv('ODOO_ADMIN_LOGIN'),
                os.getenv('ODOO_ADMIN_PASSWORD')
            )
            
            # Verify connection
            user = odoo.env.user
            print(f"✅ Successfully connected to Odoo {odoo.version} as {user.name}")
            print(f"🔑 Permissions: {user.groups_id.mapped('name')}")
            
            return True
            
        except Exception as e:
            print(f"❌ Connection failed: {str(e)}")
            return False

if __name__ == "__main__":
    OdooTester.test_connection()