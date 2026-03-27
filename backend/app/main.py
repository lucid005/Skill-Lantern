"""
Skill Lantern Backend - FastAPI Application
AI-Powered Career Guidance System

Main entry point for the FastAPI backend.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.config import settings
from app.models.schemas import HealthResponse
from app.routers import career, roadmap, colleges, recommendations
from app.services.gemini_service import gemini_service
from app.services.college_service import college_service
from app.models.career_predictor import career_predictor

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan handler.
    Runs on startup and shutdown.
    """
    # Startup
    logger.info("🚀 Starting Skill Lantern Backend...")
    
    # Load college data
    logger.info("📚 Loading college data...")
    if college_service.load_data():
        logger.info("✅ College data loaded successfully")
    else:
        logger.warning("⚠️ Failed to load college data - check CSV path")
    
    # Load career data
    logger.info("📊 Loading career data...")
    if career_predictor.load_career_data():
        logger.info("✅ Career data loaded successfully")
    else:
        logger.warning("⚠️ Failed to load career data - using rule-based prediction")
    
    # Try to load XGBoost model
    logger.info("🤖 Loading XGBoost model...")
    if career_predictor.load_model():
        logger.info("✅ XGBoost model loaded")
    else:
        logger.info("ℹ️ Using rule-based prediction (XGBoost model not found)")
    
    # Check Gemini API connection
    logger.info("🔗 Checking Gemini API connection...")
    if await gemini_service.check_health():
        logger.info(f"✅ Gemini API is connected (model: {settings.gemini_model})")
    else:
        logger.warning("⚠️ Gemini API is not accessible - LLM features will be limited")
    
    logger.info("✨ Skill Lantern Backend is ready!")
    
    yield
    
    # Shutdown
    logger.info("👋 Shutting down Skill Lantern Backend...")


# Create FastAPI app
app = FastAPI(
    title="Skill Lantern API",
    description="""
    AI-Powered Career Guidance System for Nepal
    
    ## Features
    
    * **Career Prediction** - XGBoost-based career recommendations
    * **Career Roadmap** - LLaMA-generated learning paths
    * **College Recommendations** - Nepal college suggestions
    * **Full Guidance** - Complete career assessment
    
    ## Tech Stack
    
    * FastAPI + Python
    * XGBoost for career prediction
    * Google Gemini for LLM inference
    * Nepal college dataset
    """,
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(career.router, prefix="/api")
app.include_router(roadmap.router, prefix="/api")
app.include_router(colleges.router, prefix="/api")
app.include_router(recommendations.router, prefix="/api")


# Root endpoints
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint - API information."""
    return {
        "name": "Skill Lantern API",
        "version": "1.0.0",
        "description": "AI-Powered Career Guidance System for Nepal",
        "docs": "/docs",
        "health": "/api/health"
    }


@app.get("/api/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint.
    
    Returns status of:
    - API server
    - Gemini API connection
    - XGBoost model
    """
    gemini_healthy = await gemini_service.check_health()
    
    return HealthResponse(
        status="healthy",
        gemini_status="connected" if gemini_healthy else "disconnected",
        model_loaded=career_predictor.model_loaded,
        version="1.0.0"
    )


@app.get("/api/config", tags=["Config"])
async def get_config():
    """Get non-sensitive configuration info."""
    return {
        "gemini_model": settings.gemini_model,
        "debug": settings.debug
    }


# Run with uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
