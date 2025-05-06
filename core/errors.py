class BotBaseError(Exception):
    """Base exception for all bot errors"""
    def __init__(self, message="", user_message=None):
        self.message = message
        self.user_message = user_message or "❌ An error occurred"
        super().__init__(self.message)

class OdooIntegrationError(BotBaseError):
    """Base class for Odoo-related errors"""
    def __init__(self, message="", user_message=None):
        user_message = user_message or "🔌 Odoo operation failed"
        super().__init__(message, user_message)

# Add these specific error classes
class EmailNotRegisteredError(OdooIntegrationError):
    def __init__(self, email: str):
        super().__init__(
            f"Email not found: {email}",
            user_message="❌ This email isn't registered in our system"
        )

class InvalidOTPError(OdooIntegrationError):
    def __init__(self):
        super().__init__(
            "Invalid OTP provided",
            user_message="❌ Invalid verification code"
        )

class TelegramFieldMissingError(OdooIntegrationError):
    def __init__(self):
        super().__init__(
            "Custom field x_telegram_id not found in hr.employee",
            user_message="❌ System misconfigured - contact admin"
        )