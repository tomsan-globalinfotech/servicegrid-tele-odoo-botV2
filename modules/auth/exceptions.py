from core.errors import OdooIntegrationError

class InvalidOTPError(OdooIntegrationError):
    def __init__(self):
        super().__init__(
            "Invalid OTP provided",
            user_message="❌ Invalid verification code"
        )

class EmailNotRegisteredError(OdooIntegrationError):
    def __init__(self, email: str):
        super().__init__(
            f"Email not found: {email}",
            user_message="❌ This email isn't registered in our system"
        )