"""
FastAPI routes for cover generation with Raga-based instrument synthesis
VERSION 4.0 - Two separate pipelines for Karaoke and Full Cover
PRODUCTION-READY with comprehensive error handling and logging
"""

from fastapi import (
    FastAPI,
    APIRouter,
    UploadFile,
    File,
    Form,
    HTTPException,
)
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import logging
import uuid
from pathlib import Path
import librosa
import soundfile as sf
import numpy as np

from services.stem_separator import StemSeparator
from services.instrument_synth import RagaInstrumentSynthesizer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Raga Remix Studio API v4.0",
    description="AI Cover Studio - Generate Raga-based cover songs",
    version="4.0.0"
)
router = APIRouter(prefix="/api", tags=["cover-generation"])

# Initialize synthesizer with Raga database
try:
    synthesizer = RagaInstrumentSynthesizer(raga_db_path="services/raga_database.py")
    logger.info("✅ Raga Instrument Synthesizer initialized successfully")
except Exception as e:
    logger.error(f"❌ Failed to initialize synthesizer: {e}")
    raise

# =========================================================================
# PYDANTIC MODELS
# =========================================================================

class KaraokeWithRagaRequest(BaseModel):
    """Karaoke mode request with Raga-based instruments."""
    target_raga: str
    instruments: str = "tabla,sitar,guitar"
    tempo_ratio: float = 1.0
    energy_level: float = 0.8

class CoverWithRagaRequest(BaseModel):
    """Full cover mode request with Raga-based instruments."""
    target_raga: str
    instruments: str = "tabla,sitar,guitar"
    tempo_ratio: float = 1.0
    pitch_semitones: int = 0
    energy_level: float = 0.8

class GenerateCoverResponse(BaseModel):
    """Response for cover generation."""
    job_id: str
    status: str
    mode: str
    raga: str
    instruments: List[str]
    download_url: str

# =========================================================================
# HEALTH & CATALOG ENDPOINTS
# =========================================================================

@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": "4.0.0",
        "service": "Raga Remix Studio API",
        "timestamp": str(np.datetime64('now'))
    }

@app.get("/api/ragas")
async def get_ragas():
    """Get all available Ragas with details."""
    ragas_data = {
        "count": 8,
        "ragas": {
            "yaman": {
                "name": "Yaman",
                "mood": "Peaceful, devotional, evening",
                "notes": ["Sa", "Re", "Ga", "Ma", "Pa", "Dha", "Ni"],
                "time": "Evening",
                "character": "Serene and devotional"
            },
            "bhairav": {
                "name": "Bhairav",
                "mood": "Serious, reverent, morning",
                "notes": ["Sa", "Re", "Ga", "Ma", "Pa", "Dha", "Ni"],
                "time": "Morning",
                "character": "Solemn and majestic"
            },
            "khamaaj": {
                "name": "Khamaaj",
                "mood": "Gentle, soothing",
                "notes": ["Sa", "Re", "Ga", "Ma", "Pa", "Dha", "Ni"],
                "character": "Soft and melodic"
            },
            "ahir_bhairav": {
                "name": "Ahir Bhairav",
                "mood": "Melancholic, contemplative",
                "notes": ["Sa", "Re", "Ga", "Ma", "Pa", "Dha", "Ni"],
                "character": "Introspective and thoughtful"
            },
            "marwa": {
                "name": "Marwa",
                "mood": "Energetic, uplifting",
                "notes": ["Sa", "Re", "Ga", "Ma", "Pa", "Dha", "Ni"],
                "character": "Bright and vibrant"
            },
            "todi": {
                "name": "Todi",
                "mood": "Pathos, separation",
                "notes": ["Sa", "Re", "Ga", "Ma", "Pa", "Dha", "Ni"],
                "character": "Emotional and expressive"
            }
        }
    }
    logger.info("📊 Ragas catalog requested")
    return ragas_data

@app.get("/api/instruments")
async def get_instruments():
    """Get available instruments."""
    return {
        "instruments": ["tabla", "sitar", "guitar"],
        "details": {
            "tabla": {
                "category": "Percussion",
                "role": "Rhythm keeper",
                "characteristics": "Provides rhythmic base respecting Raga tempo"
            },
            "sitar": {
                "category": "String",
                "role": "Melody",
                "characteristics": "Plays only notes from selected Raga"
            },
            "guitar": {
                "category": "String",
                "role": "Harmony",
                "characteristics": "Provides harmonic support respecting Raga intervals"
            }
        },
        "recommended_combinations": [
            "tabla,sitar,guitar",
            "tabla,sitar",
            "sitar,guitar"
        ]
    }

# =========================================================================
# PIPELINE 1: KARAOKE WITH RAGA-BASED INSTRUMENTS
# =========================================================================

@router.post("/mode/karaoke-with-raga")
async def karaoke_with_raga(
    file: UploadFile = File(...),
    target_raga: str = Form("yaman"),
    instruments: str = Form("tabla,sitar,guitar"),
    tempo_ratio: float = Form(1.0),
    energy_level: float = Form(0.8),
):
    """
    KARAOKE MODE: Generate backing track with Raga-based custom instruments.
    
    User sings over this custom backing track (like Boyce Avenue covers).
    
    Process:
    1. Extract vocals from original song
    2. COMPLETELY REMOVE original instruments
    3. Generate NEW custom instruments (Tabla, Sitar, Guitar) in selected Raga
    4. Create professional backing track
    5. User can sing their own performance over this
    
    Parameters:
    - target_raga: Yaman, Bhairav, Khamaaj, etc.
    - instruments: Comma-separated (tabla,sitar,guitar)
    - tempo_ratio: 0.8 (slower) to 1.3 (faster)
    - energy_level: 0.5 (soft) to 1.0 (loud)
    
    Returns: Backing track (NO original instruments, NO vocals)
    """
    job_id = None
    try:
        # Setup directories
        uploads_dir = Path("uploads")
        outputs_dir = Path("outputs")
        uploads_dir.mkdir(exist_ok=True)
        outputs_dir.mkdir(exist_ok=True)

        job_id = str(uuid.uuid4())[:8]
        input_path = uploads_dir / f"karaoke_{job_id}_{file.filename}"
        output_path = outputs_dir / f"karaoke_{target_raga}_{job_id}.wav"

        # Save uploaded file
        content = await file.read()
        input_path.write_bytes(content)
        logger.info(f"📁 [Karaoke-{job_id}] File uploaded: {input_path}")

        # Load audio
        audio, sr = librosa.load(str(input_path), sr=None, mono=True)
        logger.info(f"🎵 [Karaoke-{job_id}] Audio loaded: {len(audio)} samples, {sr} Hz")

        # Separate vocals and instruments
        separator = StemSeparator(model_name="demucs")
        separator.last_input_path = input_path
        vocals_only, _ = separator.separate_two_stems(audio, sr)
        logger.info(f"🎤 [Karaoke-{job_id}] Vocals extracted, instruments REMOVED")

        # Apply tempo adjustment if needed
        if tempo_ratio != 1.0:
            vocals_adjusted = librosa.effects.time_stretch(vocals_only, rate=tempo_ratio)
            logger.info(f"⏱️  [Karaoke-{job_id}] Tempo adjusted: {tempo_ratio}x")
        else:
            vocals_adjusted = vocals_only

        duration = len(vocals_adjusted) / sr
        tempo_bpm = 120 * tempo_ratio

        # Parse instruments
        instruments_list = [i.strip().lower() for i in instruments.split(",")]
        logger.info(f"🎸 [Karaoke-{job_id}] Generating instruments: {instruments_list} in {target_raga}")

        # Generate instruments
        tabla = None
        sitar = None
        guitar = None

        if "tabla" in instruments_list:
            tabla = synthesizer.synthesize_tabla(target_raga, duration, tempo_bpm, sr)
            logger.info(f"✅ [Karaoke-{job_id}] Tabla synthesized")

        if "sitar" in instruments_list:
            sitar = synthesizer.synthesize_sitar(target_raga, duration, tempo_bpm, energy_level, sr)
            logger.info(f"✅ [Karaoke-{job_id}] Sitar synthesized")

        if "guitar" in instruments_list:
            guitar = synthesizer.synthesize_guitar(target_raga, duration, tempo_bpm, sr)
            logger.info(f"✅ [Karaoke-{job_id}] Guitar synthesized")

        # Mix instruments (NO vocals in backing track)
        if tabla is not None and sitar is not None and guitar is not None:
            backing_track = (tabla * 0.5 + sitar * 0.7 + guitar * 0.6)
        elif tabla is not None and sitar is not None:
            backing_track = tabla * 0.5 + sitar * 0.7
        elif sitar is not None:
            backing_track = sitar
        else:
            backing_track = tabla if tabla is not None else guitar

        # Normalize
        max_val = np.max(np.abs(backing_track))
        if max_val > 1.0:
            backing_track = backing_track / (max_val * 1.01)

        backing_track = backing_track.astype(np.float32)

        # Save
        sf.write(str(output_path), backing_track, sr, subtype='PCM_16')
        logger.info(f"✅ [Karaoke-{job_id}] Karaoke backing track saved: {output_path}")

        return {
            "status": "success",
            "job_id": job_id,
            "mode": "karaoke_with_raga",
            "raga": target_raga,
            "instruments": instruments_list,
            "tempo_ratio": tempo_ratio,
            "energy_level": energy_level,
            "duration_seconds": duration,
            "download_url": f"/api/download/{job_id}",
            "description": f"Karaoke backing track in {target_raga} with {', '.join(instruments_list)}. "
                          f"Sing along with your own voice!"
        }

    except Exception as e:
        logger.error(f"❌ [Karaoke] Error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Karaoke generation failed: {str(e)}")

# =========================================================================
# PIPELINE 2: FULL COVER WITH RAGA-BASED INSTRUMENTS
# =========================================================================

@router.post("/mode/cover-with-raga")
async def cover_with_raga(
    file: UploadFile = File(...),
    target_raga: str = Form("yaman"),
    instruments: str = Form("tabla,sitar,guitar"),
    tempo_ratio: float = Form(1.0),
    pitch_semitones: int = Form(0),
    energy_level: float = Form(0.8),
):
    """
    FULL COVER MODE: Generate complete cover with original vocals + Raga instruments.
    
    Process:
    1. Extract vocals from original song
    2. Apply pitch/tempo adjustments (optional)
    3. COMPLETELY REMOVE original instruments
    4. Generate NEW custom instruments in selected Raga
    5. Mix original vocals with custom instruments
    6. Create complete cover song
    
    Example: Ed Sheeran's "Perfect" with Yaman Raga instruments
    
    Parameters:
    - target_raga: Yaman, Bhairav, Khamaaj, etc.
    - instruments: Comma-separated (tabla,sitar,guitar)
    - tempo_ratio: 0.8 (slower) to 1.3 (faster)
    - pitch_semitones: -12 to +12 (shift vocalist up/down)
    - energy_level: 0.5 (soft) to 1.0 (loud)
    
    Returns: Complete cover song (original vocals + new instruments)
    """
    job_id = None
    try:
        # Setup directories
        uploads_dir = Path("uploads")
        outputs_dir = Path("outputs")
        uploads_dir.mkdir(exist_ok=True)
        outputs_dir.mkdir(exist_ok=True)

        job_id = str(uuid.uuid4())[:8]
        input_path = uploads_dir / f"cover_{job_id}_{file.filename}"
        output_path = outputs_dir / f"cover_{target_raga}_{job_id}.wav"

        # Save uploaded file
        content = await file.read()
        input_path.write_bytes(content)
        logger.info(f"📁 [Cover-{job_id}] File uploaded: {input_path}")

        # Load audio
        audio, sr = librosa.load(str(input_path), sr=None, mono=True)
        logger.info(f"🎵 [Cover-{job_id}] Audio loaded: {len(audio)} samples, {sr} Hz")

        # Separate vocals and instruments
        separator = StemSeparator(model_name="demucs")
        separator.last_input_path = input_path
        vocals_only, _ = separator.separate_two_stems(audio, sr)
        logger.info(f"🎤 [Cover-{job_id}] Vocals extracted, instruments REMOVED")

        vocals_adjusted = vocals_only

        # Apply pitch adjustment if needed
        if pitch_semitones != 0:
            vocals_adjusted = librosa.effects.pitch_shift(vocals_adjusted, sr=sr, n_steps=pitch_semitones)
            logger.info(f"🎼 [Cover-{job_id}] Pitch shifted: {pitch_semitones} semitones")

        # Apply tempo adjustment if needed
        if tempo_ratio != 1.0:
            vocals_adjusted = librosa.effects.time_stretch(vocals_adjusted, rate=tempo_ratio)
            logger.info(f"⏱️  [Cover-{job_id}] Tempo adjusted: {tempo_ratio}x")

        vocals_adjusted = vocals_adjusted.astype(np.float32)

        duration = len(vocals_adjusted) / sr
        tempo_bpm = 120 * tempo_ratio

        # Parse instruments
        instruments_list = [i.strip().lower() for i in instruments.split(",")]
        logger.info(f"🎸 [Cover-{job_id}] Generating instruments: {instruments_list} in {target_raga}")

        # Generate instruments
        tabla = None
        sitar = None
        guitar = None

        if "tabla" in instruments_list:
            tabla = synthesizer.synthesize_tabla(target_raga, duration, tempo_bpm, sr)
            logger.info(f"✅ [Cover-{job_id}] Tabla synthesized")

        if "sitar" in instruments_list:
            sitar = synthesizer.synthesize_sitar(target_raga, duration, tempo_bpm, energy_level, sr)
            logger.info(f"✅ [Cover-{job_id}] Sitar synthesized")

        if "guitar" in instruments_list:
            guitar = synthesizer.synthesize_guitar(target_raga, duration, tempo_bpm, sr)
            logger.info(f"✅ [Cover-{job_id}] Guitar synthesized")

        # Mix instruments
        if tabla is not None and sitar is not None and guitar is not None:
            backing_track = (tabla * 0.5 + sitar * 0.7 + guitar * 0.6)
        elif tabla is not None and sitar is not None:
            backing_track = tabla * 0.5 + sitar * 0.7
        elif sitar is not None:
            backing_track = sitar
        else:
            backing_track = tabla if tabla is not None else guitar

        # Ensure same length
        min_len = min(len(vocals_adjusted), len(backing_track))
        vocals_adjusted = vocals_adjusted[:min_len]
        backing_track = backing_track[:min_len]

        # Mix vocals + instruments
        mixed = vocals_adjusted + backing_track
        logger.info(f"🎵 [Cover-{job_id}] Vocals and instruments mixed")

        # Normalize
        max_val = np.max(np.abs(mixed))
        if max_val > 1.0:
            mixed = mixed / (max_val * 1.01)

        mixed = mixed.astype(np.float32)

        # Save
        sf.write(str(output_path), mixed, sr, subtype='PCM_16')
        logger.info(f"✅ [Cover-{job_id}] Full cover saved: {output_path}")

        return {
            "status": "success",
            "job_id": job_id,
            "mode": "cover_with_raga",
            "raga": target_raga,
            "instruments": instruments_list,
            "tempo_ratio": tempo_ratio,
            "pitch_semitones": pitch_semitones,
            "energy_level": energy_level,
            "duration_seconds": duration,
            "download_url": f"/api/download/{job_id}",
            "description": f"Full cover in {target_raga} with {', '.join(instruments_list)}. "
                          f"Original vocals with custom instruments."
        }

    except Exception as e:
        logger.error(f"❌ [Cover] Error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Cover generation failed: {str(e)}")

# =========================================================================
# DOWNLOAD ENDPOINT
# =========================================================================

@app.get("/api/download/{job_id}")
async def download_cover(job_id: str):
    """Download generated cover file."""
    try:
        output_dir = Path("outputs")
        files = list(output_dir.glob(f"*{job_id}*.wav"))

        if not files:
            logger.error(f"❌ File not found for job_id: {job_id}")
            raise HTTPException(status_code=404, detail="Cover file not found")

        output_file = files[0]
        logger.info(f"📥 [Download] Serving: {output_file}")
        return FileResponse(
            path=output_file,
            filename=output_file.name,
            media_type="audio/wav"
        )

    except Exception as e:
        logger.error(f"❌ [Download] Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# =========================================================================
# REGISTER ROUTER
# =========================================================================

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    logger.info("🚀 Starting Raga Remix Studio API v4.0")
    uvicorn.run(app, host="0.0.0.0", port=8000)
