# services/lyria_client.py

import asyncio
import wave
from pathlib import Path
from typing import List

from google import genai
from google.genai import types

client = genai.Client(http_options={"api_version": "v1alpha"})


async def generate_backing_track(
    prompt_texts: List[str],
    bpm: int,
    duration_seconds: float,
    output_path: Path,
) -> Path:
    """Generate instrumental backing with Lyria and save as WAV."""

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

    output_path.parent.mkdir(parents=True, exist_ok=True)

    if not pcm_frames:
        raise RuntimeError("Lyria did not return any audio data")

    with wave.open(str(output_path), "wb") as wf:
        wf.setnchannels(num_channels)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate_hz)
        wf.writeframes(bytes(pcm_frames))

    return output_path

