"""Database connection and query utilities."""
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    """Create database connection."""
    DB_URL = os.getenv('DATABASE_URL')
    if not DB_URL:
        raise ValueError("DATABASE_URL environment variable is not set")
    return create_engine(DB_URL) 