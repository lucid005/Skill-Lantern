"""
Roadmap Router - Career Roadmap Generation Endpoints
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
import json
import logging

from app.models.schemas import (
    RoadmapRequest,
    RoadmapResponse,
    ErrorResponse
)
from app.services.roadmap_service import roadmap_service
from app.services.ollama_service import ollama_service
from app.prompts.roadmap_prompts import ROADMAP_SYSTEM_PROMPT, get_roadmap_user_prompt

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/roadmap", tags=["Career Roadmap"])


@router.post(
    "/generate",
    response_model=RoadmapResponse,
    responses={500: {"model": ErrorResponse}}
)
async def generate_roadmap(request: RoadmapRequest):
    """
    Generate a detailed career roadmap using LLaMA/Ollama.
    
    Returns a structured roadmap with:
    - Career overview
    - Beginner → Intermediate → Advanced stages
    - Skills, resources, and milestones for each stage
    - Tools and technologies
    - Job roles and growth paths
    """
    try:
        roadmap = await roadmap_service.generate_roadmap(
            career_name=request.career_name,
            user_profile=request.user_profile
        )
        return roadmap
        
    except Exception as e:
        logger.error(f"Roadmap generation failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate roadmap: {str(e)}"
        )


@router.post("/generate/stream")
async def generate_roadmap_stream(request: RoadmapRequest):
    """
    Generate roadmap with streaming response.
    Returns Server-Sent Events (SSE) stream.
    """
    async def generate():
        try:
            # Build prompt
            user_prompt = get_roadmap_user_prompt(
                career_name=request.career_name,
                education_level=request.user_profile.education_level.value,
                skills=request.user_profile.skills,
                interests=request.user_profile.interests,
                preferences=request.user_profile.preferences
            )
            
            # Stream response
            async for chunk in ollama_service.generate_stream(
                prompt=user_prompt,
                system_prompt=ROADMAP_SYSTEM_PROMPT
            ):
                yield f"data: {json.dumps({'text': chunk})}\n\n"
            
            yield "data: [DONE]\n\n"
            
        except Exception as e:
            logger.error(f"Stream generation failed: {e}")
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive"
        }
    )
