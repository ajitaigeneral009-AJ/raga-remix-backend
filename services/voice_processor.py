"""
Voice Processing Module
Handles pitch shifting, time stretching, and voice conversion
"""

import numpy as np
import librosa
import soundfile as sf
from typing import Tuple, Optional
from scipy.interpolate import interp1d
import logging

logger = logging.getLogger(__name__)

class VoiceProcessor:
    """
    Processes voice for different singers and pitch shifts
    """
    
    def __init__(self, sample_rate: int = 44100):
        self.sr = sample_rate
        self.logger = logger
    
    def pitch_shift(self, audio: np.ndarray, n_steps: int, sr: int = None) -> np.ndarray:
        """
        Shift pitch of audio by n_steps semitones
        
        Args:
            audio: Input audio signal
            n_steps: Number of semitones to shift (positive = higher, negative = lower)
            sr: Sample rate
        
        Returns:
            Pitch-shifted audio
        """
        if sr is None:
            sr = self.sr
        
        self.logger.info(f"Pitch shifting by {n_steps} semitones...")
        
        try:
            # Use librosa's pitch shifting
            shifted = librosa.effects.pitch_shift(audio, sr=sr, n_steps=n_steps)
            self.logger.info(f"✅ Pitch shifted successfully by {n_steps} semitones")
            return shifted
        except Exception as e:
            self.logger.error(f"Error in pitch shifting: {e}")
            return audio
    
    def time_stretch(self, audio: np.ndarray, rate: float, sr: int = None) -> np.ndarray:
        """
        Time stretch audio to match target tempo
        
        Args:
            audio: Input audio signal
            rate: Stretch rate (1.0 = no change, 1.2 = 20% faster, 0.8 = 20% slower)
            sr: Sample rate
        
        Returns:
            Time-stretched audio
        """
        if sr is None:
            sr = self.sr
        
        if abs(rate - 1.0) < 0.01:
            self.logger.info("No time stretching needed")
            return audio
        
        self.logger.info(f"Time stretching with rate {rate}...")
        
        try:
            stretched = librosa.effects.time_stretch(audio, rate=rate)
            self.logger.info(f"✅ Time stretched successfully (rate: {rate})")
            return stretched
        except Exception as e:
            self.logger.error(f"Error in time stretching: {e}")
            return audio
    
    def shift_to_match_original(self, 
                                new_audio: np.ndarray,
                                original_tempo: float,
                                original_key: str,
                                new_audio_tempo: float = None,
                                new_audio_key: str = None,
                                sr: int = None) -> np.ndarray:
        """
        Shift pitch and tempo of new audio to match original
        
        This is crucial for the Full Remix mode when adding different singer's voice
        
        Args:
            new_audio: New vocal performance (from different singer)
            original_tempo: Original song's tempo (BPM)
            original_key: Original song's key (e.g., "C", "D#")
            new_audio_tempo: New audio's detected tempo (optional, will detect if not provided)
            new_audio_key: New audio's detected key (optional, will detect if not provided)
            sr: Sample rate
        
        Returns:
            Adjusted audio matching original tempo and key
        """
        if sr is None:
            sr = self.sr
        
        self.logger.info(f"Matching new audio to original song...")
        self.logger.info(f"  Original: Tempo {original_tempo} BPM, Key {original_key}")
        
        # Auto-detect if not provided
        if new_audio_tempo is None or new_audio_key is None:
            self.logger.info("Detecting new audio properties...")
            from services.music_analyzer import MusicAnalyzer
            analyzer = MusicAnalyzer(sr=sr)
            analysis = analyzer.analyze_complete(new_audio)
            if new_audio_tempo is None:
                new_audio_tempo = analysis['tempo']
            if new_audio_key is None:
                new_audio_key = analysis['key']
        
        self.logger.info(f"  New audio: Tempo {new_audio_tempo} BPM, Key {new_audio_key}")
        
        # Calculate adjustments needed
        tempo_ratio = original_tempo / new_audio_tempo if new_audio_tempo > 0 else 1.0
        
        # Calculate semitone shift needed
        note_map = {'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5, 
                   'F#': 6, 'G': 7, 'G#': 8, 'A': 9, 'A#': 10, 'B': 11}
        
        original_semitone = note_map.get(original_key.replace('m', ''), 0)
        new_semitone = note_map.get(new_audio_key.replace('m', ''), 0)
        semitone_shift = original_semitone - new_semitone
        
        # Apply adjustments
        result = new_audio.copy()
        
        # 1. Time stretch first (to match tempo)
        if abs(tempo_ratio - 1.0) > 0.01:
            self.logger.info(f"Applying time stretch: {tempo_ratio:.2f}x")
            result = self.time_stretch(result, 1.0 / tempo_ratio, sr)
        
        # 2. Then pitch shift (to match key)
        if abs(semitone_shift) > 0.5:  # Only if shift > 0.5 semitones
            self.logger.info(f"Applying pitch shift: {semitone_shift:.0f} semitones")
            result = self.pitch_shift(result, int(round(semitone_shift)), sr)
        
        self.logger.info("✅ Audio matched to original song")
        return result
    
    def apply_vibrato(self, audio: np.ndarray, rate: float = 5.0, depth: float = 0.02) -> np.ndarray:
        """
        Apply vibrato effect to audio
        
        Args:
            audio: Input audio
            rate: Vibrato rate in Hz (typically 4-8 Hz)
            depth: Vibrato depth (0-1, typically 0.02-0.1)
        
        Returns:
            Audio with vibrato
        """
        self.logger.info(f"Applying vibrato: {rate}Hz, depth {depth}")
        
        t = np.arange(len(audio)) / self.sr
        lfo = depth * np.sin(2 * np.pi * rate * t)
        
        # Use phase vocoder for natural vibrato
        result = librosa.effects.pitch_shift(audio, sr=self.sr, n_steps=lfo)
        
        return result
    
    def apply_formant_shift(self, audio: np.ndarray, formant_shift: float = 1.0) -> np.ndarray:
        """
        Apply formant shifting (makes voice sound different without changing pitch much)
        
        Args:
            audio: Input audio
            formant_shift: How much to shift formant (1.0 = no change, 1.2 = higher, 0.8 = lower)
        
        Returns:
            Audio with shifted formant
        """
        self.logger.info(f"Applying formant shift: {formant_shift}")
        
        # Simple formant shift using spectral modification
        if abs(formant_shift - 1.0) < 0.01:
            return audio
        
        # Extract spectrogram
        D = librosa.stft(audio)
        magnitude, phase = np.abs(D), np.angle(D)
        
        # Stretch magnitude spectrum
        new_magnitude = np.zeros_like(magnitude)
        for i in range(magnitude.shape[0]):
            new_i = int(i * formant_shift)
            if new_i < magnitude.shape[0]:
                new_magnitude[new_i] = magnitude[i]
        
        # Reconstruct
        D_modified = new_magnitude * np.exp(1j * phase)
        result = librosa.istft(D_modified)
        
        return result
    
    def normalize_loudness(self, audio: np.ndarray, target_loudness: float = -20.0) -> np.ndarray:
        """
        Normalize audio loudness
        
        Args:
            audio: Input audio
            target_loudness: Target loudness in LUFS (typically -20 to -14)
        
        Returns:
            Normalized audio
        """
        self.logger.info(f"Normalizing loudness to {target_loudness} LUFS...")
        
        # Simple loudness calculation
        rms = np.sqrt(np.mean(audio ** 2))
        if rms == 0:
            return audio
        
        # Convert RMS to dB
        current_loudness = 20 * np.log10(rms)
        adjustment = target_loudness - current_loudness
        gain = 10 ** (adjustment / 20)
        
        result = audio * gain
        
        # Prevent clipping
        if np.max(np.abs(result)) > 0.99:
            result = result / np.max(np.abs(result))
        
        self.logger.info(f"✅ Normalized: {current_loudness:.1f}dB → {target_loudness}dB")
        return result
    
    def blend_vocals(self, vocal1: np.ndarray, vocal2: np.ndarray, ratio: float = 0.5) -> np.ndarray:
        """
        Blend two vocal tracks
        
        Args:
            vocal1: First vocal track
            vocal2: Second vocal track
            ratio: Mix ratio (0.0 = all vocal1, 1.0 = all vocal2, 0.5 = equal)
        
        Returns:
            Blended audio
        """
        # Make same length
        min_len = min(len(vocal1), len(vocal2))
        vocal1 = vocal1[:min_len]
        vocal2 = vocal2[:min_len]
        
        blended = (1 - ratio) * vocal1 + ratio * vocal2
        
        return blended
    
    def save_audio(self, audio: np.ndarray, filepath: str, sr: int = None) -> bool:
        """
        Save audio to file
        
        Args:
            audio: Audio signal
            filepath: Output file path
            sr: Sample rate
        
        Returns:
            Success status
        """
        if sr is None:
            sr = self.sr
        
        try:
            sf.write(filepath, audio, sr)
            self.logger.info(f"✅ Audio saved: {filepath}")
            return True
        except Exception as e:
            self.logger.error(f"Error saving audio: {e}")
            return False