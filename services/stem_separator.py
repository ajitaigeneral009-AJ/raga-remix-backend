"""
Stem Separator Service - Separates vocals from instrumentals using AI models
"""

import subprocess
import shlex
from pathlib import Path
from typing import Dict, Tuple, Optional
import logging
import numpy as np
import soundfile as sf

logger = logging.getLogger(__name__)

class StemSeparator:
    """Separates audio stems (vocals, drums, bass, other) from mixed audio"""

    def __init__(self, model_name: str = "demucs"):
        """
        Initialize stem separator.
        Args:
            model_name: Model to use for separation (demucs, spleeter, etc.)
        """
        self.model_name = model_name
        self.name = "StemSeparator"
        self.output_dir = "demucs_outputs"
        self.last_input_path: Optional[Path] = None

        if model_name == "demucs":
            logger.info("✅ Demucs (CLI) will be used for separation")
        else:
            logger.warning(f"Model {model_name} not configured, using basic separation")

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def separate_vocals(
        self, audio: np.ndarray, sr: int = 44100
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Separate vocals from instrumental.
        Args:
            audio: Input audio (mono or stereo)
            sr: Sample rate
        Returns:
            Tuple of (vocals, instrumental_dummy)
        """
        try:
            if self.model_name == "demucs":
                return self._separate_demucs(audio, sr)
            else:
                return self._separate_basic(audio, sr)
        except Exception as e:
            logger.error(f"Separation failed: {e}, using fallback")
            return self._separate_basic(audio, sr)

    def separate_two_stems(
        self, audio: np.ndarray, sr: int = 44100
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Get both stems using Demucs CLI two-stems=vocals.
        Returns:
            (vocals, no_vocals_instrumental)
        """
        if self.model_name != "demucs":
            return self._separate_basic(audio, sr)

        if not self.last_input_path:
            raise RuntimeError(
                "last_input_path not set on StemSeparator; "
                "set separator.last_input_path = Path(input_audio_file)"
            )

        vocals_file, no_vocals_file = self._demucs_cli_two_stems(
            str(self.last_input_path)
        )

        vocals, _ = sf.read(str(vocals_file))
        if vocals.ndim > 1:
            vocals = vocals.mean(axis=1)

        instrumental, _ = sf.read(str(no_vocals_file))
        if instrumental.ndim > 1:
            instrumental = instrumental.mean(axis=1)

        return vocals.astype(np.float32), instrumental.astype(np.float32)

    def separate_to_file(self, input_audio_path: str) -> str:
        """
        Separate audio and save stems to files.
        Args:
            input_audio_path: Path to input audio file
        Returns:
            Path to output directory containing stems
        """
        if self.model_name != "demucs":
            raise RuntimeError("separate_to_file only works with demucs model")

        input_path = Path(input_audio_path)
        self.last_input_path = input_path

        try:
            vocals_file, instrumental_file = self._demucs_cli_two_stems(
                str(input_path)
            )
            logger.info(f"✅ Separation complete: vocals={vocals_file}, instrumental={instrumental_file}")
            return str(Path(self.output_dir) / "htdemucs")
        except Exception as e:
            logger.error(f"Separation failed: {e}")
            raise

    # ------------------------------------------------------------------
    # Demucs CLI implementation
    # ------------------------------------------------------------------

    def _demucs_cli_two_stems(
        self, input_path: str, output_root: str = "demucs_outputs"
    ) -> Tuple[Path, Path]:
        """
        Call Demucs CLI with two-stems=vocals on input_path.
        Returns:
            (vocals_path, no_vocals_path)
        """
        input_path = Path(input_path)
        output_root = Path(output_root)
        output_root.mkdir(parents=True, exist_ok=True)

        cmd = f'demucs --two-stems=vocals -n htdemucs -o "{output_root}" "{input_path}"'
        logger.info(f"Running Demucs CLI: {cmd}")

        try:
            subprocess.check_call(shlex.split(cmd))
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Demucs CLI failed with code {e.returncode}") from e

        model_dir = output_root / "htdemucs"
        if not model_dir.exists():
            raise RuntimeError(f"Demucs output directory not found: {model_dir}")

        track_dirs = [p for p in model_dir.iterdir() if p.is_dir()]
        if not track_dirs:
            raise RuntimeError("Demucs CLI did not create any track directory.")

        track_dir = track_dirs[0]

        vocals_file: Optional[Path] = None
        no_vocals_file: Optional[Path] = None

        for p in track_dir.iterdir():
            name = p.stem.lower()
            if "vocals" in name and "no" not in name:
                vocals_file = p
            elif "no_vocals" in name or "no-vocals" in name or "accompaniment" in name:
                no_vocals_file = p

        if vocals_file is None or no_vocals_file is None:
            raise RuntimeError(
                f"Could not find both vocals and no_vocals stems in {track_dir}"
            )

        return vocals_file, no_vocals_file

    def _separate_demucs(
        self, audio: np.ndarray, sr: int = 44100
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Separate using Demucs CLI and return vocals only.
        Expects that the original mixed file path is stored in
        self.last_input_path by the caller.
        """
        try:
            if not self.last_input_path:
                raise RuntimeError(
                    "last_input_path not set on StemSeparator; "
                    "set separator.last_input_path = Path(input_audio_file)"
                )

            vocals_file, _ = self._demucs_cli_two_stems(str(self.last_input_path))

            # Load vocals from Demucs
            vocals, _ = sf.read(str(vocals_file))
            if vocals.ndim > 1:
                vocals = vocals.mean(axis=1)

            instrumental_dummy = np.zeros_like(vocals, dtype=np.float32)

            return vocals.astype(np.float32), instrumental_dummy

        except Exception as e:
            logger.warning(f"Demucs CLI separation failed: {e}, using fallback")
            return self._separate_basic(audio, sr)

    # ------------------------------------------------------------------
    # Basic / fallback separation
    # ------------------------------------------------------------------

    def _separate_basic(
        self, audio: np.ndarray, sr: int
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Very simple fallback separation (not high quality)."""
        if audio.ndim == 1:
            mono_audio = audio
        else:
            mono_audio = audio.mean(axis=0)

        vocals = mono_audio.copy() * 0.4
        instrumental = mono_audio.copy() * 0.6

        return vocals.astype(np.float32), instrumental.astype(np.float32)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def quality_check(self, vocals: np.ndarray, instrumental: np.ndarray) -> Dict:
        """Check quality of separation."""
        return {
            "vocal_energy": float(np.mean(np.abs(vocals))),
            "instrumental_energy": float(np.mean(np.abs(instrumental))),
            "separation_quality": (
                "good"
                if np.std(vocals) > np.std(instrumental) * 0.5
                else "fair"
            ),
            "estimated_snr": float(
                np.max(np.abs(vocals)) / (np.max(np.abs(instrumental)) + 1e-6)
            ),
        }

    def create_vocal_track(
        self, audio: np.ndarray, output_path: str = None
    ) -> Tuple[np.ndarray, Optional[str]]:
        """
        Create vocal-only track.
        Useful for Mode 1: Remove Instruments.
        """
        vocals, _ = self.separate_vocals(audio)

        if output_path:
            sf.write(output_path, vocals, 44100)
            logger.info(f"✅ Vocal track saved: {output_path}")

        return vocals, output_path
