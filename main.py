"""
Raga Remix Studio - FastAPI Backend
Complete implementation with RAG-powered cover generation
"""

import logging
import time
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, File, UploadFile, Form, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError

from config import Settings
from models.schemas import (
    CoverGenerationRequest,
    CoverGenerationResponse,
    SongAnalysisRequest,
    SongAnalysisResponse,
    InstrumentRecommendationRequest,
    InstrumentRecommendationResponse,
    HealthResponse,
    FusionStyle,
    ProcessingMode,
)
from services.rag_service import get_rag_service
from services.audio_processor import get_audio_processor
from services.cover_generator import get_cover_generator

settings = Settings()

logging.basicConfig(
    level=logging.INFO if settings.DEBUG else logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Raga Remix Studio API",
    description="RAG-powered AI music cover generation with Indian classical fusion",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: restrict for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Track startup time
startup_time = time.time()

# ============================================================
# STARTUP & SHUTDOWN
# ============================================================

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    
    logger.info("=" * 70)
    logger.info("🎵 RAGA REMIX STUDIO BACKEND STARTING")
    logger.info("=" * 70)
    
    try:
        # Initialize RAG service
        logger.info("Initializing RAG Service...")
        get_rag_service()
        logger.info("✅ RAG Service ready")
        
        # Initialize audio processor
        logger.info("Initializing Audio Processor...")
        get_audio_processor()
        logger.info("✅ Audio Processor ready")
        
        # Initialize cover generator
        logger.info("Initializing Cover Generator...")
        get_cover_generator()
        logger.info("✅ Cover Generator ready")
        
        logger.info("=" * 70)
        logger.info(f"🚀 SERVER READY ON http://{settings.HOST}:{settings.PORT}")
        logger.info(f"📚 API Docs: http://{settings.HOST}:{settings.PORT}/docs")
        logger.info("=" * 70)
        
    except Exception as e:
        logger.error(f"❌ Startup failed: {e}", exc_info=True)
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("🛑 Server shutting down...")


# ============================================================
# HEALTH & STATUS ENDPOINTS
# ============================================================

@app.get("/", tags=["Status"])
async def root():
    """Root endpoint"""
    return {
        "message": "Raga Remix Studio API",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs"
    }


@app.api_route("/health", methods=["GET", "HEAD"], response_model=HealthResponse, tags=["Status"])
async def health_check():
    """Health check endpoint"""
    
    try:
        # Check RAG service
        rag_service = get_rag_service()
        rag_health = rag_service.health_check()
        
        # Check audio processor
        audio_processor = get_audio_processor()
        audio_health = audio_processor.health_check()
        
        uptime = time.time() - startup_time
        
        overall_status = "healthy" if (
            rag_health["status"] == "healthy" and
            audio_health["status"] == "healthy"
        ) else "degraded"
        
        return HealthResponse(
            status=overall_status,
            rag_status=rag_health["status"],
            audio_processor_status=audio_health["status"],
            version="1.0.0",
            uptime_seconds=uptime
        )
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return HealthResponse(
            status="unhealthy",
            rag_status="error",
            audio_processor_status="error",
            version="1.0.0"
        )


# ============================================================
# RAG QUERY ENDPOINTS
# ============================================================

@app.post("/api/analyze-song", response_model=SongAnalysisResponse, tags=["Analysis"])
async def analyze_song(request: SongAnalysisRequest):
    """
    Analyze song characteristics and get RAG-powered recommendations
    
    This endpoint uses the RAG system to provide intelligent recommendations
    for ragas, instruments, and fusion styles based on the query.
    """
    
    logger.info(f"📊 Song analysis request: {request.query}")
    
    try:
        rag_service = get_rag_service()
        
        # Query RAG system
        result = rag_service.query(
            query_text=request.query,
            time_of_day=request.time_of_day.value if request.time_of_day else None,
            mood=request.desired_mood.value if request.desired_mood else None
        )
        
        # Build response
        response = SongAnalysisResponse(
            recommended_ragas=[
                {
                    "name": raga["name"],
                    "notes": raga.get("notes", "").split(", "),
                    "time_of_day": raga.get("time_of_day", ""),
                    "mood": raga.get("mood", ""),
                    "compatibility_score": raga.get("compatibility_score", 0.8)
                }
                for raga in result["recommendations"]["ragas"][:3]
            ],
            recommended_instruments=[
                {
                    "name": inst["name"],
                    "category": inst.get("category", ""),
                    "compatibility_score": inst.get("compatibility_score", 0.8),
                    "role": inst.get("role", "")
                }
                for inst in result["recommendations"]["instruments"][:5]
            ],
            fusion_style_suggestion=FusionStyle.INDO_WESTERN_CLASSICAL,  # Default
            analysis_context=result["answer"],
            confidence_score=result["confidence"]
        )
        
        logger.info(f"✅ Analysis complete: {len(response.recommended_ragas)} ragas, "
                   f"{len(response.recommended_instruments)} instruments")
        
        return response
        
    except Exception as e:
        logger.error(f"❌ Analysis failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/recommend-instruments", response_model=InstrumentRecommendationResponse, tags=["Analysis"])
async def recommend_instruments(request: InstrumentRecommendationRequest):
    """Get instrument recommendations for specific raga and fusion style"""
    
    logger.info(f"🎹 Instrument recommendation: {request.raga_name} + {request.fusion_style}")
    
    try:
        rag_service = get_rag_service()
        
        instruments = rag_service.recommend_instruments(
            raga_name=request.raga_name,
            fusion_style=request.fusion_style.value,
            max_count=request.max_instruments
        )
        
        response = InstrumentRecommendationResponse(
            raga_name=request.raga_name,
            fusion_style=request.fusion_style,
            recommended_instruments=[
                {
                    "name": inst["name"],
                    "category": inst.get("category", ""),
                    "compatibility_score": inst.get("compatibility_score", 0.8),
                    "role": inst.get("role", "")
                }
                for inst in instruments
            ],
            arrangement_suggestion=f"Recommended {request.fusion_style.value} arrangement"
        )
        
        return response
        
    except Exception as e:
        logger.error(f"❌ Instrument recommendation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# COVER GENERATION ENDPOINTS
# ============================================================

@app.post("/api/mode/cover-with-style", response_model=CoverGenerationResponse, tags=["Cover Generation"])
async def generate_cover_with_style(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    style: str = Form(...),
    custom_instruments: Optional[str] = Form(None),
    tempo_ratio: float = Form(1.0),
    pitch_semitones: int = Form(0),
    energy_level: float = Form(0.7),
    preserve_vocals: bool = Form(True),
    target_raga: Optional[str] = Form(None)
):
    """
    Generate cover song with specified fusion style
    
    This is the main endpoint that:
    1. Uploads audio file
    2. Uses RAG to select raga & instruments
    3. Separates stems
    4. Applies transformations
    5. Returns generated cover
    """
    
    logger.info("=" * 70)
    logger.info("🎵 COVER GENERATION REQUEST")
    logger.info(f"   File: {file.filename}")
    logger.info(f"   Style: {style}")
    logger.info(f"   Instruments: {custom_instruments}")
    logger.info("=" * 70)
    
    try:
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in settings.ALLOWED_AUDIO_FORMATS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported format. Allowed: {settings.ALLOWED_AUDIO_FORMATS}"
            )
        
        # Save uploaded file
        upload_dir = settings.TEMP_UPLOAD_DIR
        upload_path = upload_dir / f"{int(time.time())}_{file.filename}"
        
        with open(upload_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        logger.info(f"✅ File saved: {upload_path}")
        
        # Parse instruments
        instruments_list = None
        if custom_instruments:
            instruments_list = [inst.strip() for inst in custom_instruments.split(",")]
        
        # Build request
        request = CoverGenerationRequest(
            style=FusionStyle(style),
            custom_instruments=instruments_list,
            tempo_ratio=tempo_ratio,
            pitch_semitones=pitch_semitones,
            energy_level=energy_level,
            preserve_vocals=preserve_vocals,
            target_raga=target_raga
        )
        
        # Generate cover
        cover_generator = get_cover_generator()
        
        response = await cover_generator.generate_cover(
            audio_path=str(upload_path),
            request=request
        )
        
        logger.info(f"✅ Cover generation response: Status={response.status}")
        
        return response
        
    except ValidationError as e:
        logger.error(f"❌ Validation error: {e}")
        raise HTTPException(status_code=422, detail=str(e))
        
    except Exception as e:
        logger.error(f"❌ Cover generation failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/download/{job_id}", tags=["Cover Generation"])
async def download_cover(job_id: str):
    """Download generated cover by job ID"""
    
    logger.info(f"📥 Download request: {job_id}")
    
    try:
        cover_generator = get_cover_generator()
        metadata = cover_generator.get_job_status(job_id)
        
        if not metadata:
            raise HTTPException(status_code=404, detail="Job not found")
        
        if not metadata.output_file:
            raise HTTPException(status_code=404, detail="Output file not ready")
        
        output_path = Path(metadata.output_file)
        
        if not output_path.exists():
            raise HTTPException(status_code=404, detail="Output file not found")
        
        return FileResponse(
            path=str(output_path),
            media_type="audio/wav",
            filename=f"cover_{job_id}.wav"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Download failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# LEGACY ENDPOINTS (for backward compatibility)
# ============================================================

@app.post("/process", tags=["Legacy"])
async def process_audio_legacy(
    file: UploadFile = File(...),
    mode: str = Form(...)
):
    """Legacy endpoint - redirects to new cover generation"""
    
    logger.warning(f"⚠️ Using legacy endpoint /process - please migrate to /api/mode/cover-with-style")
    
    # Map legacy mode to new style
    mode_mapping = {
        "full_remix": "indo_western_classical",
        "remove_vocals": "bollywood_electronic",
        "remove_instruments": "sufi_rock"
    }
    
    style = mode_mapping.get(mode, "indo_western_classical")
    
    return await generate_cover_with_style(
        background_tasks=BackgroundTasks(),
        file=file,
        style=style
    )


# ============================================================
# RUN SERVER
# ============================================================

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info" if settings.DEBUG else "warning"
    )
