"""
Pydantic Data Models and Schemas
Request/Response models for all API endpoints
"""

from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator


# ============================================================
# ENUMS
# ============================================================

class FusionStyle(str, Enum):
    """Available fusion music styles"""
    INDO_WESTERN_CLASSICAL = "indo_western_classical"
    JAZZ_INDIAN_FUSION = "jazz_indian_fusion"
    ROCK_RAGA_FUSION = "rock_raga_fusion"
    BOLLYWOOD_ELECTRONIC = "bollywood_electronic"
    EDM_INDIAN_FUSION = "edm_indian_fusion"
    HIP_HOP_INDIAN = "hip_hop_indian"
    SUFI_ROCK = "sufi_rock"
    CARNATIC_JAZZ = "carnatic_jazz"
    EDM_BHANGRA = "edm_bhangra"


class ProcessingMode(str, Enum):
    """Audio processing modes"""
    FULL_REMIX = "full_remix"
    REMOVE_VOCALS = "remove_vocals"
    REMOVE_INSTRUMENTS = "remove_instruments"
    STEM_SEPARATION = "stem_separation"


class Mood(str, Enum):
    """Musical moods"""
    ROMANTIC = "romantic"
    DEVOTIONAL = "devotional"
    MELANCHOLIC = "melancholic"
    JOYFUL = "joyful"
    SERENE = "serene"
    ENERGETIC = "energetic"
    MYSTERIOUS = "mysterious"


class TimeOfDay(str, Enum):
    """Time of day for raga selection"""
    MORNING = "morning"
    AFTERNOON = "afternoon"
    EVENING = "evening"
    NIGHT = "night"
    LATE_NIGHT = "late_night"


# ============================================================
# AUDIO FEATURE MODELS
# ============================================================

class AudioFeatures(BaseModel):
    """Extracted audio features"""
    tempo_bpm: float = Field(..., description="Tempo in beats per minute")
    key: str = Field(..., description="Musical key (e.g., 'C major')")
    energy: float = Field(..., ge=0, le=1, description="Energy level 0-1")
    danceability: float = Field(..., ge=0, le=1, description="Danceability 0-1")
    valence: float = Field(..., ge=0, le=1, description="Musical positiveness 0-1")
    spectral_centroid: float = Field(..., description="Brightness measure")
    zero_crossing_rate: float = Field(..., description="Percussiveness measure")
    duration_seconds: float = Field(..., description="Track duration")


# ============================================================
# RAGA & INSTRUMENT MODELS
# ============================================================

class RagaInfo(BaseModel):
    """Raga information"""
    name: str = Field(..., description="Raga name")
    notes: List[str] = Field(default_factory=list, description="Raga notes (Sa Re Ga...)")
    time_of_day: str = Field(default="", description="Preferred time")
    mood: str = Field(default="", description="Associated mood")
    compatibility_score: float = Field(default=0.8, ge=0, le=1, description="Match score")


class InstrumentInfo(BaseModel):
    """Instrument information"""
    name: str = Field(..., description="Instrument name")
    category: str = Field(..., description="Category (Indian/Western/Electronic)")
    compatibility_score: float = Field(default=0.8, ge=0, le=1, description="Match score")
    role: str = Field(default="melody", description="Musical role")


# ============================================================
# REQUEST MODELS
# ============================================================

class CoverGenerationRequest(BaseModel):
    """Request for cover generation"""
    style: FusionStyle = Field(..., description="Fusion style to apply")
    custom_instruments: Optional[List[str]] = Field(
        None,
        description="Custom instruments (e.g., ['Tabla', 'Guitar'])"
    )
    tempo_ratio: float = Field(
        1.0,
        ge=0.5,
        le=2.0,
        description="Tempo adjustment ratio (1.0 = original)"
    )
    pitch_semitones: int = Field(
        0,
        ge=-12,
        le=12,
        description="Pitch shift in semitones"
    )
    energy_level: float = Field(
        0.7,
        ge=0,
        le=1,
        description="Target energy level"
    )
    preserve_vocals: bool = Field(
        True,
        description="Whether to preserve original vocals"
    )
    target_raga: Optional[str] = Field(
        None,
        description="Specific raga to target (optional)"
    )
    
    @validator("custom_instruments")
    def validate_instruments(cls, v):
        """Validate instrument list"""
        if v and len(v) > 10:
            raise ValueError("Maximum 10 instruments allowed")
        return v


class SongAnalysisRequest(BaseModel):
    """Request for RAG-powered song analysis"""
    query: str = Field(..., min_length=3, description="Analysis query")
    time_of_day: Optional[TimeOfDay] = Field(None, description="Time constraint")
    desired_mood: Optional[Mood] = Field(None, description="Mood constraint")


class InstrumentRecommendationRequest(BaseModel):
    """Request for instrument recommendations"""
    raga_name: str = Field(..., description="Raga name")
    fusion_style: FusionStyle = Field(..., description="Fusion style")
    max_instruments: int = Field(5, ge=1, le=10, description="Max recommendations")


# ============================================================
# RESPONSE MODELS
# ============================================================

class ProcessingStep(BaseModel):
    """Single processing step info"""
    step: str = Field(..., description="Step name")
    status: str = Field(..., description="Status (completed/failed/in_progress)")
    duration_seconds: Optional[float] = Field(None, description="Step duration")
    details: Dict[str, Any] = Field(default_factory=dict, description="Step details")


class CoverGenerationResponse(BaseModel):
    """Response from cover generation"""
    job_id: str = Field(..., description="Unique job identifier")
    status: str = Field(..., description="Job status")
    output_url: Optional[str] = Field(None, description="Download URL")
    processing_details: Optional[Dict[str, Any]] = Field(
        None,
        description="Detailed processing info"
    )
    applied_raga: Optional[str] = Field(None, description="Applied raga")
    instruments_used: List[str] = Field(default_factory=list, description="Instruments")
    processing_time_seconds: Optional[float] = Field(None, description="Total time")
    audio_features: Optional[AudioFeatures] = Field(None, description="Audio features")
    error_message: Optional[str] = Field(None, description="Error if failed")


class SongAnalysisResponse(BaseModel):
    """Response from song analysis"""
    recommended_ragas: List[RagaInfo] = Field(
        default_factory=list,
        description="Recommended ragas"
    )
    recommended_instruments: List[InstrumentInfo] = Field(
        default_factory=list,
        description="Recommended instruments"
    )
    fusion_style_suggestion: FusionStyle = Field(
        ...,
        description="Suggested fusion style"
    )
    analysis_context: str = Field(..., description="Detailed analysis")
    confidence_score: float = Field(
        ...,
        ge=0,
        le=1,
        description="Confidence in recommendations"
    )


class InstrumentRecommendationResponse(BaseModel):
    """Response from instrument recommendation"""
    raga_name: str = Field(..., description="Input raga")
    fusion_style: FusionStyle = Field(..., description="Input style")
    recommended_instruments: List[InstrumentInfo] = Field(
        default_factory=list,
        description="Recommendations"
    )
    arrangement_suggestion: str = Field(
        ...,
        description="Arrangement advice"
    )


class HealthResponse(BaseModel):
    """Health check response"""
    status: str = Field(..., description="Overall status")
    rag_status: str = Field(..., description="RAG service status")
    audio_processor_status: str = Field(..., description="Audio processor status")
    version: str = Field(..., description="API version")
    uptime_seconds: Optional[float] = Field(None, description="Server uptime")


# ============================================================
# JOB TRACKING MODELS
# ============================================================

class JobMetadata(BaseModel):
    """Job tracking metadata"""
    job_id: str
    status: str  # pending, processing, completed, failed
    created_at: float
    updated_at: float
    input_file: str
    output_file: Optional[str] = None
    request: Dict[str, Any]
    progress: float = 0.0  # 0-1
    current_step: Optional[str] = None
    error: Optional[str] = None


# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def create_error_response(
    job_id: str,
    error_message: str
) -> CoverGenerationResponse:
    """Create error response"""
    return CoverGenerationResponse(
        job_id=job_id,
        status="failed",
        error_message=error_message,
        instruments_used=[]
    )


def create_success_response(
    job_id: str,
    output_url: str,
    metadata: JobMetadata,
    processing_time: float
) -> CoverGenerationResponse:
    """Create success response"""
    return CoverGenerationResponse(
        job_id=job_id,
        status="completed",
        output_url=output_url,
        applied_raga=metadata.request.get("target_raga"),
        instruments_used=metadata.request.get("custom_instruments", []),
        processing_time_seconds=processing_time
    )


if __name__ == "__main__":
    # Test models
    print("Testing Pydantic models...")
    
    # Test request
    request = CoverGenerationRequest(
        style=FusionStyle.INDO_WESTERN_CLASSICAL,
        custom_instruments=["Tabla", "Guitar"],
        tempo_ratio=1.1,
        energy_level=0.8
    )
    print(f"Request: {request.dict()}")
    
    # Test response
    response = CoverGenerationResponse(
        job_id="test-123",
        status="completed",
        output_url="/download/test-123",
        applied_raga="Yaman",
        instruments_used=["Tabla", "Guitar"],
        processing_time_seconds=78.5
    )
    print(f"Response: {response.dict()}")
    
    print("✅ All models validated successfully!")
