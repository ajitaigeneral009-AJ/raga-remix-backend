import asyncio
import wave
from pathlib import Path

from google import genai
from google.genai import types

client = genai.Client(http_options={"api_version": "v1alpha"})

OUTPUT_WAV = Path("lyria_test.wav")


async def main():
    sample_rate_hz = 44100
    num_channels = 2
    pcm_frames = bytearray()
    target_seconds = 5.0            # how long we want to record
    total_seconds = 0.0
    done = asyncio.Event()

    async def receive_audio(session):
        nonlocal pcm_frames, total_seconds
        async for message in session.receive():
            if not message.server_content.audio_chunks:
                continue
            chunk = message.server_content.audio_chunks[0]
            data = chunk.data
            print("chunk bytes:", len(data))
            pcm_frames.extend(data)

            seconds = len(data) / (sample_rate_hz * num_channels * 2)
            total_seconds += seconds
            if total_seconds >= target_seconds:
                # tell main to stop
                done.set()
                return

    async with client.aio.live.music.connect(
        model="models/lyria-realtime-exp"
    ) as session:
        recv_task = asyncio.create_task(receive_audio(session))

        await session.set_weighted_prompts(
            prompts=[
                types.WeightedPrompt(
                    text="instrumental sitar and tabla in raga Yaman, 4/4, 140 BPM",
                    weight=1.0,
                )
            ]
        )
        await session.set_music_generation_config(
            config=types.LiveMusicGenerationConfig(
                bpm=140,
                temperature=1.0,
            )
        )

        await session.play()

        # wait until receive_audio says we have enough audio
        await done.wait()
        await session.stop()
        await recv_task

    # write WAV
    if pcm_frames:
        with wave.open(str(OUTPUT_WAV), "wb") as wf:
            wf.setnchannels(num_channels)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate_hz)
            wf.writeframes(bytes(pcm_frames))

        print(f"Saved WAV to {OUTPUT_WAV.resolve()}")
    else:
        print("No audio frames received")


if __name__ == "__main__":
    asyncio.run(main())
