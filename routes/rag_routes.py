"""
FastAPI routes for RAG-powered music knowledge queries
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import logging

from rag_service import rag_system

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/rag", tags=["rag"])

# ===== REQUEST/RESPONSE MODELS =====

class RAGQueryRequest(BaseModel):
    """RAG query request"""
    question: str
    include_sources: bool = True

class RAGMoodSearchRequest(BaseModel):
    """Search ragas by mood"""
    mood: str
    limit: int = 3

class RAGInstrumentSearchRequest(BaseModel):
    """Search instruments by category"""
    category: str
    limit: int = 5

class RAGFusionRecommendRequest(BaseModel):
    """Get fusion style recommendation"""
    preferences: str

# ===== ENDPOINTS =====

@router.post("/query")
async def rag_query(request: RAGQueryRequest):
    """
    Ask any question about ragas, instruments, or fusion styles.
    Uses RAG to retrieve relevant information and generate accurate answers.
    """
    try:
        logger.info(f"🎵 RAG query received: {request.question}")
        
        result = rag_system.query(
            question=request.question,
            include_sources=request.include_sources
        )
        
        return {
            "status": "success",
            **result
        }
    
    except Exception as e:
        logger.error(f"❌ Error in RAG query: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/search/ragas-by-mood")
async def search_ragas_by_mood(request: RAGMoodSearchRequest):
    """
    Search for ragas that match a specific mood (peaceful, energetic, romantic, etc.)
    """
    try:
        logger.info(f"🎵 Mood search: {request.mood}")
        
        result = rag_system.search_ragas_by_mood(
            mood=request.mood,
            limit=request.limit
        )
        
        return {
            "status": "success",
            **result
        }
    
    except Exception as e:
        logger.error(f"❌ Error in mood search: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/search/instruments")
async def search_instruments(request: RAGInstrumentSearchRequest):
    """
    Search instruments by category (string, percussion, wind, electronic)
    """
    try:
        logger.info(f"🎸 Instrument search: {request.category}")
        
        result = rag_system.search_instruments_by_category(
            category=request.category,
            limit=request.limit
        )
        
        return {
            "status": "success",
            **result
        }
    
    except Exception as e:
        logger.error(f"❌ Error in instrument search: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/recommend/fusion-style")
async def recommend_fusion_style(request: RAGFusionRecommendRequest):
    """
    Get AI-powered fusion style recommendation based on your preferences
    """
    try:
        logger.info(f"🎨 Fusion recommendation request: {request.preferences}")
        
        result = rag_system.recommend_fusion_style(
            preferences=request.preferences
        )
        
        return {
            "status": "success",
            **result
        }
    
    except Exception as e:
        logger.error(f"❌ Error in fusion recommendation: {e}")
        raise HTTPException(status_code=500, detail=str(e))
