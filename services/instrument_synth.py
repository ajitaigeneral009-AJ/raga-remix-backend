"""
Raga-Aware Instrument Synthesizer for AI Cover Studio

VERSION 4.0 - Professional synthesis of Tabla, Sitar, and Guitar
Respects Raga characteristics, notes, and musical traditions
"""

import numpy as np
import logging
from typing import List, Optional

logger = logging.getLogger(__name__)

# =========================================================================
# RAGA DATABASE - Notes and Characteristics
# =========================================================================

RAGA_DATABASE = {
    "yaman": {
        "name": "Yaman",
        "notes": [0, 2, 4, 6, 7, 9, 11],  # Sa Re Ga Ma Pa Dha Ni (C scale)
        "mood": "Peaceful, devotional",
        "time": "Evening (6-9 PM)",
        "character": "Serene and uplifting",
        "characteristic_notes": [6, 7, 9],  # Ma, Pa, Dha
        "resting_notes": [0, 7],  # Sa, Pa
    },
    "bhairav": {
        "name": "Bhairav",
        "notes": [0, 1, 4, 5, 7, 8, 11],
        "mood": "Serious, reverent",
        "time": "Morning (4-7 AM)",
        "character": "Solemn and majestic",
        "characteristic_notes": [1, 5, 8],
        "resting_notes": [0, 5],
    },
    "khamaaj": {
        "name": "Khamaaj",
        "notes": [0, 2, 4, 5, 7, 9, 10],
        "mood": "Gentle, soothing",
        "time": "Afternoon (12-3 PM)",
        "character": "Soft and melodic",
        "characteristic_notes": [5, 10],
        "resting_notes": [0, 7],
    },
    "ahir_bhairav": {
        "name": "Ahir Bhairav",
        "notes": [0, 1, 4, 5, 7, 8, 11],
        "mood": "Melancholic, contemplative",
        "time": "Late night (10 PM-2 AM)",
        "character": "Introspective and thoughtful",
        "characteristic_notes": [1, 8],
        "resting_notes": [0, 5],
    },
    "marwa": {
        "name": "Marwa",
        "notes": [0, 1, 4, 6, 7, 9, 11],
        "mood": "Energetic, uplifting",
        "time": "Evening (6-9 PM)",
        "character": "Bright and vibrant",
        "characteristic_notes": [1, 6, 9],
        "resting_notes": [0, 7],
    },
    "todi": {
        "name": "Todi",
        "notes": [0, 1, 3, 5, 7, 8, 10],
        "mood": "Pathos, separation",
        "time": "Night (9 PM-12 AM)",
        "character": "Emotional and expressive",
        "characteristic_notes": [1, 3, 8],
        "resting_notes": [0, 5],
    },
}

# =========================================================================
# RAGA INSTRUMENT SYNTHESIZER
# =========================================================================


class RagaInstrumentSynthesizer:
    """Professional synthesizer for Raga-aware instruments."""

    def __init__(self, raga_db_path: Optional[str] = None):
        """Initialize synthesizer with Raga database."""
        self.raga_db = RAGA_DATABASE
        logger.info(
            f"✅ RagaInstrumentSynthesizer initialized with {len(self.raga_db)} ragas"
        )

    # ------------------------ helpers ------------------------

    def get_raga_notes(self, raga_name: str) -> List[int]:
        """Get MIDI note offsets for a Raga."""
        raga = self.raga_db.get(raga_name.lower())
        if not raga:
            logger.warning(f"⚠️ Raga '{raga_name}' not found, using Yaman")
            raga = self.raga_db["yaman"]
        return raga["notes"]

    # ------------------------ Tabla --------------------------

    def synthesize_tabla(
        self, raga_name: str, duration: float, tempo_bpm: float, sr: int
    ) -> np.ndarray:
        """
        Synthesize Tabla rhythm respecting Raga characteristics.
        Tabla provides the rhythmic foundation.
        """
        num_samples = int(duration * sr)
        tabla = np.zeros(num_samples, dtype=np.float32)

        beat_duration = (60.0 / tempo_bpm) * sr  # samples per beat

        bass_freq = 80.0   # low thoom
        treble_freq = 150.0  # high tak

        logger.info(f"🥁 Tabla: {raga_name} at {tempo_bpm} BPM")

        # Simple 8‑beat Keherwa pattern
        beat_pattern = [1.0, 0.0, 0.5, 0.0, 1.0, 0.0, 0.7, 0.0]
        pattern_length = len(beat_pattern)

        beat_idx = 0
        pattern_idx = 0

        while beat_idx * beat_duration < num_samples:
            beat_start = int(beat_idx * beat_duration)
            beat_end = int((beat_idx + 0.5) * beat_duration)
            if beat_end > num_samples:
                beat_end = num_samples

            amplitude = beat_pattern[pattern_idx % pattern_length]
            if amplitude > 0:
                freq = bass_freq if amplitude > 0.7 else treble_freq
                t = np.arange(beat_end - beat_start) / sr
                tabla[beat_start:beat_end] += (
                    amplitude * 0.6 * np.sin(2 * np.pi * freq * t)
                ).astype(np.float32)

            beat_idx += 1
            pattern_idx += 1

        max_val = float(np.max(np.abs(tabla)))
        if max_val > 0:
            tabla /= max_val * 1.01

        return tabla

    # ------------------------ Sitar --------------------------

    def synthesize_sitar(
        self,
        raga_name: str,
        duration: float,
        tempo_bpm: float,
        energy_level: float,
        sr: int,
    ) -> np.ndarray:
        """
        Synthesize Sitar melody using ONLY Raga notes.
        """
        num_samples = int(duration * sr)
        sitar = np.zeros(num_samples, dtype=np.float32)

        raga_notes = self.get_raga_notes(raga_name)
        raga_data = self.raga_db.get(raga_name.lower(), self.raga_db["yaman"])

        sa_freq = 262.0  # C4

        logger.info(f"🎸 Sitar: {raga_name} with {len(raga_notes)} notes")

        note_duration = (60.0 / tempo_bpm) * sr * 2.0  # 2 beats per note
        phrase = raga_data.get("characteristic_notes", raga_notes[:3])
        phrase_idx = 0
        current_sample = 0

        while current_sample < num_samples:
            note_offset = phrase[phrase_idx % len(phrase)]
            freq = sa_freq * (2.0 ** (note_offset / 12.0))

            note_dur = min(note_duration, num_samples - current_sample)
            note_len = int(note_dur)

            t = np.arange(note_len) / sr

            vibrato_freq = 5.0
            vibrato_depth = 0.02
            vibrato = 1.0 + vibrato_depth * np.sin(2 * np.pi * vibrato_freq * t)

            note = 0.6 * energy_level * np.sin(2 * np.pi * freq * vibrato * t)

            env_samples = int(0.05 * sr)
            if env_samples < note_len:
                env = np.ones(note_len, dtype=np.float32)
                env[:env_samples] = np.linspace(0.0, 1.0, env_samples)
                env[-env_samples:] = np.linspace(1.0, 0.0, env_samples)
                note *= env

            note = note.astype(np.float32)

            end = current_sample + note_len
            sitar[current_sample:end] += note
            current_sample = end
            phrase_idx += 1

        max_val = float(np.max(np.abs(sitar)))
        if max_val > 0:
            sitar /= max_val * 1.01

        return sitar

    # ------------------------ Guitar -------------------------

    def synthesize_guitar(
        self, raga_name: str, duration: float, tempo_bpm: float, sr: int
    ) -> np.ndarray:
        """
        Synthesize Guitar harmonic accompaniment respecting Raga intervals.
        """
        num_samples = int(duration * sr)
        guitar = np.zeros(num_samples, dtype=np.float32)

        raga_data = self.raga_db.get(raga_name.lower(), self.raga_db["yaman"])
        resting_notes = raga_data.get("resting_notes", [0, 7])

        sa_freq = 262.0
        logger.info(f"🎵 Guitar: {raga_name} harmony")

        chord_duration = (60.0 / tempo_bpm) * sr * 4.0  # 4 beats per chord
        chord_idx = 0
        current_sample = 0

        while current_sample < num_samples:
            primary = resting_notes[chord_idx % len(resting_notes)]
            secondary = resting_notes[(chord_idx + 1) % len(resting_notes)]

            freq1 = sa_freq * (2.0 ** (primary / 12.0))
            freq2 = sa_freq * (2.0 ** (secondary / 12.0))

            dur = min(chord_duration, num_samples - current_sample)
            dur_int = int(dur)

            t = np.arange(dur_int) / sr
            chord = 0.3 * (
                np.sin(2 * np.pi * freq1 * t) + np.sin(2 * np.pi * freq2 * t)
            )

            env_samples = int(0.05 * sr)
            if env_samples < dur_int:
                env = np.ones(dur_int, dtype=np.float32)
                env[:env_samples] = np.linspace(0.0, 1.0, env_samples)
                env[-env_samples:] = np.linspace(1.0, 0.2, env_samples)
                chord *= env

            chord = chord.astype(np.float32)

            end = current_sample + dur_int
            guitar[current_sample:end] += chord
            current_sample = end
            chord_idx += 1

        max_val = float(np.max(np.abs(guitar)))
        if max_val > 0:
            guitar /= max_val * 1.01

        return guitar

    # ------------------ Generic synth for main.py ------------

    def synthesize(
        self,
        instrument_name: str,
        raga_name: str,
        num_samples: int,
        sr: int,
        tempo_bpm: float,
        energy_level: float,
    ) -> np.ndarray:
        """
        Generic synth method expected by main.py.

        Parameters:
          instrument_name: e.g. "Tabla", "Sitar", "Guitar"
          raga_name: e.g. "yaman"
          num_samples: section length in samples
          sr: sample rate
          tempo_bpm: tempo for this section
          energy_level: dynamics (0–1)
        """
        duration_sec = num_samples / float(sr)
        name = instrument_name.strip().lower()

        if name in {"tabla", "drums", "percussion"}:
            audio = self.synthesize_tabla(raga_name, duration_sec, tempo_bpm, sr)
        elif name in {"sitar", "lead_sitar", "melody", "lead"}:
            audio = self.synthesize_sitar(
                raga_name, duration_sec, tempo_bpm, energy_level, sr
            )
        elif name in {
            "guitar",
            "rhythm_guitar",
            "acoustic_guitar",
            "electric_guitar",
            "harmony",
        }:
            audio = self.synthesize_guitar(raga_name, duration_sec, tempo_bpm, sr)
        else:
            logger.warning(
                f"⚠️ Instrument '{instrument_name}' not recognized for synthesis; "
                f"using sitar engine as fallback."
            )
            audio = self.synthesize_sitar(
                raga_name, duration_sec, tempo_bpm, energy_level, sr
            )

        # Ensure exact length
        if len(audio) < num_samples:
            pad = np.zeros(num_samples - len(audio), dtype=audio.dtype)
            audio = np.concatenate([audio, pad])
        elif len(audio) > num_samples:
            audio = audio[:num_samples]

        return audio.astype(np.float32)

    # ---------------------- Mixer helper ---------------------

    def combine_instruments(
        self,
        tabla: Optional[np.ndarray] = None,
        sitar: Optional[np.ndarray] = None,
        guitar: Optional[np.ndarray] = None,
        tabla_volume: float = 0.5,
        sitar_volume: float = 0.7,
        guitar_volume: float = 0.6,
    ) -> np.ndarray:
        """Professionally mix instruments with volume control."""
        parts = []
        if tabla is not None:
            parts.append(tabla * tabla_volume)
        if sitar is not None:
            parts.append(sitar * sitar_volume)
        if guitar is not None:
            parts.append(guitar * guitar_volume)

        if not parts:
            return np.array([], dtype=np.float32)

        mixed = np.sum(parts, axis=0)
        max_val = float(np.max(np.abs(mixed)))
        if max_val > 1.0:
            mixed /= max_val * 1.01

        logger.info("✅ Instruments mixed successfully")
        return mixed.astype(np.float32)


# =========================================================================
# STANDALONE FUNCTIONS FOR BACKWARD COMPATIBILITY
# =========================================================================


def synthesize_tabla(
    raga_name: str, duration: float, tempo_bpm: float, sr: int
) -> np.ndarray:
    """Standalone function for Tabla synthesis."""
    synth = RagaInstrumentSynthesizer()
    return synth.synthesize_tabla(raga_name, duration, tempo_bpm, sr)


def synthesize_sitar(
    raga_name: str, duration: float, tempo_bpm: float, energy_level: float, sr: int
) -> np.ndarray:
    """Standalone function for Sitar synthesis."""
    synth = RagaInstrumentSynthesizer()
    return synth.synthesize_sitar(raga_name, duration, tempo_bpm, energy_level, sr)


def synthesize_guitar(
    raga_name: str, duration: float, tempo_bpm: float, sr: int
) -> np.ndarray:
    """Standalone function for Guitar synthesis."""
    synth = RagaInstrumentSynthesizer()
    return synth.synthesize_guitar(raga_name, duration, tempo_bpm, sr)
