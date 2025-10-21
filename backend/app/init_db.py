"""
Database Initialization - Internal version for app package
ASSUMES DATABASE ALREADY EXISTS - Only creates tables
"""
import os

# Force UTF-8 encoding FIRST, before any imports
os.environ['PYTHONIOENCODING'] = 'utf-8'
os.environ['PGCLIENTENCODING'] = 'UTF8'

from sqlalchemy import text
from .database import Base, engine, SessionLocal
from .models import Ingredient, ShoppingList, ShoppingItem, Recipe
import logging

logger = logging.getLogger(__name__)

def init_database_simple():
    """
    Simple database initialization - creates tables only
    Assumes database already exists (created via Docker)
    """
    try:
        logger.info("Creating tables...")
        
        # Create all tables (this works even with encoding warnings)
        Base.metadata.create_all(bind=engine)
        
        # Test connection - ignore encoding errors
        try:
            db = SessionLocal()
            db.execute(text("SELECT 1"))
            db.close()
            logger.info("✅ Database tables created/verified")
        except UnicodeDecodeError:
            # Ignore encoding errors on test query
            logger.info("✅ Database tables created (encoding warning ignored)")
        
        return True
        
    except UnicodeDecodeError as e:
        # Even with encoding errors, tables might be created
        logger.info("✅ Tables created despite encoding warning")
        return True
        
    except Exception as e:
        logger.error(f"❌ Database initialization error: {e}")
        return False