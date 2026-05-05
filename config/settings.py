"""
Configuration settings for Raga Remix Studio Backend
"""

import os
from pathlib import Path
from typing import List, Dict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # ============================================================
    # API KEYS
    # ============================================================
    
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # ============================================================
    # SERVER CONFIGURATION
    # ============================================================
    
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # ============================================================
    # PATHS
    # ============================================================
    
    BASE_DIR: Path = Path(__file__).parent
    TEMP_UPLOAD_DIR: Path = BASE_DIR / "temp_uploads"
    OUTPUT_DIR: Path = BASE_DIR / "outputs"
    CHROMA_PERSIST_DIRECTORY: str = str(BASE_DIR / "chroma_db")
    
    # ============================================================
    # AUDIO PROCESSING
    # ============================================================
    
    # File handling
    MAX_FILE_SIZE_MB: int = 50
    ALLOWED_AUDIO_FORMATS: List[str] = [".mp3", ".wav", ".flac", ".ogg", ".m4a"]
    
    # Audio quality
    SAMPLE_RATE: int = 22050  # Halved from 44100 to reduce memory usage
    TARGET_LOUDNESS_LUFS: float = -14.0
    TEMP_UPLOAD_DIR: Path = Path(__file__).parent.parent / "temp_uploads"
    OUTPUT_DIR: Path = Path(__file__).parent.parent / "outputs"
    
    # Demucs configuration
    DEMUCS_MODEL: str = "mdx_q"  # Quantized model - uses ~300MB RAM (fits free tier 512MB)
    DEMUCS_DEVICE: str = "cpu"  # or "cuda" for GPU
    
    # Processing limits
    MAX_CONCURRENT_JOBS: int = 1  # Limit to 1 job to prevent OOM on free tier 512MB
    PROCESSING_TIMEOUT_SECONDS: int = 600
    
    # ============================================================
    # RAG SYSTEM
    # ============================================================
    
    # Embedding model
    EMBEDDING_MODEL: str = "text-embedding-ada-002"
    
    # LLM model
    LLM_MODEL: str = "gpt-4"
    LLM_TEMPERATURE: float = 0.7
    MAX_TOKENS: int = 2000
    
    # Retrieval
    TOP_K_RESULTS: int = 5
    SIMILARITY_THRESHOLD: float = 0.7
    
    # ============================================================
    # RAGA CONFIGURATION
    # ============================================================
    
    # Raga transformation settings
    RAGA_PITCH_SHIFT_RANGE: tuple = (-12, 12)  # Semitones
    RAGA_ORNAMENTATION_INTENSITY: float = 0.5  # 0-1
    
    # Raga note mapping (simplified - full mapping in raga_database.py)
    RAGA_SCALE_DEGREES: Dict[str, List[int]] = {
        "Yaman": [0, 2, 4, 6, 7, 9, 11],  # Sa Re Ga Ma# Pa Dha Ni
        "Bhairav": [0, 1, 4, 5, 7, 8, 11],  # Sa re Ga ma Pa dha Ni
        "Kafi": [0, 2, 3, 5, 7, 9, 10],  # Sa Re ga ma Pa Dha ni
    }
    
    # ============================================================
    # INSTRUMENT CONFIGURATION
    # ============================================================
    
    # Instrument synthesis settings
    TABLA_SAMPLE_RATE: int = 44100
    TABLA_PATTERNS: List[str] = ["teentaal", "dadra", "keherwa", "jhaptaal"]
    
    # MIDI settings for synthesis
    MIDI_VELOCITY_RANGE: tuple = (60, 100)
    MIDI_DEFAULT_TEMPO: int = 120
    
    # Instrument mixing levels (in dB)
    DEFAULT_MIX_LEVELS: Dict[str, float] = {
        "vocals": 0.0,
        "tabla": -2.0,
        "sitar": -4.0,
        "harmonium": -6.0,
        "guitar": -4.0,
        "bass": -3.0,
        "drums": -2.0,
        "other": -8.0
    }
    
    # ============================================================
    # FUSION STYLE CONFIGURATION
    # ============================================================
    
    # Style-specific parameters
    FUSION_STYLE_PARAMS: Dict[str, Dict] = {
        "indo_western_classical": {
            "tempo_range": (0.8, 1.2),
            "energy_curve": "gradual_rise",
            "mix_balance": "indian_dominant"
        },
        "jazz_indian_fusion": {
            "tempo_range": (0.9, 1.3),
            "energy_curve": "dynamic",
            "mix_balance": "balanced"
        },
        "rock_raga_fusion": {
            "tempo_range": (1.0, 1.4),
            "energy_curve": "high_energy",
            "mix_balance": "western_dominant"
        },
        "bollywood_electronic": {
            "tempo_range": (0.95, 1.25),
            "energy_curve": "pulsating",
            "mix_balance": "electronic_prominent"
        },
        "edm_indian_fusion": {
            "tempo_range": (1.1, 1.5),
            "energy_curve": "build_drop",
            "mix_balance": "electronic_dominant"
        },
        "hip_hop_indian": {
            "tempo_range": (0.85, 1.15),
            "energy_curve": "steady_groove",
            "mix_balance": "rhythm_focused"
        },
        "sufi_rock": {
            "tempo_range": (0.9, 1.2),
            "energy_curve": "spiritual_rise",
            "mix_balance": "vocal_centric"
        },
        "carnatic_jazz": {
            "tempo_range": (0.9, 1.35),
            "energy_curve": "improvisational",
            "mix_balance": "balanced"
        },
        "edm_bhangra": {
            "tempo_range": (1.15, 1.45),
            "energy_curve": "festive_energy",
            "mix_balance": "rhythm_and_electronic"
        }
    }
    
    # ============================================================
    # AUDIO FEATURE EXTRACTION
    # ============================================================
    
    # Librosa feature extraction
    N_FFT: int = 2048
    HOP_LENGTH: int = 512
    N_MELS: int = 128
    
    # Tempo detection
    TEMPO_MIN_BPM: int = 40
    TEMPO_MAX_BPM: int = 200
    
    # Key detection
    KEY_PROFILES: List[str] = ["krumhansl", "temperley", "edma"]
    
    # ============================================================
    # LOGGING
    # ============================================================
    
    LOG_LEVEL: str = "INFO" if DEBUG else "WARNING"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_FILE: str = "raga_remix.log"

    GEMINI_API_KEY: str = ""
    LYRIA_MODEL_ID: str = "models/lyria-realtime-exp"  # from Gemini docs[web:198]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Create directories if they don't exist
        self.TEMP_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        self.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        
        # Validate OpenAI API key
        if not self.OPENAI_API_KEY or self.OPENAI_API_KEY == "your-api-key-here":
            print("⚠️  WARNING: OPENAI_API_KEY not set in environment variables!")
            print("   Set it in .env file or export OPENAI_API_KEY=sk-...")
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create global settings instance
settings = Settings()


# ============================================================
# RAGA TIME ASSOCIATIONS
# ============================================================

RAGA_TIME_MAP = {
    "morning": ["Bhairav", "Todi", "Asavari", "Lalit"],
    "afternoon": ["Sarang", "Multani", "Madhyamavati"],
    "evening": ["Yaman", "Bihag", "Puriya", "Marwa"],
    "night": ["Kafi", "Darbari", "Bageshri", "Malkauns"],
    "late_night": ["Darbari Kanada", "Malkauns", "Chandrakauns"]
}


# ============================================================
# RAGA MOOD ASSOCIATIONS
# ============================================================

RAGA_MOOD_MAP = {
    "romantic": ["Yaman", "Kafi", "Bihag", "Khamaj"],
    "devotional": ["Bhairav", "Bhairavi", "Pilu"],
    "melancholic": ["Darbari", "Bageshri", "Todi"],
    "joyful": ["Bilawal", "Durga", "Khamaj"],
    "serene": ["Yaman", "Bhupali", "Ahir Bhairav"],
    "energetic": ["Jog", "Jaunpuri", "Multani"],
    "mysterious": ["Marwa", "Puriya", "Sohini"]
}


# ============================================================
# INSTRUMENT COMPATIBILITY
# ============================================================

INSTRUMENT_COMPATIBILITY = {
    "Tabla": ["Sitar", "Sarod", "Bansuri", "Harmonium", "Santoor"],
    "Sitar": ["Tabla", "Tanpura", "Harmonium"],
    "Guitar": ["Tabla", "Cajon", "Bass", "Violin"],
    "Harmonium": ["Tabla", "Dholak", "Flute", "Vocals"],
    "Flute": ["Tabla", "Guitar", "Violin", "Cello"],
    "Violin": ["Guitar", "Piano", "Cello", "Tabla"]
}


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_raga_for_time(time_of_day: str) -> List[str]:
    """Get recommended ragas for time of day"""
    return RAGA_TIME_MAP.get(time_of_day.lower(), [])


def get_raga_for_mood(mood: str) -> List[str]:
    """Get recommended ragas for mood"""
    return RAGA_MOOD_MAP.get(mood.lower(), [])


def get_compatible_instruments(instrument: str, max_count: int = 5) -> List[str]:
    """Get compatible instruments for given instrument"""
    return INSTRUMENT_COMPATIBILITY.get(instrument, [])[:max_count]


if __name__ == "__main__":
    # Test configuration
    print("=" * 70)
    print("RAGA REMIX STUDIO - CONFIGURATION")
    print("=" * 70)
    print(f"OpenAI API Key: {settings.OPENAI_API_KEY[:10]}..." if settings.OPENAI_API_KEY else "Not set")
    print(f"Server: {settings.HOST}:{settings.PORT}")
    print(f"Debug Mode: {settings.DEBUG}")
    print(f"Temp Upload Dir: {settings.TEMP_UPLOAD_DIR}")
    print(f"Output Dir: {settings.OUTPUT_DIR}")
    print(f"Demucs Model: {settings.DEMUCS_MODEL}")
    print(f"Sample Rate: {settings.SAMPLE_RATE} Hz")
    print("=" * 70)
