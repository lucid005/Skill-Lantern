"""
Skill Lantern AI - FastAPI Application Entry Point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from config.settings import settings
from api.routes import predict, careers, health


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager - runs on startup and shutdown"""
    # Startup
    print("🚀 Starting Skill Lantern AI Backend...")
    print(f"📊 Environment: {settings.environment}")
    print(f"🔧 Debug mode: {settings.debug}")
    
    # Load models on startup
    from core.ml_predictor import MLPredictor
    app.state.ml_predictor = MLPredictor()
    print("✅ ML Predictor loaded")
    
    from core.career_matcher import CareerMatcher
    app.state.career_matcher = CareerMatcher()
    print("✅ Career Matcher loaded")
    
    yield
    
    # Shutdown
    print("👋 Shutting down Skill Lantern AI Backend...")


# Create FastAPI application
app = FastAPI(
    title="Skill Lantern AI",
    description="Career recommendation system powered by machine learning",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.frontend_url,
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(careers.router, prefix="/api/v1", tags=["Careers"])
app.include_router(predict.router, prefix="/api/v1", tags=["Predictions"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "Skill Lantern AI",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )
