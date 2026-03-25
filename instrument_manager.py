"""
🎵 Advanced Instrument Manager for Raga Remix Studio
Handles 30+ instruments with synthesis, compatibility, and dynamic generation
"""

import numpy as np
import logging
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class InstrumentProfile:
    """Instrument synthesis profile"""
    name: str
    category: str
    frequency_range: Tuple[float, float]
    characteristic_timbre: str
    attack_time: float
    decay_time: float
    sustain_level: float
    release_time: float
    vibrato_rate: float
    vibrato_depth: float
    harmonic_content: List[float]
    dynamic_range: float


class InstrumentManager:
    """Manages synthesis, compatibility, and generation of all instruments"""
    
    def __init__(self):
        """Initialize instrument profiles and compatibility matrix"""
        self.profiles = self._initialize_profiles()
        self.compatibility = self._calculate_compatibility()
        logger.info(f"✅ InstrumentManager initialized with {len(self.profiles)} instruments")
    
    def _initialize_profiles(self) -> Dict[str, InstrumentProfile]:
        """Initialize profiles for all 30+ instruments"""
        return {
            # Indian Classical Instruments (12)
            "sitar": InstrumentProfile(
                name="Sitar", category="Indian Classical String",
                frequency_range=(100, 5000), characteristic_timbre="Bright, resonant",
                attack_time=0.05, decay_time=0.1, sustain_level=0.8, release_time=0.2,
                vibrato_rate=5, vibrato_depth=0.05,
                harmonic_content=[1.0, 0.6, 0.4, 0.3, 0.2],
                dynamic_range=0.8
            ),
            "sarangi": InstrumentProfile(
                name="Sarangi", category="Indian Classical String",
                frequency_range=(80, 4000), characteristic_timbre="Warm, vocal-like",
                attack_time=0.1, decay_time=0.15, sustain_level=0.85, release_time=0.3,
                vibrato_rate=4, vibrato_depth=0.08,
                harmonic_content=[1.0, 0.7, 0.5, 0.4, 0.3, 0.2],
                dynamic_range=0.75
            ),
            "bansuri": InstrumentProfile(
                name="Bansuri", category="Indian Classical Wind",
                frequency_range=(300, 4500), characteristic_timbre="Mellow, sweet",
                attack_time=0.08, decay_time=0.05, sustain_level=0.9, release_time=0.15,
                vibrato_rate=6, vibrato_depth=0.06,
                harmonic_content=[1.0, 0.3, 0.2, 0.1],
                dynamic_range=0.7
            ),
            "tabla": InstrumentProfile(
                name="Tabla", category="Indian Classical Percussion",
                frequency_range=(50, 3000), characteristic_timbre="Punchy, rhythmic",
                attack_time=0.01, decay_time=0.1, sustain_level=0.3, release_time=0.15,
                vibrato_rate=0, vibrato_depth=0,
                harmonic_content=[1.0, 0.8, 0.6, 0.4, 0.3],
                dynamic_range=0.95
            ),
            "mridangam": InstrumentProfile(
                name="Mridangam", category="Indian Classical Percussion",
                frequency_range=(60, 2800), characteristic_timbre="Deep, resonant",
                attack_time=0.01, decay_time=0.12, sustain_level=0.4, release_time=0.2,
                vibrato_rate=0, vibrato_depth=0,
                harmonic_content=[1.0, 0.7, 0.5, 0.3],
                dynamic_range=0.9
            ),
            "harmonium": InstrumentProfile(
                name="Harmonium", category="Indian Classical Keyboard",
                frequency_range=(50, 4000), characteristic_timbre="Steady, full",
                attack_time=0.05, decay_time=0, sustain_level=1.0, release_time=0.1,
                vibrato_rate=0, vibrato_depth=0,
                harmonic_content=[1.0, 0.4, 0.2],
                dynamic_range=0.5
            ),
            "veena": InstrumentProfile(
                name="Veena", category="Indian Classical String",
                frequency_range=(70, 3500), characteristic_timbre="Rich, mellow",
                attack_time=0.08, decay_time=0.12, sustain_level=0.85, release_time=0.25,
                vibrato_rate=3, vibrato_depth=0.04,
                harmonic_content=[1.0, 0.5, 0.3, 0.2],
                dynamic_range=0.7
            ),
            "shehnai": InstrumentProfile(
                name="Shehnai", category="Indian Classical Wind",
                frequency_range=(250, 3000), characteristic_timbre="Bright, festive",
                attack_time=0.06, decay_time=0.08, sustain_level=0.85, release_time=0.15,
                vibrato_rate=5, vibrato_depth=0.08,
                harmonic_content=[1.0, 0.5, 0.3, 0.2],
                dynamic_range=0.8
            ),
            "sarod": InstrumentProfile(
                name="Sarod", category="Indian Classical String",
                frequency_range=(70, 4500), characteristic_timbre="Warm, deep",
                attack_time=0.07, decay_time=0.1, sustain_level=0.8, release_time=0.22,
                vibrato_rate=4, vibrato_depth=0.06,
                harmonic_content=[1.0, 0.6, 0.4, 0.3, 0.2],
                dynamic_range=0.75
            ),
            "flute": InstrumentProfile(
                name="Indian Flute", category="Indian Classical Wind",
                frequency_range=(260, 3500), characteristic_timbre="Pure, lyrical",
                attack_time=0.07, decay_time=0.06, sustain_level=0.9, release_time=0.12,
                vibrato_rate=5, vibrato_depth=0.05,
                harmonic_content=[1.0, 0.2, 0.1],
                dynamic_range=0.65
            ),
            "gong": InstrumentProfile(
                name="Gong", category="Indian Classical Percussion",
                frequency_range=(30, 5000), characteristic_timbre="Resonant, shimmering",
                attack_time=0.02, decay_time=0.3, sustain_level=0.5, release_time=0.5,
                vibrato_rate=0, vibrato_depth=0,
                harmonic_content=[1.0, 0.6, 0.4, 0.3, 0.2, 0.1],
                dynamic_range=0.85
            ),
            
            # Western String Instruments (8)
            "guitar": InstrumentProfile(
                name="Guitar", category="Western String",
                frequency_range=(80, 4000), characteristic_timbre="Warm, woody",
                attack_time=0.02, decay_time=0.15, sustain_level=0.7, release_time=0.25,
                vibrato_rate=4, vibrato_depth=0.04,
                harmonic_content=[1.0, 0.5, 0.3, 0.2],
                dynamic_range=0.8
            ),
            "electric_guitar": InstrumentProfile(
                name="Electric Guitar", category="Western String",
                frequency_range=(80, 5000), characteristic_timbre="Bright, punchy",
                attack_time=0.01, decay_time=0.1, sustain_level=0.8, release_time=0.2,
                vibrato_rate=5, vibrato_depth=0.06,
                harmonic_content=[1.0, 0.7, 0.5, 0.3, 0.2],
                dynamic_range=0.85
            ),
            "violin": InstrumentProfile(
                name="Violin", category="Western String",
                frequency_range=(196, 4000), characteristic_timbre="Warm, expressive",
                attack_time=0.08, decay_time=0.1, sustain_level=0.95, release_time=0.15,
                vibrato_rate=6, vibrato_depth=0.08,
                harmonic_content=[1.0, 0.6, 0.4, 0.3, 0.2],
                dynamic_range=0.9
            ),
            "cello": InstrumentProfile(
                name="Cello", category="Western String",
                frequency_range=(65, 3000), characteristic_timbre="Deep, warm",
                attack_time=0.1, decay_time=0.12, sustain_level=0.9, release_time=0.2,
                vibrato_rate=4, vibrato_depth=0.06,
                harmonic_content=[1.0, 0.7, 0.5, 0.3],
                dynamic_range=0.85
            ),
            "bass": InstrumentProfile(
                name="Bass", category="Western String",
                frequency_range=(40, 1500), characteristic_timbre="Deep, punchy",
                attack_time=0.05, decay_time=0.2, sustain_level=0.75, release_time=0.3,
                vibrato_rate=2, vibrato_depth=0.04,
                harmonic_content=[1.0, 0.6, 0.3],
                dynamic_range=0.8
            ),
            "mandolin": InstrumentProfile(
                name="Mandolin", category="Western String",
                frequency_range=(300, 4500), characteristic_timbre="Bright, bouncy",
                attack_time=0.01, decay_time=0.15, sustain_level=0.5, release_time=0.2,
                vibrato_rate=4, vibrato_depth=0.03,
                harmonic_content=[1.0, 0.4, 0.2],
                dynamic_range=0.75
            ),
            "harp": InstrumentProfile(
                name="Harp", category="Western String",
                frequency_range=(30, 4000), characteristic_timbre="Bright, ethereal",
                attack_time=0.02, decay_time=0.3, sustain_level=0.3, release_time=0.4,
                vibrato_rate=0, vibrato_depth=0,
                harmonic_content=[1.0, 0.5, 0.2],
                dynamic_range=0.7
            ),
            "oud": InstrumentProfile(
                name="Oud", category="Middle Eastern String",
                frequency_range=(70, 3500), characteristic_timbre="Warm, resonant",
                attack_time=0.08, decay_time=0.12, sustain_level=0.8, release_time=0.2,
                vibrato_rate=3, vibrato_depth=0.05,
                harmonic_content=[1.0, 0.6, 0.4, 0.2],
                dynamic_range=0.75
            ),
            
            # Wind Instruments (6)
            "saxophone": InstrumentProfile(
                name="Saxophone", category="Western Wind",
                frequency_range=(104, 3500), characteristic_timbre="Warm, soulful",
                attack_time=0.06, decay_time=0.08, sustain_level=0.9, release_time=0.15,
                vibrato_rate=5, vibrato_depth=0.07,
                harmonic_content=[1.0, 0.5, 0.3, 0.2],
                dynamic_range=0.8
            ),
            "trumpet": InstrumentProfile(
                name="Trumpet", category="Western Wind",
                frequency_range=(165, 3500), characteristic_timbre="Bright, piercing",
                attack_time=0.04, decay_time=0.07, sustain_level=0.85, release_time=0.12,
                vibrato_rate=5, vibrato_depth=0.05,
                harmonic_content=[1.0, 0.6, 0.4, 0.2],
                dynamic_range=0.85
            ),
            "clarinet": InstrumentProfile(
                name="Clarinet", category="Western Wind",
                frequency_range=(165, 3000), characteristic_timbre="Warm, woody",
                attack_time=0.07, decay_time=0.06, sustain_level=0.9, release_time=0.14,
                vibrato_rate=4, vibrato_depth=0.06,
                harmonic_content=[1.0, 0.4, 0.2],
                dynamic_range=0.75
            ),
            "flute_western": InstrumentProfile(
                name="Western Flute", category="Western Wind",
                frequency_range=(260, 3500), characteristic_timbre="Pure, bright",
                attack_time=0.06, decay_time=0.05, sustain_level=0.92, release_time=0.12,
                vibrato_rate=5, vibrato_depth=0.05,
                harmonic_content=[1.0, 0.2, 0.1],
                dynamic_range=0.7
            ),
            "oboe": InstrumentProfile(
                name="Oboe", category="Western Wind",
                frequency_range=(233, 3000), characteristic_timbre="Warm, nasal",
                attack_time=0.08, decay_time=0.07, sustain_level=0.88, release_time=0.15,
                vibrato_rate=4, vibrato_depth=0.06,
                harmonic_content=[1.0, 0.5, 0.3],
                dynamic_range=0.75
            ),
            "trombone": InstrumentProfile(
                name="Trombone", category="Western Wind",
                frequency_range=(73, 2500), characteristic_timbre="Warm, mellow",
                attack_time=0.08, decay_time=0.1, sustain_level=0.85, release_time=0.18,
                vibrato_rate=4, vibrato_depth=0.06,
                harmonic_content=[1.0, 0.6, 0.4, 0.2],
                dynamic_range=0.8
            ),
            
            # Percussion Instruments (4)
            "drums": InstrumentProfile(
                name="Drums", category="Western Percussion",
                frequency_range=(40, 3000), characteristic_timbre="Punchy, dynamic",
                attack_time=0.01, decay_time=0.15, sustain_level=0.2, release_time=0.2,
                vibrato_rate=0, vibrato_depth=0,
                harmonic_content=[1.0, 0.6, 0.3, 0.1],
                dynamic_range=0.95
            ),
            "cymbals": InstrumentProfile(
                name="Cymbals", category="Western Percussion",
                frequency_range=(200, 5000), characteristic_timbre="Bright, shimmering",
                attack_time=0.01, decay_time=0.4, sustain_level=0.3, release_time=0.5,
                vibrato_rate=0, vibrato_depth=0,
                harmonic_content=[1.0, 0.7, 0.5, 0.3, 0.2],
                dynamic_range=0.9
            ),
            "marimba": InstrumentProfile(
                name="Marimba", category="Western Percussion",
                frequency_range=(65, 4000), characteristic_timbre="Warm, mellow",
                attack_time=0.02, decay_time=0.2, sustain_level=0.4, release_time=0.3,
                vibrato_rate=0, vibrato_depth=0,
                harmonic_content=[1.0, 0.5, 0.3, 0.2],
                dynamic_range=0.8
            ),
            "timpani": InstrumentProfile(
                name="Timpani", category="Western Percussion",
                frequency_range=(40, 1500), characteristic_timbre="Deep, resonant",
                attack_time=0.01, decay_time=0.2, sustain_level=0.3, release_time=0.25,
                vibrato_rate=0, vibrato_depth=0,
                harmonic_content=[1.0, 0.7, 0.4],
                dynamic_range=0.9
            ),
            
            # Keyboard (3)
            "piano": InstrumentProfile(
                name="Piano", category="Western Keyboard",
                frequency_range=(27, 4200), characteristic_timbre="Warm, balanced",
                attack_time=0.01, decay_time=0.4, sustain_level=0.5, release_time=0.5,
                vibrato_rate=0, vibrato_depth=0,
                harmonic_content=[1.0, 0.5, 0.3, 0.2],
                dynamic_range=0.9
            ),
            "organ": InstrumentProfile(
                name="Organ", category="Western Keyboard",
                frequency_range=(27, 4000), characteristic_timbre="Full, powerful",
                attack_time=0.05, decay_time=0, sustain_level=1.0, release_time=0.1,
                vibrato_rate=0, vibrato_depth=0,
                harmonic_content=[1.0, 0.4, 0.2, 0.1],
                dynamic_range=0.6
            ),
            "synthesizer": InstrumentProfile(
                name="Synthesizer", category="Electronic",
                frequency_range=(20, 20000), characteristic_timbre="Versatile, bright",
                attack_time=0.01, decay_time=0.1, sustain_level=0.9, release_time=0.1,
                vibrato_rate=6, vibrato_depth=0.08,
                harmonic_content=[1.0, 0.8, 0.6, 0.4, 0.3, 0.2],
                dynamic_range=0.95
            ),
        }
    
    def _calculate_compatibility(self) -> Dict[str, Dict[str, float]]:
        """Calculate compatibility scores between all instruments"""
        instruments = list(self.profiles.keys())
        compatibility = {}
        
        for inst1 in instruments:
            compatibility[inst1] = {}
            prof1 = self.profiles[inst1]
            
            for inst2 in instruments:
                if inst1 == inst2:
                    compatibility[inst1][inst2] = 1.0
                else:
                    prof2 = self.profiles[inst2]
                    
                    # Calculate compatibility based on frequency range overlap
                    freq_overlap = self._calculate_frequency_overlap(
                        prof1.frequency_range, prof2.frequency_range
                    )
                    
                    # Category compatibility
                    category_compat = self._get_category_compatibility(
                        prof1.category, prof2.category
                    )
                    
                    # Combined score
                    score = 0.4 * freq_overlap + 0.6 * category_compat
                    compatibility[inst1][inst2] = max(0.0, min(1.0, score))
        
        return compatibility
    
    @staticmethod
    def _calculate_frequency_overlap(range1: Tuple[float, float], 
                                     range2: Tuple[float, float]) -> float:
        """Calculate frequency range overlap percentage"""
        overlap_start = max(range1[0], range2[0])
        overlap_end = min(range1[1], range2[1])
        
        if overlap_end <= overlap_start:
            return 0.0
        
        overlap = overlap_end - overlap_start
        range1_span = range1[1] - range1[0]
        range2_span = range2[1] - range2[0]
        
        return overlap / max(range1_span, range2_span)
    
    @staticmethod
    def _get_category_compatibility(cat1: str, cat2: str) -> float:
        """Get category compatibility score"""
        # Define friendly category pairs
        friendly_pairs = {
            ("Indian Classical String", "Indian Classical Wind"): 0.9,
            ("Indian Classical String", "Indian Classical Percussion"): 0.8,
            ("Indian Classical Wind", "Indian Classical Percussion"): 0.85,
            ("Western String", "Western Wind"): 0.8,
            ("Western String", "Western Percussion"): 0.7,
            ("Western Wind", "Western Percussion"): 0.75,
            ("Indian Classical String", "Western String"): 0.7,
            ("Indian Classical Wind", "Western Wind"): 0.7,
            ("Electronic", "Western Percussion"): 0.8,
            ("Electronic", "Indian Classical String"): 0.75,
        }
        
        # Check both directions
        score = friendly_pairs.get((cat1, cat2)) or friendly_pairs.get((cat2, cat1))
        return score if score else 0.5
    
    def synthesize_instrument(self, instrument_id: str, duration_samples: int,
                            sample_rate: int, energy_level: float = 0.8) -> np.ndarray:
        """Synthesize instrument with given parameters"""
        if instrument_id not in self.profiles:
            logger.warning(f"Unknown instrument: {instrument_id}")
            return np.zeros(duration_samples)
        
        profile = self.profiles[instrument_id]
        
        # Generate base frequency content
        t = np.arange(duration_samples) / sample_rate
        fundamental = np.random.uniform(*profile.frequency_range)
        
        # Generate harmonics
        audio = np.zeros(duration_samples)
        for harmonic_idx, amplitude in enumerate(profile.harmonic_content):
            freq = fundamental * (harmonic_idx + 1)
            if freq < sample_rate / 2:
                audio += amplitude * np.sin(2 * np.pi * freq * t)
        
        # Apply ADSR envelope
        attack_samples = int(profile.attack_time * sample_rate)
        decay_samples = int(profile.decay_time * sample_rate)
        release_samples = int(profile.release_time * sample_rate)
        sustain_samples = duration_samples - attack_samples - decay_samples - release_samples
        
        envelope = np.concatenate([
            np.linspace(0, 1, attack_samples),
            np.linspace(1, profile.sustain_level, decay_samples),
            np.full(sustain_samples, profile.sustain_level),
            np.linspace(profile.sustain_level, 0, release_samples)
        ])
        
        # Ensure envelope matches duration
        if len(envelope) < duration_samples:
            envelope = np.pad(envelope, (0, duration_samples - len(envelope)))
        else:
            envelope = envelope[:duration_samples]
        
        # Apply envelope and energy
        audio = audio * envelope * energy_level
        
        # Apply vibrato if needed
        if profile.vibrato_rate > 0:
            vibrato = profile.vibrato_depth * np.sin(2 * np.pi * profile.vibrato_rate * t)
            audio = audio * (1 + vibrato)
        
        # Normalize
        max_val = np.max(np.abs(audio))
        if max_val > 0:
            audio = audio / max_val * profile.dynamic_range
        
        return audio
    
    def get_compatible_instruments(self, instrument_id: str, 
                                  min_compatibility: float = 0.5) -> List[str]:
        """Get instruments compatible with given instrument"""
        if instrument_id not in self.compatibility:
            return []
        
        compatible = []
        for other_inst, score in self.compatibility[instrument_id].items():
            if score >= min_compatibility and other_inst != instrument_id:
                compatible.append(other_inst)
        
        return compatible
    
    def suggest_ensemble(self, style_category: str, num_instruments: int = 4) -> List[str]:
        """Suggest ensemble instruments for a given style"""
        style_mapping = {
            "classical": ["sitar", "tabla", "sarangi", "flute"],
            "fusion": ["sitar", "guitar", "tabla", "synthesizer"],
            "jazz": ["saxophone", "piano", "bass", "drums"],
            "world": ["oud", "drums", "violin", "flute"],
            "orchestral": ["violin", "cello", "piano", "timpani"]
        }
        
        suggested = style_mapping.get(style_category.lower(), 
                                     list(self.profiles.keys())[:num_instruments])
        return suggested[:num_instruments]


# Initialize global instance
instrument_manager = InstrumentManager()
