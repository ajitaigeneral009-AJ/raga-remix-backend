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
    indo_western_classical = "indo_western_classical"
    jazz_indian_fusion = "jazz_indian_fusion"
    rock_raga_fusion = "rock_raga_fusion"
    edm_indian_fusion = "edm_indian_fusion"
    bollywood_electronic = "bollywood_electronic"
    hip_hop_indian = "hip_hop_indian"
    sufi_rock = "sufi_rock"
    carnatic_jazz = "carnatic_jazz"
    edm_bhangra = "edm_bhangra"


class InstrumentMode(str, Enum):
    mute = "mute"
    original = "original"
    ai = "ai"


STYLE_ALIASES: Dict[str, str] = {
    "indian-western classical": "indo_western_classical",
    "indo-western classical": "indo_western_classical",
    "east meets west": "indo_western_classical",
    "jazz-indian fusion": "jazz_indian_fusion",
    "rock-raag fusion": "rock_raga_fusion",
    "edm-indian fusion": "edm_indian_fusion",
    "bollywood-electronic": "bollywood_electronic",
    "hip-hop-indian": "hip_hop_indian",
    "world music fusion": "indo_western_classical",
    "bhangra-rock": "edm_bhangra",

    "hindustani classical": "indo_western_classical",
    "carnatic music": "carnatic_jazz",
    "light classical": "indo_western_classical",
    "qawwali": "sufi_rock",
    "sufi music": "sufi_rock",
    "thumri": "indo_western_classical",
    "kajari": "indo_western_classical",
    "ghazal": "indo_western_classical",
    "bollywood pop": "bollywood_electronic",
    "bollywood folk": "indo_western_classical",
    "classical fusion": "indo_western_classical",
    "devotional bhajan": "indo_western_classical",

    "rock": "rock_raga_fusion",
    "metal": "rock_raga_fusion",
    "pop": "bollywood_electronic",
    "contemporary": "indo_western_classical",
    "jazz": "jazz_indian_fusion",
    "country": "indo_western_classical",
    "r&b": "hip_hop_indian",
    "soul": "jazz_indian_fusion",
    "acoustic": "indo_western_classical",
    "folk": "indo_western_classical",
    "reggae": "hip_hop_indian",
    "electronic": "edm_indian_fusion",
    "edm": "edm_indian_fusion",
    "hip-hop": "hip_hop_indian",
    "rap": "hip_hop_indian",
    "funk": "jazz_indian_fusion",
    "disco": "bollywood_electronic",
    "blues": "jazz_indian_fusion",
    "classical orchestral": "indo_western_classical",
}

STYLE_DEFAULT_INSTRUMENTS: Dict[str, List[str]] = {
    "indo_western_classical": ["tabla", "sitar", "acoustic_guitar"],
    "jazz_indian_fusion": ["tabla", "piano", "saxophone"],
    "rock_raga_fusion": ["drums", "electric_guitar", "bass"],
    "edm_indian_fusion": ["synthesizer", "bass", "tabla"],
    "bollywood_electronic": ["synthesizer", "tabla", "pads"],
    "hip_hop_indian": ["drums", "bass", "bansuri"],
    "sufi_rock": ["tabla", "acoustic_guitar", "harmonium"],
    "carnatic_jazz": ["mridangam", "violin", "piano"],
    "edm_bhangra": ["dhol", "bass", "synthesizer"],
}

VALID_INSTRUMENTS = [
    "sitar", "sarod", "veena", "sarangi", "dilruba", "israj", "mandolin",
    "bansuri", "shehnai", "nadaswaram", "tabla", "mridangam", "ghatam",
    "dholak", "harmonium",
    "acoustic_guitar", "electric_guitar", "violin", "cello", "bass",
    "saxophone", "trumpet", "trombone", "clarinet", "flute", "drums",
    "cymbals", "timpani", "piano", "synthesizer", "organ",
    "acoustic guitar", "electric guitar"
]


class ProcessingMode(str, Enum):
    FULL_REMIX = "full_remix"
    REMOVE_VOCALS = "remove_vocals"
    REMOVE_INSTRUMENTS = "remove_instruments"
    STEM_SEPARATION = "stem_separation"


class Mood(str, Enum):
    ROMANTIC = "romantic"
    DEVOTIONAL = "devotional"
    MELANCHOLIC = "melancholic"
    JOYFUL = "joyful"
    SERENE = "serene"
    ENERGETIC = "energetic"
    MYSTERIOUS = "mysterious"


class TimeOfDay(str, Enum):
    MORNING = "morning"
    AFTERNOON = "afternoon"
    EVENING = "evening"
    NIGHT = "night"
    LATE_NIGHT = "late_night"


# ============================================================
# AUDIO FEATURE MODELS
# ============================================================

class AudioFeatures(BaseModel):
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
    name: str = Field(..., description="Raga name")
    notes: List[str] = Field(default_factory=list, description="Raga notes")
    time_of_day: str = Field(default="", description="Preferred time")
    mood: str = Field(default="", description="Associated mood")
    compatibility_score: float = Field(default=0.8, ge=0, le=1, description="Match score")


class InstrumentInfo(BaseModel):
    name: str = Field(..., description="Instrument name")
    category: str = Field(..., description="Category")
    compatibility_score: float = Field(default=0.8, ge=0, le=1, description="Match score")
    role: str = Field(default="melody", description="Musical role")


# ============================================================
# REQUEST MODELS
# ============================================================

class CoverGenerationRequest(BaseModel):
    style: FusionStyle = Field(..., description="Fusion style to apply")
    custom_instruments: Optional[List[str]] = Field(
        None,
        description="Custom instruments"
    )
    tempo_ratio: float = Field(
        1.0,
        ge=0.5,
        le=2.0,
        description="Tempo adjustment ratio"
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
    instrument_mode: InstrumentMode = Field(
        InstrumentMode.mute,
        description="How to handle accompaniment: mute, original, or ai"
    )
    target_raga: Optional[str] = Field(
        None,
        description="Specific raga to target (optional)"
    )

    @validator("custom_instruments")
    def validate_instruments(cls, v):
        if v and len(v) > 10:
            raise ValueError("Maximum 10 instruments allowed")
        return v


class SongAnalysisRequest(BaseModel):
    query: str = Field(..., min_length=3, description="Analysis query")
    time_of_day: Optional[TimeOfDay] = Field(None, description="Time constraint")
    desired_mood: Optional[Mood] = Field(None, description="Mood constraint")


class InstrumentRecommendationRequest(BaseModel):
    raga_name: str = Field(..., description="Raga name")
    fusion_style: FusionStyle = Field(..., description="Fusion style")
    max_instruments: int = Field(5, ge=1, le=10, description="Max recommendations")


# ============================================================
# RESPONSE MODELS
# ============================================================

class ProcessingStep(BaseModel):
    step: str = Field(..., description="Step name")
    status: str = Field(..., description="Status")
    duration_seconds: Optional[float] = Field(None, description="Step duration")
    details: Dict[str, Any] = Field(default_factory=dict, description="Step details")


class CoverGenerationResponse(BaseModel):
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
    recommended_ragas: List[RagaInfo] = Field(default_factory=list, description="Recommended ragas")
    recommended_instruments: List[InstrumentInfo] = Field(default_factory=list, description="Recommended instruments")
    fusion_style_suggestion: FusionStyle = Field(..., description="Suggested fusion style")
    analysis_context: str = Field(..., description="Detailed analysis")
    confidence_score: float = Field(..., ge=0, le=1, description="Confidence in recommendations")


class InstrumentRecommendationResponse(BaseModel):
    raga_name: str = Field(..., description="Input raga")
    fusion_style: FusionStyle = Field(..., description="Input style")
    recommended_instruments: List[InstrumentInfo] = Field(default_factory=list, description="Recommendations")
    arrangement_suggestion: str = Field(..., description="Arrangement advice")


class HealthResponse(BaseModel):
    status: str = Field(..., description="Overall status")
    rag_status: str = Field(..., description="RAG service status")
    audio_processor_status: str = Field(..., description="Audio processor status")
    version: str = Field(..., description="API version")
    uptime_seconds: Optional[float] = Field(None, description="Server uptime")


# ============================================================
# JOB TRACKING MODELS
# ============================================================

class JobMetadata(BaseModel):
    job_id: str
    status: str
    created_at: float
    updated_at: float
    input_file: str
    output_file: Optional[str] = None
    request: Dict[str, Any]
    progress: float = 0.0
    current_step: Optional[str] = None
    error: Optional[str] = None


# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def create_error_response(job_id: str, error_message: str) -> CoverGenerationResponse:
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
    return CoverGenerationResponse(
        job_id=job_id,
        status="completed",
        output_url=output_url,
        applied_raga=metadata.request.get("target_raga"),
        instruments_used=metadata.request.get("custom_instruments", []),
        processing_time_seconds=processing_time
    )
