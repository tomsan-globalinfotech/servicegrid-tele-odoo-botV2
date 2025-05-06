import unittest
import sqlite3
import time
from pathlib import Path
from utils.storage import SQLiteStorage

class TestSQLiteStorage(unittest.TestCase):
    def setUp(self):
        """Create an in-memory database for testing"""
        self.storage = SQLiteStorage(":memory:")
        
    def test_user_linking(self):
        # Test valid user linking
        self.storage.link_user(12345, 67890)
        user = self.storage.get_odoo_user(12345)
        self.assertEqual(user['odoo_user_id'], 67890)
        self.assertEqual(user['verified'], 1)

        # Test user update
        self.storage.link_user(12345, 54321)
        updated_user = self.storage.get_odoo_user(12345)
        self.assertEqual(updated_user['odoo_user_id'], 54321)

    def test_nonexistent_user(self):
        user = self.storage.get_odoo_user(99999)
        self.assertIsNone(user)

    def test_otp_verification(self):
        # Test valid OTP flow
        email = "user@company.com"
        otp = "123456"
        expires_at = time.time() + 300  # 5 minutes from now
        
        self.storage.store_otp(email, otp, expires_at, 12345)
        self.assertTrue(self.storage.verify_otp(email, otp))
        
        # Test invalid OTP
        self.assertFalse(self.storage.verify_otp(email, "wrongotp"))

    def test_otp_expiration(self):
        email = "user@company.com"
        otp = "654321"
        expires_at = time.time() - 10  # Already expired
        
        self.storage.store_otp(email, otp, expires_at, 12345)
        self.assertFalse(self.storage.verify_otp(email, otp))

    def test_otp_cleanup(self):
        # Add expired and valid OTPs
        self.storage.store_otp("expired@test.com", "111111", time.time() - 100, 12345)
        self.storage.store_otp("valid@test.com", "222222", time.time() + 100, 12345)
        
        # Trigger cleanup by verifying
        self.storage.verify_otp("valid@test.com", "222222")
        
        # Check remaining records
        with self.storage.conn:
            cursor = self.storage.conn.execute(
                "SELECT COUNT(*) FROM otp_verifications"
            )
            count = cursor.fetchone()[0]
            self.assertEqual(count, 1)  # Only valid OTP remains

    def test_invalid_inputs(self):
        # Test invalid telegram_id type
        with self.assertRaises(TypeError):
            self.storage.link_user("invalid_id", 67890)

        # Test missing required fields
        with self.assertRaises(sqlite3.IntegrityError):
            with self.storage.conn:
                self.storage.conn.execute(
                    "INSERT INTO telegram_users (telegram_id) VALUES (?)",
                    (12345,)
                )

    def test_connection_management(self):
        # Test connection closure
        self.storage.close()
        with self.assertRaises(sqlite3.ProgrammingError):
            self.storage.conn.execute("SELECT 1")

if __name__ == "__main__":
    unittest.main()