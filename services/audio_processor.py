"""
Audio Processor Service
Handles audio processing operations: stem separation, feature extraction, mixing
"""

import logging
import subprocess
import json
from pathlib import Path
from typing import Dict, Optional

import librosa
import numpy as np
import soundfile as sf

from config import Settings

logger = logging.getLogger(__name__)


class AudioProcessor:
    """Audio processing service for stem separation and feature extraction"""

    def __init__(self) -> None:
        self.settings = Settings()

        self.sample_rate = self.settings.SAMPLE_RATE
        self.target_lufs = self.settings.TARGET_LOUDNESS_LUFS
        self.temp_upload_dir = self.settings.TEMP_UPLOAD_DIR
        self.output_dir = self.settings.OUTPUT_DIR

    def separate_stems(self, audio_path: str, output_dir: str) -> Dict[str, str]:
        """
        Separate audio into stems using Demucs.
        """
        logger.info(f"Starting stem separation: {audio_path}")

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        try:
            # Run Demucs
            cmd = [
                "demucs",
                "--two-stems=vocals",  # Separate vocals and accompaniment
                "-n",
                self.settings.DEMUCS_MODEL,
                "-o",
                str(output_path),
                audio_path,
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.settings.PROCESSING_TIMEOUT_SECONDS,
            )

            if result.returncode != 0:
                logger.error(f"Demucs failed: {result.stderr}")
                raise RuntimeError(f"Stem separation failed: {result.stderr}")

            # Find output files
            model_dir = output_path / self.settings.DEMUCS_MODEL
            audio_name = Path(audio_path).stem
            stem_dir = model_dir / audio_name

            stems = {
                "vocals": str(stem_dir / "vocals.wav"),
                "no_vocals": str(stem_dir / "no_vocals.wav"),
            }

            # Verify stems exist
            for stem_name, stem_path in stems.items():
                if not Path(stem_path).exists():
                    raise FileNotFoundError(f"Stem not found: {stem_path}")

            logger.info(f"✅ Stem separation complete: {len(stems)} stems")
            return stems

        except subprocess.TimeoutExpired:
            raise RuntimeError("Stem separation timed out")
        except Exception as e:
            logger.error(f"Stem separation failed: {e}")
            raise

    def extract_features(self, audio_path: str) -> Dict:
        """
        Extract audio features using librosa.
        """
        logger.info(f"Extracting audio features: {audio_path}")

        y, sr = librosa.load(audio_path, sr=self.sample_rate)

        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
        spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
        zero_crossing_rate = librosa.feature.zero_crossing_rate(y)[0]
        rms = librosa.feature.rms(y=y)[0]
        energy = float(np.mean(rms))

        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        key_index = int(np.argmax(np.sum(chroma, axis=1)))
        keys = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        detected_key = keys[key_index]

        features = {
            "tempo_bpm": float(tempo),
            "key": f"{detected_key} major",
            "energy": float(np.clip(energy * 10, 0, 1)),
            "spectral_centroid": float(np.mean(spectral_centroids)),
            "spectral_rolloff": float(np.mean(spectral_rolloff)),
            "zero_crossing_rate": float(np.mean(zero_crossing_rate)),
            "duration_seconds": float(librosa.get_duration(y=y, sr=sr)),
            "danceability": float(np.clip(tempo / 140, 0, 1)),
            "valence": float(np.clip(energy, 0, 1)),
        }

        logger.info(
            f"✅ Features extracted: Tempo={features['tempo_bpm']:.1f} BPM, "
            f"Key={features['key']}"
        )
        return features

    def apply_pitch_shift(
        self, audio_path: str, output_path: str, semitones: int
    ) -> str:
        """Apply pitch shift to audio."""
        logger.info(f"Applying pitch shift: {semitones} semitones")

        if semitones == 0:
            return audio_path

        y, sr = librosa.load(audio_path, sr=self.sample_rate)
        y_shifted = librosa.effects.pitch_shift(y, sr=sr, n_steps=semitones)
        sf.write(output_path, y_shifted, sr)

        logger.info(f"✅ Pitch shifted audio saved: {output_path}")
        return output_path

    def apply_time_stretch(
        self, audio_path: str, output_path: str, ratio: float
    ) -> str:
        """Apply time stretching to audio."""
        logger.info(f"Applying time stretch: {ratio}x")

        if ratio == 1.0:
            return audio_path

        y, sr = librosa.load(audio_path, sr=self.sample_rate)
        y_stretched = librosa.effects.time_stretch(y, rate=ratio)
        sf.write(output_path, y_stretched, sr)

        logger.info(f"✅ Time stretched audio saved: {output_path}")
        return output_path

    def mix_stems(
        self,
        stems: Dict[str, str],
        output_path: str,
        levels: Optional[Dict[str, float]] = None,
    ) -> str:
        """
        Mix multiple audio stems together.
        """
        logger.info(f"Mixing {len(stems)} stems...")

        if levels is None:
            levels = {name: 0.0 for name in stems.keys()}

        mixed_audio = None
        max_length = 0

        for stem_name, stem_path in stems.items():
            if not Path(stem_path).exists():
                logger.warning(f"Stem not found, skipping: {stem_path}")
                continue

            y, sr = librosa.load(stem_path, sr=self.sample_rate)

            level_db = levels.get(stem_name, 0.0)
            level_linear = 10 ** (level_db / 20)
            y = y * level_linear

            max_length = max(max_length, len(y))

            if mixed_audio is None:
                mixed_audio = y
            else:
                if len(y) < len(mixed_audio):
                    y = np.pad(y, (0, len(mixed_audio) - len(y)))
                elif len(y) > len(mixed_audio):
                    mixed_audio = np.pad(mixed_audio, (0, len(y) - len(mixed_audio)))
                mixed_audio += y

        max_val = np.max(np.abs(mixed_audio))
        if max_val > 0:
            mixed_audio = mixed_audio / max_val * 0.95

        sf.write(output_path, mixed_audio, self.sample_rate)
        logger.info(f"✅ Mixed audio saved: {output_path}")
        return output_path

    def normalize_loudness(
        self,
        audio_path: str,
        output_path: str,
        target_lufs: float = -14.0,
    ) -> str:
        """Normalize audio loudness to target LUFS (approx)."""
        logger.info(f"Normalizing loudness to {target_lufs} LUFS")

        y, sr = librosa.load(audio_path, sr=self.sample_rate)
        rms = np.sqrt(np.mean(y**2))
        target_rms = 10 ** (target_lufs / 20)

        if rms > 0:
            y_normalized = y * (target_rms / rms)
            max_val = np.max(np.abs(y_normalized))
            if max_val > 1.0:
                y_normalized = y_normalized / max_val * 0.95
        else:
            y_normalized = y

        sf.write(output_path, y_normalized, sr)
        logger.info(f"✅ Loudness normalized: {output_path}")
        return output_path

    def health_check(self) -> Dict[str, str]:
        """Check audio processor health."""
        try:
            result = subprocess.run(
                ["demucs", "--help"],
                capture_output=True,
                timeout=5,
            )
            if result.returncode == 0:
                return {"status": "healthy", "message": "Audio processor operational"}
            return {
                "status": "degraded",
                "message": "Demucs not responding properly",
            }
        except FileNotFoundError:
            return {"status": "unhealthy", "message": "Demucs not installed"}
        except Exception as e:
            return {"status": "unhealthy", "message": str(e)}


_audio_processor_instance: Optional[AudioProcessor] = None


def get_audio_processor() -> AudioProcessor:
    """Get singleton audio processor instance."""
    global _audio_processor_instance
    if _audio_processor_instance is None:
        _audio_processor_instance = AudioProcessor()
    return _audio_processor_instance


if __name__ == "__main__":
    print("Testing Audio Processor...")
    processor = get_audio_processor()
    print("✅ Audio Processor ready!")

def health_check(self) -> bool:
    try:
        import librosa
        import numpy as np
        import soundfile as sf
        return True
    except Exception:
        return False
    
def health_check(self) -> dict:
    """Returns health status of the audio processor."""
    try:
        return {"status": "healthy", "ready": True}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}