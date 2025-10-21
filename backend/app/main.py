from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import ingredients, shopping_lists, recipes
from .init_db import init_database_simple
import logging
import sys
import os

# Configure loggingg
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="GroceryMate API",
    description="API for managing groceries, shopping lists, and recipes",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database on application startup"""
    logger.info("Starting GroceryMate API...")
    
    try:
        # Try simple initialization first
        success = init_database_simple()
        if success:
            logger.info("✅ Database ready")
        else:
            # Fall back to trying the advanced init
            logger.warning("Simple init failed, trying advanced init...")
            backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            if backend_dir not in sys.path:
                sys.path.insert(0, backend_dir)
            
            try:
                import simple_init_db
                success = simple_init_db.init_database_simple()
                if success:
                    logger.info("✅ Database ready (via simple_init_db)")
                else:
                    logger.error("❌ Database initialization failed")
            except Exception as e2:
                logger.error(f"❌ All initialization methods failed: {e2}")
    except Exception as e:
        logger.error(f"❌ Error during database initialization: {e}")
        logger.warning("⚠️  Continuing without database initialization")
    
    logger.info("GroceryMate API ready!")

# Include routers
app.include_router(ingredients.router)
app.include_router(shopping_lists.router)
app.include_router(recipes.router)

@app.get("/")
def read_root():
    return {
        "message": "Welcome to GroceryMate API",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}