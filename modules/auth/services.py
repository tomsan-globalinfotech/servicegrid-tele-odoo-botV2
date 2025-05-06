import random
from typing import Optional
from modules.auth.exceptions import InvalidOTPError

class AuthService:
    def __init__(self, repository, email_sender):
        self.repo = repository
        self.email_sender = email_sender

    async def initiate_verification(self, email: str, telegram_id: int) -> str:
        """Generate and send OTP"""
        employee = self.repo.find_employee_by_email(email)
        otp = str(random.randint(100000, 999999))
        await self.email_sender.send_otp(email, otp)
        self.repo.store_otp(email, otp, telegram_id)
        return otp

    def register_user(self, telegram_id, email):
        # Your user registration logic
        pass

    # ... other service methods