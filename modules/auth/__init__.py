from .email_verification import setup_email_verification  # Now matches
from .user_registry import setup_user_registry
from .handlers import AuthHandlers
from .services import AuthService

__all__ = [
    'AuthHandlers', 
    'AuthService',
    'setup_auth_handlers'
]

def setup_auth_handlers(app, container):
    """Central entry point for auth module handlers"""
    # Initialize core services
    auth_service = AuthService(container.auth_repository)
    
    # Register handlers
    setup_email_verification(app, auth_service)
    setup_user_registry(app, container.storage)
    
    # Initialize and register handler classes
    auth_handlers = AuthHandlers(auth_service)
    auth_handlers.register(app)