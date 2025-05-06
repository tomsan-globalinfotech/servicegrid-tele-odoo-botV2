# main.py
from core.dependencies import Container, Config
from core.errors import OdooIntegrationError, BotBaseError
import logging
import sys
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_container() -> Container:
    try:
        config = Config(
            telegram_token=os.getenv("TELEGRAM_TOKEN"),
            odoo_url=os.getenv("ODOO_URL"),
            odoo_db=os.getenv("ODOO_DB"),
            odoo_admin_login=os.getenv("ODOO_ADMIN_LOGIN"),
            odoo_admin_password=os.getenv("ODOO_ADMIN_PASSWORD")
        )
        return Container(config)
    except OdooIntegrationError as e:
        logger.critical(f"Odoo Configuration Error: {e.message}")
        sys.exit(1)
    except Exception as e:
        logger.critical(f"Unexpected Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    container = init_container()
    logger.info("All services initialized successfully")