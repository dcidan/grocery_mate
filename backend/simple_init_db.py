"""
Simple Database Initialization - Using psycopg2 directly to avoid encoding issues
"""
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine
from app.database import Base
from app.models import Ingredient, ShoppingList, ShoppingItem, Recipe
import logging
from urllib.parse import urlparse
import os
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://grocery_user:grocery_pass@localhost:5432/grocery_db"
)

def parse_db_url(url):
    """Parse database URL into components"""
    parsed = urlparse(url)
    return {
        'host': parsed.hostname or 'localhost',
        'port': parsed.port or 5432,
        'user': parsed.username or 'grocery_user',
        'password': parsed.password or 'grocery_pass',
        'database': parsed.path.lstrip('/') or 'grocery_db'
    }

def ensure_database_exists():
    """Ensure the database exists, create if it doesn't"""
    config = parse_db_url(DATABASE_URL)
    db_name = config['database']
    
    logger.info(f"Ensuring database '{db_name}' exists...")
    
    try:
        # Connect to postgres database with UTF-8 encoding
        conn = psycopg2.connect(
            host=config['host'],
            port=config['port'],
            user=config['user'],
            password=config['password'],
            database='postgres',
            client_encoding='utf8'
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s",
            (db_name,)
        )
        
        if cursor.fetchone():
            logger.info(f"✅ Database '{db_name}' already exists")
        else:
            # Create database
            logger.info(f"Creating database '{db_name}'...")
            cursor.execute(f'CREATE DATABASE "{db_name}" ENCODING "UTF8"')
            logger.info(f"✅ Database '{db_name}' created successfully")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        logger.error(f"❌ Error with database: {e}")
        return False

def create_tables():
    """Create all tables using SQLAlchemy"""
    try:
        logger.info("Creating/verifying tables...")
        
        # Create engine with UTF-8 encoding
        engine = create_engine(
            DATABASE_URL,
            client_encoding='utf8',
            connect_args={'client_encoding': 'utf8'}
        )
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        
        # Verify tables were created
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        engine.dispose()
        
        logger.info(f"✅ Tables ready ({len(tables)} tables): {', '.join(tables)}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error creating tables: {e}")
        return False

def init_database_simple():
    """Simple database initialization"""
    logger.info("=" * 60)
    logger.info("DATABASE INITIALIZATION (SIMPLE)")
    logger.info("=" * 60)
    
    try:
        # Step 1: Ensure database exists
        if not ensure_database_exists():
            return False
        
        # Step 2: Create tables
        if not create_tables():
            return False
        
        logger.info("=" * 60)
        logger.info("✅ DATABASE INITIALIZATION COMPLETE")
        logger.info("=" * 60)
        return True
        
    except Exception as e:
        logger.error(f"❌ Initialization failed: {e}")
        return False

if __name__ == "__main__":
    init_database_simple()