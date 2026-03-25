"""
Raga and scale analysis - the foundation of quality
"""

import numpy as np
from typing import List, Dict, Tuple
from config.raga_database import RAGAS, SCALES, INSTRUMENTS
import logging

logger = logging.getLogger(__name__)

class RagaAnalyzer:
    """
    Analyze and map audio to raga/scale constraints
    """
    
    def __init__(self):
        self.ragas = RAGAS
        self.note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    
    def freq_to_note(self, freq: float, reference: float = 440.0) -> Tuple[str, float]:
        """
        Convert frequency to note name
        
        Args:
            freq: Frequency in Hz
            reference: Reference frequency (A4 = 440 Hz)
            
        Returns:
            Tuple of (note_name, cents_deviation)
        """
        if freq <= 0:
            return None, 0
        
        # Calculate semitones from A4
        semitones = 12 * np.log2(freq / reference) + 9
        
        # Note index (0-11)
        note_idx = int(round(semitones % 12))
        octave = int(semitones // 12) + 4
        
        note_name = self.note_names[note_idx]
        cents = (semitones - round(semitones)) * 100
        
        return f"{note_name}{octave}", cents
    
    def note_to_freq(self, note: str, reference: float = 440.0) -> float:
        """
        Convert note name to frequency
        """
        # Parse note (e.g., "C4", "F#5")
        note_name = note[:-1]
        octave = int(note[-1])
        
        semitones_from_a4 = self.note_names.index(note_name) + (octave - 4) * 12 - 9
        freq = reference * (2 ** (semitones_from_a4 / 12))
        return freq
    
    def get_raga_notes(self, raga_name: str) -> List[str]:
        """
        Get all notes in a raga
        """
        if raga_name not in self.ragas:
            return []
        
        raga = self.ragas[raga_name]
        if 'notes_solfege' in raga:
            return raga['notes_solfege']
        elif 'notes_chromatic' in raga:
            return raga['notes_chromatic']
        return []
    
    def is_note_in_raga(self, note: str, raga_name: str) -> bool:
        """
        Check if note is in raga
        """
        raga_notes = self.get_raga_notes(raga_name)
        return note in raga_notes
    
    def find_closest_raga_note(self, note: str, raga_name: str) -> str:
        """
        Find closest note in raga if input not in raga
        """
        if self.is_note_in_raga(note, raga_name):
            return note
        
        raga_notes = self.get_raga_notes(raga_name)
        if not raga_notes:
            return note
        
        # Convert to frequencies for comparison
        target_freq = self.note_to_freq(note)
        
        min_distance = float('inf')
        closest_note = raga_notes[0]
        
        for raga_note in raga_notes:
            raga_freq = self.note_to_freq(raga_note)
            distance = abs(target_freq - raga_freq)
            
            if distance < min_distance:
                min_distance = distance
                closest_note = raga_note
        
        logger.info(f"Mapped {note} to raga note {closest_note}")
        return closest_note
    
    def get_raga_characteristics(self, raga_name: str) -> Dict:
        """
        Get detailed raga characteristics
        """
        if raga_name not in self.ragas:
            return {}
        
        return self.ragas[raga_name]
    
    def are_ragas_compatible(self, raga1: str, raga2: str) -> float:
        """
        Determine compatibility between two ragas (0-1 score)
        """
        if raga1 == raga2:
            return 1.0
        
        notes1 = set(self.get_raga_notes(raga1))
        notes2 = set(self.get_raga_notes(raga2))
        
        if not notes1 or not notes2:
            return 0.0
        
        # Jaccard similarity
        intersection = len(notes1 & notes2)
        union = len(notes1 | notes2)
        
        return intersection / union if union > 0 else 0.0
    
    def suggest_compatible_ragas(self, input_raga: str, n: int = 5) -> List[Tuple[str, float]]:
        """
        Suggest ragas compatible with input raga
        """
        compatibility_scores = []
        
        for raga_name in self.ragas:
            if raga_name != input_raga:
                score = self.are_ragas_compatible(input_raga, raga_name)
                compatibility_scores.append((raga_name, score))
        
        # Sort by score descending
        compatibility_scores.sort(key=lambda x: x[1], reverse=True)
        return compatibility_scores[:n]
    
    def get_scale_for_raga(self, raga_name: str) -> Dict:
        """
        Get scale information for a raga
        """
        raga = self.get_raga_characteristics(raga_name)
        notes = raga.get('notes_chromatic', [])
        
        if not notes:
            return {}
        
        # Convert to intervals
        intervals = []
        for i in range(len(notes)):
            note_idx = self.note_names.index(notes[i])
            intervals.append(note_idx)
        
        # Normalize intervals relative to C
        base_interval = intervals[0]
        normalized_intervals = [(i - base_interval) % 12 for i in intervals]
        normalized_intervals.sort()
        
        return {
            'name': raga_name,
            'notes': notes,
            'intervals': normalized_intervals,
            'interval_distances': self._compute_interval_distances(normalized_intervals),
        }
    
    def _compute_interval_distances(self, intervals: List[int]) -> Dict[str, float]:
        """
        Compute distances between intervals
        """
        distances = {}
        interval_names = ['unison', 'minor_2nd', 'major_2nd', 'minor_3rd', 'major_3rd', 
                         'perfect_4th', 'tritone', 'perfect_5th', 'minor_6th', 'major_6th', 
                         'minor_7th', 'major_7th']
        
        for i in intervals:
            distances[interval_names[i]] = float(i)
        
        return distances
