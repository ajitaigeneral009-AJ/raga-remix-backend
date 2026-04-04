# services/lyria_client.py
import asyncio
import logging
import os
import wave
from pathlib import Path
from typing import List

logger = logging.getLogger(__name__)

# Lazy import - only load google.genai when actually needed
_genai_available = False
try:
    from google import genai
    from google.genai import types
    _genai_available = True
    logger.info("google-generativeai SDK loaded successfully")
except ImportError as e:
    logger.warning(f"google-generativeai not available: {e}. Lyria will use fallback.")


def _get_client():
    """Get Lyria client with API key from environment."""
    if not _genai_available:
        raise RuntimeError("google-generativeai package not installed")
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not set in environment")
    return genai.Client(
        api_key=api_key,
        http_options={"api_version": "v1alpha"}
    )


async def generate_backing_track(
    prompt_texts: List[str],
    bpm: int,
    duration_seconds: float,
    output_path: Path,
) -> Path:
    """Generate instrumental backing with Lyria and save as WAV.
    Falls back to silence if Lyria is unavailable.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if not _genai_available:
        logger.warning("Lyria unavailable - writing silent placeholder WAV")
        _write_silence(output_path, duration_seconds)
        return output_path

    try:
        client = _get_client()
    except RuntimeError as e:
        logger.warning(f"Lyria client error: {e} - writing silent placeholder WAV")
        _write_silence(output_path, duration_seconds)
        return output_path

    sample_rate_hz = 44100
    num_channels = 2
    pcm_frames = bytearray()
    total_seconds = 0.0
    done = asyncio.Event()

    async def receive_audio(session):
        nonlocal pcm_frames, total_seconds
        async for message in session.receive():
            if not message.server_content.audio_chunks:
                continue
            chunk = message.server_content.audio_chunks[0]
            data = chunk.data
            pcm_frames.extend(data)
            seconds = len(data) / (sample_rate_hz * num_channels * 2)
            total_seconds += seconds
            if total_seconds >= duration_seconds:
                done.set()
                return

    try:
        prompts = [types.WeightedPrompt(text=t, weight=1.0) for t in prompt_texts]
        async with client.aio.live.music.connect(
            model="models/lyria-realtime-exp"
        ) as session:
            recv_task = asyncio.create_task(receive_audio(session))
            await session.set_weighted_prompts(prompts=prompts)
            await session.set_music_generation_config(
                config=types.LiveMusicGenerationConfig(
                    bpm=bpm,
                    temperature=1.0,
                )
            )
            await session.play()
            await done.wait()
            await session.stop()
            await recv_task

        if not pcm_frames:
            raise RuntimeError("Lyria returned no audio data")

        with wave.open(str(output_path), "wb") as wf:
            wf.setnchannels(num_channels)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate_hz)
            wf.writeframes(bytes(pcm_frames))

        logger.info(f"Lyria backing track saved: {output_path}")
        return output_path

    except Exception as e:
        logger.error(f"Lyria generation failed: {e} - using silent fallback")
        _write_silence(output_path, duration_seconds)
        return output_path


def _write_silence(output_path: Path, duration_seconds: float) -> None:
    """Write a silent WAV file as placeholder."""
    sample_rate = 44100
    num_channels = 2
    num_frames = int(sample_rate * duration_seconds)
    silence = b'\x00\x00' * num_channels * num_frames
    with wave.open(str(output_path), "wb") as wf:
        wf.setnchannels(num_channels)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(silence)
    logger.info(f"Silent placeholder written: {output_path}")
