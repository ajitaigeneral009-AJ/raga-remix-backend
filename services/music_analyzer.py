"""
Music analysis: key, tempo, melody, chords
"""

import numpy as np
import librosa
from typing import Dict, Tuple, List
import logging

logger = logging.getLogger(__name__)

class MusicAnalyzer:
    """
    Analyze musical properties of audio
    """
    
    def __init__(self, sr: int = 44100):
        self.sr = sr
        self.note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    
    def detect_tempo(self, audio: np.ndarray) -> Tuple[float, np.ndarray]:
        """
        Detect tempo (BPM) and beat frames
        
        Returns:
            Tuple of (tempo_bpm, beat_frames)
        """
        try:
            # Compute onset strength
            onset_env = librosa.onset.onset_strength(y=audio, sr=self.sr)
            
            # Estimate tempo
            tempo, beats = librosa.beat.beat_track(onset_envelope=onset_env, sr=self.sr)
            
            logger.info(f"Detected tempo: {tempo:.2f} BPM")
            return float(tempo), beats
            
        except Exception as e:
            logger.error(f"Failed to detect tempo: {e}")
            return 120.0, np.array([])  # Default fallback
    
    def detect_key(self, audio: np.ndarray) -> Dict:
        """
        Detect musical key
        
        Returns:
            Dict with 'key', 'mode' (major/minor), 'confidence'
        """
        try:
            # Compute chroma features
            chroma = librosa.feature.chroma_cqt(y=audio, sr=self.sr)
            chroma_mean = chroma.mean(axis=1)
            
            # Major and minor templates
            major_template = np.array([1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1])
            minor_template = np.array([1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1])
            
            # Correlate with templates
            major_scores = np.correlate(chroma_mean, major_template, mode='same')
            minor_scores = np.correlate(chroma_mean, minor_template, mode='same')
            
            # Find best key
            major_key_idx = np.argmax(major_scores)
            minor_key_idx = np.argmax(minor_scores)
            
            major_score = major_scores[major_key_idx]
            minor_score = minor_scores[minor_key_idx]
            
            if major_score > minor_score:
                key_idx = major_key_idx
                mode = 'major'
                confidence = major_score
            else:
                key_idx = minor_key_idx
                mode = 'minor'
                confidence = minor_score
            
            key_name = self.note_names[key_idx]
            
            result = {
                'key': key_name,
                'mode': mode,
                'confidence': float(confidence),
                'all_keys': {
                    'major': [(self.note_names[i], float(s)) for i, s in enumerate(major_scores)],
                    'minor': [(self.note_names[i], float(s)) for i, s in enumerate(minor_scores)],
                }
            }
            
            logger.info(f"Detected key: {key_name} {mode.upper()}")
            return result
            
        except Exception as e:
            logger.error(f"Failed to detect key: {e}")
            return {'key': 'C', 'mode': 'major', 'confidence': 0.0}
    
    def extract_melody(self, audio: np.ndarray) -> np.ndarray:
        """
        Extract pitch contour (melody)
        Using librosa's crepe-like approach
        """
        try:
            # Compute STFT
            S = np.abs(librosa.stft(audio))
            
            # Extract harmonics
            harmonic, percussive = librosa.decompose.hpss(S)
            
            # Get fundamental frequency from harmonic component
            # This is simplified - for production use actual CREPE model
            frequencies = librosa.fft_frequencies(sr=self.sr)
            
            # Get peak frequency per frame
            melody = np.zeros(harmonic.shape[1])
            for i in range(harmonic.shape[1]):
                if harmonic[:, i].max() > 0:
                    melody[i] = frequencies[np.argmax(harmonic[:, i])]
            
            logger.info(f"Extracted melody contour, {len(melody)} frames")
            return melody
            
        except Exception as e:
            logger.error(f"Failed to extract melody: {e}")
            return np.array([])
    
    def extract_chords(self, audio: np.ndarray) -> List[str]:
        """
        Estimate chord progression
        Simplified approach - for production use specialized library
        """
        try:
            # Compute chroma features
            chroma = librosa.feature.chroma_cqt(y=audio, sr=self.sr)
            
            # Define chord templates (simplified - triads only)
            chord_templates = {
                'C': np.array([1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0]),
                'C#': np.array([0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0]),
                'D': np.array([0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0]),
                # ... add all 12 keys
                'Cm': np.array([1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0]),
                # ... minor chords
            }
            
            chords = []
            # Reduce chroma to beats for better robustness
            beat_chroma = librosa.util.sync(chroma, librosa.frames_to_samples(np.arange(chroma.shape[1]), sr=self.sr)//2048)
            
            for frame_chroma in beat_chroma.T:
                best_chord = 'C'
                best_score = 0
                
                for chord_name, template in chord_templates.items():
                    score = np.dot(frame_chroma, template)
                    if score > best_score:
                        best_score = score
                        best_chord = chord_name
                
                chords.append(best_chord)
            
            logger.info(f"Extracted chord progression: {len(chords)} chords")
            return chords
            
        except Exception as e:
            logger.error(f"Failed to extract chords: {e}")
            return []
    
    def analyze_complete(self, audio: np.ndarray) -> Dict:
        """
        Complete music analysis
        """
        logger.info("Starting complete music analysis...")
        
        tempo, beats = self.detect_tempo(audio)
        key_info = self.detect_key(audio)
        melody = self.extract_melody(audio)
        chords = self.extract_chords(audio)
        
        # Energy analysis
        S = np.abs(librosa.stft(audio))
        energy = np.sqrt(np.sum(S**2, axis=0))
        energy_db = librosa.power_to_db(energy, ref=np.max)
        
        analysis = {
            'tempo': tempo,
            'beats': beats.tolist() if len(beats) > 0 else [],
            'key': key_info['key'],
            'mode': key_info['mode'],
            'key_confidence': key_info['confidence'],
            'melody': melody.tolist() if len(melody) > 0 else [],
            'chords': chords,
            'energy': energy_db.tolist() if len(energy_db) > 0 else [],
            'duration_seconds': len(audio) / self.sr,
        }
        
        logger.info("Music analysis complete")
        return analysis