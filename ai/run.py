"""
Skill Lantern AI - Application Runner
"""

import uvicorn
from config.settings import settings


def main():
    """Run the FastAPI application"""
    print("\n" + "=" * 60)
    print("🚀 Starting Skill Lantern AI Backend")
    print("=" * 60)
    print(f"\n📍 Server: http://{settings.host}:{settings.port}")
    print(f"📚 API Docs: http://{settings.host}:{settings.port}/docs")
    print(f"🔧 Environment: {settings.environment}")
    print("\n" + "=" * 60 + "\n")
    
    uvicorn.run(
        "api.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )


if __name__ == "__main__":
    main()
