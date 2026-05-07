"""
Cover Generator Service
Orchestrates the complete 6-step cover generation pipeline
"""

import logging
import time
import uuid
from pathlib import Path
from typing import Dict, Optional
import asyncio

from config import Settings
from models.schemas import (
    CoverGenerationRequest,
    CoverGenerationResponse,
    JobMetadata,
    ProcessingStep,
    InstrumentMode,
)
from services.rag_service import get_rag_service
from services.audio_processor import get_audio_processor
from services.lyria_client import generate_backing_track
from pydub import AudioSegment

logger = logging.getLogger(__name__)


class CoverGenerator:
    """Cover generation service - orchestrates full pipeline"""

    def __init__(self) -> None:
        logger.info("Initializing Cover Generator...")
        self.settings = Settings()
        self.rag_service = get_rag_service()
        self.audio_processor = get_audio_processor()
        self.jobs: Dict[str, JobMetadata] = {}
        logger.info("✅ Cover Generator initialized")

    def create_pending_job(
        self,
        audio_path: str,
        request: CoverGenerationRequest,
        ) -> str:
        """Create a pending job and return job_id immediately."""
        import uuid as _uuid
        job_id = str(_uuid.uuid4())
        start_time = time.time()
        job_metadata = JobMetadata(
            job_id=job_id,
            status="queued",
            created_at=start_time,
            updated_at=start_time,
            input_file=audio_path,
            request=request.dict(),
        )
        self.jobs[job_id] = job_metadata
        logger.info(f"Created pending job {job_id}")
        return job_id

        async def generate_cover(
        self,
        audio_path: str,
        request: CoverGenerationRequest,
        job_id: Optional[str] = None,
    ) -> CoverGenerationResponse:
        """
        Generate cover song using 6-step pipeline

        Pipeline:
        1. RAG Analysis
        2. Stem Separation
        3. Raga Transformation
        4. Instrument Synthesis
        5. Tempo/Energy Adjustment
        6. Mixing & Mastering
        """
        job_id = job_id or str(uuid.uuid4())
        start_time = time.time()

        logger.info("=" * 70)
        logger.info(f"🎵 COVER GENERATION STARTED - Job ID: {job_id}")
        logger.info(f"🎚️ Instrument mode: {request.instrument_mode}")
        logger.info("=" * 70)

if job_id in self.jobs:
            job_metadata = self.jobs[job_id]
            job_metadata.status = "processing"
            job_metadata.updated_at = start_time
        else:
            job_metadata = JobMetadata(
                job_id=job_id,
                status="processing",
                created_at=start_time,
                updated_at=start_time,
                input_file=audio_path,
                request=request.dict(),
            )
            self.jobs[job_id] = job_metadata

        try:
            processing_steps: list[ProcessingStep] = []

            step1_result = await self._step1_rag_analysis(audio_path, request)
            processing_steps.append(step1_result)

            step2_result = await self._step2_stem_separation(audio_path, job_id)
            processing_steps.append(step2_result)

            step3_result = await self._step3_raga_transformation(
                step2_result.details["stems"],
                step1_result.details["selected_raga"],
                request,
                job_id,
            )
            processing_steps.append(step3_result)

            step4_result = await self._step4_instrument_synthesis(
                stems=step2_result.details["stems"],
                selected_raga=step1_result.details["selected_raga"],
                instruments=step1_result.details["instruments"],
                tempo_bpm=step1_result.details["audio_features"]["tempo_bpm"],
                job_id=job_id,
            )
            processing_steps.append(step4_result)

            step5_result = await self._step5_tempo_energy_adjustment(
                step3_result.details["transformed_stems"],
                step1_result.details["audio_features"]["tempo_bpm"],
                job_id,
            )
            processing_steps.append(step5_result)

            step6_result = await self._step6_mixing_mastering(
                stems=step5_result.details["adjusted_stems"],
                ai_instruments_path=step4_result.details.get("ai_instruments_path"),
                instrument_mode=request.instrument_mode,
                job_id=job_id,
            )
            processing_steps.append(step6_result)

            output_file = step6_result.details["output_file"]
            job_metadata.status = "completed"
            job_metadata.output_file = output_file
            job_metadata.updated_at = time.time()
            job_metadata.progress = 1.0

            processing_time = time.time() - start_time

            logger.info("=" * 70)
            logger.info(f"✅ COVER GENERATION COMPLETED - Job ID: {job_id}")
            logger.info(f"⏱️ Processing Time: {processing_time:.1f}s")
            logger.info("=" * 70)

            return CoverGenerationResponse(
                job_id=job_id,
                status="completed",
                output_url=f"/api/download/{job_id}",
                processing_details={"steps": [step.dict() for step in processing_steps]},
                applied_raga=step1_result.details.get("selected_raga"),
                instruments_used=step1_result.details.get("instruments", []),
                processing_time_seconds=processing_time,
            )

        except Exception as e:
            logger.error(f"❌ Cover generation failed: {e}", exc_info=True)
            job_metadata.status = "failed"
            job_metadata.error = str(e)
            job_metadata.updated_at = time.time()

            return CoverGenerationResponse(
                job_id=job_id,
                status="failed",
                error_message=str(e),
                instruments_used=[],
            )

    async def _step1_rag_analysis(
        self,
        audio_path: str,
        request: CoverGenerationRequest,
    ) -> ProcessingStep:
        logger.info("📊 STEP 1: RAG Analysis")
        step_start = time.time()

        try:
            features = self.audio_processor.extract_features(audio_path)

            query = f"""Analyze this song and recommend:
- Best raga for tempo {features['tempo_bpm']:.0f} BPM in key {features['key']}
- Compatible instruments for {request.style.value} fusion style
- Arrangement suggestions
"""

            rag_result = self.rag_service.query(query)

            if request.target_raga:
                selected_raga = request.target_raga
            else:
                recommended_ragas = rag_result["recommendations"]["ragas"]
                selected_raga = list(recommended_ragas.keys())[0] if recommended_ragas else "Yaman"

            if request.custom_instruments:
                instruments = request.custom_instruments
            else:
                recommended_instruments = rag_result["recommendations"]["instruments"]
                instruments = list(recommended_instruments.keys())[:3]

            duration = time.time() - step_start

            return ProcessingStep(
                step="rag_analysis",
                status="completed",
                duration_seconds=duration,
                details={
                    "selected_raga": selected_raga,
                    "instruments": instruments,
                    "audio_features": features,
                    "rag_confidence": rag_result["confidence"],
                },
            )

        except Exception as e:
            logger.error(f"❌ Step 1 failed: {e}")
            raise

    async def _step2_stem_separation(
        self,
        audio_path: str,
        job_id: str,
    ) -> ProcessingStep:
        logger.info("🎼 STEP 2: Stem Separation")
        step_start = time.time()

        try:
            output_dir = self.settings.OUTPUT_DIR / f"stems_{job_id}"
            stems = self.audio_processor.separate_stems(audio_path, str(output_dir))
            duration = time.time() - step_start

            return ProcessingStep(
                step="stem_separation",
                status="completed",
                duration_seconds=duration,
                details={"stems": stems},
            )

        except Exception as e:
            logger.error(f"❌ Step 2 failed: {e}")
            raise

    async def _step3_raga_transformation(
        self,
        stems: Dict[str, str],
        raga: str,
        request: CoverGenerationRequest,
        job_id: str,
    ) -> ProcessingStep:
        logger.info(f"🎵 STEP 3: Raga Transformation ({raga})")
        step_start = time.time()

        try:
            transformed_stems: Dict[str, str] = {}

            if "vocals" in stems and request.pitch_semitones != 0:
                vocals_path = stems["vocals"]
                output_path = str(self.settings.OUTPUT_DIR / f"vocals_shifted_{job_id}.wav")
                transformed_path = self.audio_processor.apply_pitch_shift(
                    vocals_path,
                    output_path,
                    request.pitch_semitones,
                )
                transformed_stems["vocals"] = transformed_path
            else:
                transformed_stems["vocals"] = stems.get("vocals", "")

            transformed_stems["no_vocals"] = stems.get("no_vocals", "")
            duration = time.time() - step_start

            return ProcessingStep(
                step="raga_transformation",
                status="completed",
                duration_seconds=duration,
                details={
                    "raga": raga,
                    "transformed_stems": transformed_stems,
                },
            )

        except Exception as e:
            logger.error(f"❌ Step 3 failed: {e}")
            raise

    async def _step4_instrument_synthesis(
        self,
        stems: dict,
        selected_raga: str,
        instruments: list[str],
        tempo_bpm: float,
        job_id: str,
    ) -> ProcessingStep:
        logger.info("🎼 STEP 4: Instrument Synthesis (Lyria)")
        step_start = time.time()

        try:
            bpm = int(round(tempo_bpm))
            duration_sec = 30.0

            prompt_texts = [
                f"Indian classical fusion in raga {selected_raga}",
                f"Instruments: {', '.join(instruments)}",
                "No vocals, only instrumental backing track",
                "Modern clean mix suitable for Bollywood-style cover song",
            ]

            ai_path = self.settings.OUTPUT_DIR / f"ai_backing_{job_id}.wav"

            await generate_backing_track(
                prompt_texts=prompt_texts,
                bpm=bpm,
                duration_seconds=duration_sec,
                output_path=ai_path,
            )

            duration = time.time() - step_start

            return ProcessingStep(
                step="instrument_synthesis",
                status="completed",
                duration_seconds=duration,
                details={
                    "ai_instruments_path": str(ai_path),
                    "bpm": bpm,
                    "instruments": instruments,
                    "selected_raga": selected_raga,
                },
            )

        except Exception as e:
            logger.error(f"❌ Step 4 failed: {e}")
            raise

    async def _step5_tempo_energy_adjustment(
        self,
        transformed_stems: dict,
        tempo_bpm: float,
        job_id: str,
    ) -> ProcessingStep:
        logger.info("⚡ STEP 5: Tempo & Energy Adjustment")
        step_start = time.time()

        try:
            adjusted_stems: dict = {}

            target_bpm = round(tempo_bpm)
            tempo_ratio = target_bpm / tempo_bpm if tempo_bpm > 0 else 1.0

            if tempo_ratio != 1.0:
                logger.info(f"Applying tempo stretch: {tempo_ratio:.2f}x")
                for stem_name, stem_path in transformed_stems.items():
                    if stem_path and Path(stem_path).exists():
                        output_path = str(
                            self.settings.OUTPUT_DIR / f"{stem_name}_tempo_{job_id}.wav"
                        )
                        adjusted_path = self.audio_processor.apply_time_stretch(
                            stem_path,
                            output_path,
                            tempo_ratio,
                        )
                        adjusted_stems[stem_name] = adjusted_path
            else:
                adjusted_stems = transformed_stems

            duration = time.time() - step_start

            return ProcessingStep(
                step="tempo_energy_adjustment",
                status="completed",
                duration_seconds=duration,
                details={
                    "tempo_ratio": tempo_ratio,
                    "energy_level": None,
                    "adjusted_stems": adjusted_stems,
                },
            )

        except Exception as e:
            logger.error(f"❌ Step 5 failed: {e}")
            raise

    async def _step6_mixing_mastering(
        self,
        stems: dict,
        ai_instruments_path: Optional[str],
        instrument_mode: InstrumentMode,
        job_id: str,
    ) -> ProcessingStep:
        logger.info("🎚️ STEP 6: Mixing & Mastering")
        step_start = time.time()

        try:
            vocals_path = stems.get("vocals")
            original_instrumental_path = stems.get("no_vocals")

            if not vocals_path or not Path(vocals_path).exists():
                raise ValueError("Vocals stem not found for final mix")

            vocals_audio = AudioSegment.from_file(vocals_path)

            if instrument_mode == InstrumentMode.mute:
                final_mix = vocals_audio
                selected_mode = "vocals_only"

            elif instrument_mode == InstrumentMode.original:
                if not original_instrumental_path or not Path(original_instrumental_path).exists():
                    raise ValueError("Original instrumental stem not found")
                instrumental_audio = AudioSegment.from_file(original_instrumental_path)
                final_mix = self._match_and_overlay(instrumental_audio, vocals_audio)
                selected_mode = "original_instrumental"

            elif instrument_mode == InstrumentMode.ai:
                if not ai_instruments_path or not Path(ai_instruments_path).exists():
                    raise ValueError("AI instrumental file not found")
                ai_audio = AudioSegment.from_file(ai_instruments_path)
                final_mix = self._match_and_overlay(ai_audio - 3, vocals_audio)
                selected_mode = "ai_instrumental"

            else:
                raise ValueError(f"Unsupported instrument_mode: {instrument_mode}")

            mixed_path = str(self.settings.OUTPUT_DIR / f"cover_{job_id}.wav")
            final_mix.export(mixed_path, format="wav")

            final_path = str(self.settings.OUTPUT_DIR / f"final_cover_{job_id}.wav")
            self.audio_processor.normalize_loudness(
                mixed_path,
                final_path,
                target_lufs=self.settings.TARGET_LOUDNESS_LUFS,
            )

            duration = time.time() - step_start

            return ProcessingStep(
                step="mixing_mastering",
                status="completed",
                duration_seconds=duration,
                details={
                    "output_file": final_path,
                    "target_lufs": self.settings.TARGET_LOUDNESS_LUFS,
                    "instrument_mode": selected_mode,
                },
            )

        except Exception as e:
            logger.error(f"❌ Step 6 failed: {e}")
            raise

    def _match_and_overlay(self, backing: AudioSegment, vocals: AudioSegment) -> AudioSegment:
        if len(backing) > len(vocals):
            backing = backing[:len(vocals)]
        elif len(backing) < len(vocals):
            loops = (len(vocals) // len(backing)) + 1
            backing = (backing * loops)[:len(vocals)]

        return backing.overlay(vocals)

    def get_job_status(self, job_id: str) -> Optional[JobMetadata]:
        return self.jobs.get(job_id)


_cover_generator_instance: Optional[CoverGenerator] = None


def get_cover_generator() -> CoverGenerator:
    global _cover_generator_instance

    if _cover_generator_instance is None:
        _cover_generator_instance = CoverGenerator()

    return _cover_generator_instance


if __name__ == "__main__":
    print("✅ Cover Generator ready!")
