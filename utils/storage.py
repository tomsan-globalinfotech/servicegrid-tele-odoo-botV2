# utils/storage.py
import sqlite3
from typing import Optional, Dict, Any
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class SQLiteStorage:
    def __init__(self, db_path: str = "bot_storage.db"):
        self.db_path = Path(db_path)
        self.conn = self._create_connection()
        self._init_db()

    def _create_connection(self) -> sqlite3.Connection:
        """Create and return a database connection."""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # Enable dict-like access
            return conn
        except sqlite3.Error as e:
            logger.error(f"Database connection failed: {e}")
            raise RuntimeError("Could not initialize database") from e

    def _init_db(self) -> None:
        """Initialize database schema."""
        with self.conn:
            self.conn.executescript("""
                CREATE TABLE IF NOT EXISTS telegram_users (
                    telegram_id INTEGER PRIMARY KEY,
                    odoo_user_id INTEGER NOT NULL,
                    verified BOOLEAN DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                
                CREATE TABLE IF NOT EXISTS otp_verifications (
                    email TEXT PRIMARY KEY,
                    otp TEXT NOT NULL,
                    expires_at REAL NOT NULL,
                    telegram_id INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

    def link_user(self, telegram_id: int, odoo_user_id: int) -> None:
        """Link Telegram ID to Odoo user ID."""
        try:
            with self.conn:
                self.conn.execute("""
                    INSERT OR REPLACE INTO telegram_users 
                    (telegram_id, odoo_user_id, verified)
                    VALUES (?, ?, 1)
                """, (telegram_id, odoo_user_id))
        except sqlite3.Error as e:
            logger.error(f"Failed to link user: {e}")
            raise

    def get_odoo_user(self, telegram_id: int) -> Optional[Dict[str, Any]]:
        """Retrieve Odoo user ID for a Telegram user."""
        try:
            with self.conn:
                cursor = self.conn.execute("""
                    SELECT odoo_user_id FROM telegram_users 
                    WHERE telegram_id = ? AND verified = 1
                """, (telegram_id,))
                result = cursor.fetchone()
                return dict(result) if result else None
        except sqlite3.Error as e:
            logger.error(f"Failed to get Odoo user: {e}")
            return None

    def store_otp(self, email: str, otp: str, expires_at: float, telegram_id: int) -> None:
        """Store OTP verification data."""
        try:
            with self.conn:
                self.conn.execute("""
                    INSERT OR REPLACE INTO otp_verifications 
                    (email, otp, expires_at, telegram_id)
                    VALUES (?, ?, ?, ?)
                """, (email, otp, expires_at, telegram_id))
        except sqlite3.Error as e:
            logger.error(f"Failed to store OTP: {e}")
            raise

    def verify_otp(self, email: str, otp: str) -> bool:
        """Verify OTP and clean up expired entries."""
        try:
            with self.conn:
                # Cleanup expired OTPs first
                self.conn.execute("""
                    DELETE FROM otp_verifications 
                    WHERE expires_at < strftime('%s', 'now')
                """)
                
                cursor = self.conn.execute("""
                    SELECT otp FROM otp_verifications
                    WHERE email = ? AND expires_at >= strftime('%s', 'now')
                """, (email,))
                result = cursor.fetchone()
                return result and result['otp'] == otp
        except sqlite3.Error as e:
            logger.error(f"OTP verification failed: {e}")
            return False

    def close(self) -> None:
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")

    def __del__(self):
        """Ensure connection is closed when instance is destroyed."""
        self.close()