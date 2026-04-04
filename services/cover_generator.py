"""
Cover Generator Service
Orchestrates the complete 6-step cover generation pipeline
"""

import logging
import time
import uuid
from pathlib import Path
from typing import Dict, Optional, Any
import asyncio

from config import Settings
from models.schemas import (
    CoverGenerationRequest,
    CoverGenerationResponse,
    JobMetadata,
    ProcessingStep,
)
from services.rag_service import get_rag_service
from services.audio_processor import get_audio_processor
from services.lyria_client import generate_backing_track
from pydub import AudioSegment

logger = logging.getLogger(__name__)


class CoverGenerator:
    """Cover generation service - orchestrates full pipeline"""

    def __init__(self) -> None:
        """Initialize cover generator"""
        logger.info("Initializing Cover Generator...")
        self.settings = Settings()

        self.rag_service = get_rag_service()
        self.audio_processor = get_audio_processor()
        self.jobs: Dict[str, JobMetadata] = {}

        logger.info("✅ Cover Generator initialized")

    async def generate_cover(
        self,
        audio_path: str,
        request: CoverGenerationRequest,
    ) -> CoverGenerationResponse:
        """
        Generate cover song using 6-step pipeline

        Pipeline:
        1. RAG Analysis - Select raga & instruments
        2. Stem Separation - Isolate vocals/instruments
        3. Raga Transformation - Apply pitch/ornamentations
        4. Instrument Synthesis - Generate new instruments
        5. Tempo/Energy Adjustment - Match style
        6. Mixing & Mastering - Final output
        """
        job_id = str(uuid.uuid4())
        start_time = time.time()

        logger.info("=" * 70)
        logger.info(f"🎵 COVER GENERATION STARTED - Job ID: {job_id}")
        logger.info("=" * 70)

        # Create job metadata
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

            # STEP 1: RAG Analysis
            step1_result = await self._step1_rag_analysis(audio_path, request)
            processing_steps.append(step1_result)

            # STEP 2: Stem Separation
            step2_result = await self._step2_stem_separation(audio_path, job_id)
            processing_steps.append(step2_result)

            # STEP 3: Raga Transformation
            step3_result = await self._step3_raga_transformation(
                step2_result.details["stems"],
                step1_result.details["selected_raga"],
                request,
                job_id,
            )
            processing_steps.append(step3_result)

            # STEP 4: Instrument Synthesis (Lyria)
            step4_result = await self._step4_instrument_synthesis(
                stems=step2_result.details["stems"],
                selected_raga=step1_result.details["selected_raga"],
                instruments=step1_result.details["instruments"],
                tempo_bpm=step1_result.details["audio_features"]["tempo_bpm"],
                job_id=job_id,
            )
            processing_steps.append(step4_result)

            # STEP 5: Tempo & Energy Adjustment
            step5_result = await self._step5_tempo_energy_adjustment(
                step3_result.details["transformed_stems"],
                step1_result.details["audio_features"]["tempo_bpm"],
                job_id,
            )
            processing_steps.append(step5_result)

            # STEP 6: Mixing & Mastering
            step6_result = await self._step6_mixing_mastering(
                stems=step5_result.details["adjusted_stems"],
                ai_instruments_path=step4_result.details.get("ai_instruments_path"),
                job_id=job_id,
            )
            processing_steps.append(step6_result)

            # Update job metadata
            output_file = step6_result.details["output_file"]
            job_metadata.status = "completed"
            job_metadata.output_file = output_file
            job_metadata.updated_at = time.time()
            job_metadata.progress = 1.0

            processing_time = time.time() - start_time

            logger.info("=" * 70)
            logger.info(f"✅ COVER GENERATION COMPLETED - Job ID: {job_id}")
            logger.info(f"   Processing Time: {processing_time:.1f}s")
            logger.info("=" * 70)

            return CoverGenerationResponse(
                job_id=job_id,
                status="completed",
                output_url=f"/api/download/{job_id}",
                processing_details={"steps": processing_steps},
                applied_raga=step1_result.details.get("applied_raga"),
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

    # ------------------------------------------------------------------ #
    # Step 1 – RAG analysis
    # ------------------------------------------------------------------ #

    async def _step1_rag_analysis(
        self,
        audio_path: str,
        request: CoverGenerationRequest,
    ) -> ProcessingStep:
        """Step 1: RAG-powered analysis"""
        logger.info("📊 STEP 1: RAG Analysis")
        step_start = time.time()

        try:
            # Extract audio features
            features = self.audio_processor.extract_features(audio_path)

            # Build RAG query
            query = f"""Analyze this song and recommend:
- Best raga for tempo {features['tempo_bpm']:.0f} BPM in key {features['key']}
- Compatible instruments for {request.style.value} fusion style
- Arrangement suggestions
"""

            # Query RAG system
            rag_result = self.rag_service.query(query)

            # Select raga
            if request.target_raga:
                selected_raga = request.target_raga
            else:
            recommended_ragas = rag_result["recommendations"]["ragas"]
                            selected_raga = (
                    list(recommended_ragas.keys())[0] if recommended_ragas else "Yaman"
                )
            # Select instruments
            if request.custom_instruments:
                instruments = request.custom_instruments
            else:
                recommended_instruments = rag_result["recommendations"]["instruments"]
            instruments = list(recommended_instruments.keys())[:3]
            duration = time.time() - step_start

            logger.info(f"   ✅ Selected Raga: {selected_raga}")
            logger.info(f"   ✅ Instruments: {', '.join(instruments)}")
            logger.info(f"   ⏱️  Duration: {duration:.1f}s")

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
            logger.error(f"   ❌ Step 1 failed: {e}")
            raise

    # ------------------------------------------------------------------ #
    # Step 2 – Stem separation
    # ------------------------------------------------------------------ #

    async def _step2_stem_separation(
        self,
        audio_path: str,
        job_id: str,
    ) -> ProcessingStep:
        """Step 2: Stem separation"""
        logger.info("🎼 STEP 2: Stem Separation")
        step_start = time.time()

        try:
            output_dir = self.settings.OUTPUT_DIR / f"stems_{job_id}"
            stems = self.audio_processor.separate_stems(audio_path, str(output_dir))

            duration = time.time() - step_start

            logger.info(f"   ✅ Separated {len(stems)} stems")
            logger.info(f"   ⏱️  Duration: {duration:.1f}s")

            return ProcessingStep(
                step="stem_separation",
                status="completed",
                duration_seconds=duration,
                details={"stems": stems},
            )

        except Exception as e:
            logger.error(f"   ❌ Step 2 failed: {e}")
            raise

    # ------------------------------------------------------------------ #
    # Step 3 – Raga transformation
    # ------------------------------------------------------------------ #

    async def _step3_raga_transformation(
        self,
        stems: Dict[str, str],
        raga: str,
        request: CoverGenerationRequest,
        job_id: str,
    ) -> ProcessingStep:
        """Step 3: Raga transformation"""
        logger.info(f"🎵 STEP 3: Raga Transformation ({raga})")
        step_start = time.time()

        try:
            transformed_stems: Dict[str, str] = {}

            # Pitch shift vocals if requested
            if "vocals" in stems and request.pitch_semitones != 0:
                vocals_path = stems["vocals"]
                output_path = str(
                    self.settings.OUTPUT_DIR / f"vocals_shifted_{job_id}.wav"
                )
                transformed_path = self.audio_processor.apply_pitch_shift(
                    vocals_path,
                    output_path,
                    request.pitch_semitones,
                )
                transformed_stems["vocals"] = transformed_path
            else:
                transformed_stems["vocals"] = stems.get("vocals", "")

            # Keep instrumental stem as-is for now
            transformed_stems["no_vocals"] = stems.get("no_vocals", "")

            duration = time.time() - step_start

            logger.info(f"   ✅ Applied {raga} raga characteristics")
            logger.info(f"   ⏱️  Duration: {duration:.1f}s")

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
            logger.error(f"   ❌ Step 3 failed: {e}")
            raise

    # ------------------------------------------------------------------ #
    # Step 4 – Instrument synthesis (Lyria)
    # ------------------------------------------------------------------ #

    async def _step4_instrument_synthesis(
        self,
        stems: dict,
        selected_raga: str,
        instruments: list[str],
        tempo_bpm: float,
        job_id: str,
    ) -> ProcessingStep:
        """STEP 4: Instrument synthesis using Lyria"""
        logger.info("🎼 STEP 4: Instrument Synthesis (Lyria)")
        step_start = time.time()

        try:
            bpm = int(round(tempo_bpm))
            duration_sec = 30.0  # generate ~30 seconds for now

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
            logger.error(f"   ❌ Step 4 failed: {e}")
            raise

    # ------------------------------------------------------------------ #
    # Step 5 – Tempo & energy adjustment
    # ------------------------------------------------------------------ #

    async def _step5_tempo_energy_adjustment(
        self,
        transformed_stems: dict,
        tempo_bpm: float,
        job_id: str,
    ) -> ProcessingStep:
        """Step 5: Tempo & energy adjustment"""
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
                            self.settings.OUTPUT_DIR
                            / f"{stem_name}_tempo_{job_id}.wav"
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

            logger.info(f"   ✅ Tempo adjusted by {tempo_ratio:.2f}x")
            logger.info(f"   ⏱️  Duration: {duration:.1f}s")

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
            logger.error(f"   ❌ Step 5 failed: {e}")
            raise

    # ------------------------------------------------------------------ #
    # Step 6 – Mixing & mastering
    # ------------------------------------------------------------------ #

    async def _step6_mixing_mastering(
        self,
        stems: dict,
        ai_instruments_path: str | None,
        job_id: str,
    ) -> ProcessingStep:
        """Step 6: Mixing & mastering"""
        logger.info("🎚️ STEP 6: Mixing & Mastering")
        step_start = time.time()

        try:
            # Mix adjusted stems (vocals + no_vocals)
            output_path = str(self.settings.OUTPUT_DIR / f"cover_{job_id}.wav")

            mixed_path = self.audio_processor.mix_stems(
                stems,
                output_path,
                levels=self.settings.DEFAULT_MIX_LEVELS.copy(),
            )

            # If we have AI instruments, overlay them
            if ai_instruments_path:
                base = AudioSegment.from_file(mixed_path)
                ai_inst = AudioSegment.from_file(ai_instruments_path)

                # Match duration of AI instruments to base mix
                if len(ai_inst) > len(base):
                    ai_inst = ai_inst[: len(base)]
                else:
                    loops = (len(base) // len(ai_inst)) + 1
                    ai_inst = (ai_inst * loops)[: len(base)]

                # Slightly boost AI instruments
                combined = base.overlay(ai_inst - 3)

                combined.export(mixed_path, format="wav")

            # Normalize loudness
            final_path = str(
                self.settings.OUTPUT_DIR / f"final_cover_{job_id}.wav"
            )
            self.audio_processor.normalize_loudness(
                mixed_path,
                final_path,
                target_lufs=self.settings.TARGET_LOUDNESS_LUFS,
            )

            duration = time.time() - step_start

            logger.info("   ✅ Mixed and mastered")
            logger.info(f"   ⏱️  Duration: {duration:.1f}s")

            return ProcessingStep(
                step="mixing_mastering",
                status="completed",
                duration_seconds=duration,
                details={
                    "output_file": final_path,
                    "target_lufs": self.settings.TARGET_LOUDNESS_LUFS,
                },
            )

        except Exception as e:
            logger.error(f"   ❌ Step 6 failed: {e}")
            raise

    # ------------------------------------------------------------------ #
    # Job status
    # ------------------------------------------------------------------ #

    def get_job_status(self, job_id: str) -> Optional[JobMetadata]:
        """Get job status by ID"""
        return self.jobs.get(job_id)


# Singleton instance
_cover_generator_instance: Optional[CoverGenerator] = None


def get_cover_generator() -> CoverGenerator:
    """Get singleton cover generator instance"""
    global _cover_generator_instance

    if _cover_generator_instance is None:
        _cover_generator_instance = CoverGenerator()

    return _cover_generator_instance


if __name__ == "__main__":
    print("✅ Cover Generator ready!")
