# handlers/auth.py
from modules.auth.handlers import AuthHandlers

def setup_auth_handlers(application, container):
    handlers = AuthHandlers(container.auth_service)
    handlers.register(application)