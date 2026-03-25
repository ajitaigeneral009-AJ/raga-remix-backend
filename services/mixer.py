"""
Professional mixing engine - EQ, compression, reverb, balance
"""

import numpy as np
from typing import Dict
import logging
from scipy import signal

logger = logging.getLogger(__name__)

class MixingEngine:
    """
    Mix instruments with EQ, compression, effects
    """
    
    def __init__(self, sr: int = 44100):
        self.sr = sr
    
    def apply_eq(self, audio: np.ndarray, eq_preset: Dict) -> np.ndarray:
        """
        Apply EQ to audio
        
        Args:
            audio: Input audio
            eq_preset: Dict with filter specs {'low_cut': (freq, db), 'high_shelf': ...}
        """
        result = audio.copy()
        
        # Low cut
        if 'low_cut' in eq_preset:
            freq, db = eq_preset['low_cut']
            if db < 0:  # Cutting
                sos = signal.butter(2, freq, 'hp', fs=self.sr, output='sos')
                result = signal.sosfilt(sos, result)
        
        # High cut
        if 'high_cut' in eq_preset:
            freq, db = eq_preset['high_cut']
            if db < 0:
                sos = signal.butter(2, freq, 'lp', fs=self.sr, output='sos')
                result = signal.sosfilt(sos, result)
        
        # Presence peak (simplified - using bandpass)
        if 'presence' in eq_preset:
            freq, db = eq_preset['presence']
            if db > 0:
                # Boost around presence frequency
                result = self._apply_peaking_eq(result, freq, db, 2.0)
        
        return result
    
    def _apply_peaking_eq(self, audio: np.ndarray, freq: float, gain_db: float,
                         q_factor: float) -> np.ndarray:
        """
        Apply peaking EQ filter
        """
        # Convert gain to linear
        gain_linear = 10 ** (gain_db / 20.0)
        
        # Design peaking filter
        w0 = 2 * np.pi * freq / self.sr
        alpha = np.sin(w0) / (2 * q_factor)
        
        b0 = 1 + alpha * gain_linear
        b1 = -2 * np.cos(w0)
        b2 = 1 - alpha * gain_linear
        a0 = 1 + alpha / gain_linear
        a1 = -2 * np.cos(w0)
        a2 = 1 - alpha / gain_linear
        
        # Normalize
        b = [b0 / a0, b1 / a0, b2 / a0]
        a = [1, a1 / a0, a2 / a0]
        
        return signal.lfilter(b, a, audio)
    
    def apply_compression(self, audio: np.ndarray, threshold: float = -20,
                         ratio: float = 4, attack_ms: float = 5,
                         release_ms: float = 100) -> np.ndarray:
        """
        Apply dynamic range compression
        """
        attack_samples = int(attack_ms * self.sr / 1000)
        release_samples = int(release_ms * self.sr / 1000)
        
        # Calculate envelope
        threshold_linear = 10 ** (threshold / 20.0)
        
        # Simple level detector
        envelope = np.abs(audio)
        
        # Smooth envelope
        envelope_smooth = np.zeros_like(envelope)
        for i in range(len(envelope)):
            if i == 0:
                envelope_smooth[i] = envelope[i]
            else:
                if envelope[i] > envelope_smooth[i-1]:
                    # Attack
                    alpha = 2.0 / (attack_samples + 1)
                else:
                    # Release
                    alpha = 2.0 / (release_samples + 1)
                
                envelope_smooth[i] = alpha * envelope[i] + (1 - alpha) * envelope_smooth[i-1]
        
        # Calculate gain reduction
        gain_reduction = np.ones_like(envelope_smooth)
        mask = envelope_smooth > threshold_linear
        gain_reduction[mask] = (threshold_linear + (envelope_smooth[mask] - threshold_linear) / ratio) / envelope_smooth[mask]
        
        return audio * gain_reduction
    
    def apply_reverb(self, audio: np.ndarray, room_size: float = 0.7,
                    wet_amount: float = 0.3) -> np.ndarray:
        """
        Apply simple reverb using comb filters
        """
        # Simple reverb using parallel comb filters
        delays = [0.0297, 0.0371, 0.0411, 0.0437]  # Milliseconds in seconds
        decay_factor = 0.84
        
        reverb_output = np.zeros_like(audio)
        
        for delay_time in delays:
            delay_samples = int(delay_time * self.sr)
            
            if delay_samples < len(audio):
                # Comb filter with feedback
                delayed = np.zeros_like(audio)
                for i in range(delay_samples, len(audio)):
                    delayed[i] = audio[i] + decay_factor * delayed[i - delay_samples]
                
                reverb_output += delayed
        
        # Mix wet and dry
        reverb_output = reverb_output / len(delays)  # Average
        result = (1 - wet_amount) * audio + wet_amount * reverb_output
        
        return result
    
    def mix_stems(self, stems: Dict[str, np.ndarray], mixing_config: Dict) -> np.ndarray:
        """
        Mix multiple stems together
        
        Args:
            stems: Dict of {instrument_name: audio_array}
            mixing_config: {instrument_name: {level_db, eq_preset, effects}}
        """
        mixed = np.zeros_like(next(iter(stems.values())))
        
        for instrument_name, stem_audio in stems.items():
            config = mixing_config.get(instrument_name, {})
            
            # Get level
            level_db = config.get('level_db', 0)
            level_linear = 10 ** (level_db / 20.0)
            
            # Apply EQ if configured
            processed = stem_audio.copy()
            if 'eq_preset' in config:
                processed = self.apply_eq(processed, config['eq_preset'])
            
            # Apply compression if configured
            if 'compression' in config:
                comp_config = config['compression']
                processed = self.apply_compression(processed, **comp_config)
            
            # Apply effects if configured
            if 'reverb' in config:
                rev_amount = config['reverb']
                processed = self.apply_reverb(processed, wet_amount=rev_amount)
            
            # Mix to output
            mixed += processed * level_linear
        
        logger.info(f"Mixed {len(stems)} stems")
        return mixed
    
    def normalize_loudness(self, audio: np.ndarray, target_lufs: float = -14.0) -> np.ndarray:
        """
        Normalize audio to target LUFS (Loudness Units)
        """
        # Simplified LUFS calculation (proper LUFS requires K-weighting)
        rms = np.sqrt(np.mean(audio ** 2))
        current_lufs = 20 * np.log10(rms) if rms > 0 else -np.inf
        
        loudness_diff = target_lufs - current_lufs
        gain = 10 ** (loudness_diff / 20.0)
        
        normalized = audio * gain
        
        # Prevent clipping
        peak = np.max(np.abs(normalized))
        if peak > 1.0:
            normalized = normalized / peak
        
        logger.info(f"Normalized audio from {current_lufs:.1f} to {target_lufs:.1f} LUFS")
        return normalized