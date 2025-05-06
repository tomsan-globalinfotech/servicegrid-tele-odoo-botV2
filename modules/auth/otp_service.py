import random
import time
from typing import Dict, Tuple
from utils.storage import SQLiteStorage

class OTPService:
    def __init__(self, storage: SQLiteStorage):
        self.storage = storage

    def generate_otp(self, email: str, telegram_id: int) -> str:
        otp = str(random.randint(100000, 999999))
        expires_at = time.time() + 300  # 5 minutes expiry
        
        # Store in SQLite
        with self.storage.conn:
            self.storage.conn.execute("""
            INSERT OR REPLACE INTO otp_verifications 
            (email, otp, expires_at, telegram_id)
            VALUES (?, ?, ?, ?)
            """, (email, otp, expires_at, telegram_id))
        
        return otp

    def verify_otp(self, email: str, otp: str) -> bool:
        cursor = self.storage.conn.cursor()
        cursor.execute("""
        SELECT otp, expires_at FROM otp_verifications
        WHERE email = ? AND expires_at > ?
        """, (email, time.time()))
        
        record = cursor.fetchone()
        return record and record[0] == otp