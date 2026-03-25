"""
Full Remix Engine
Orchestrates the complete Full Remix (Coke Studio Style) workflow
This is the main orchestrator for Mode 3
"""

import logging
from typing import Dict, List, Optional
import numpy as np
from pathlib import Path

logger = logging.getLogger(__name__)

class FullRemixEngine:
    """
    Orchestrates full remix generation:
    1. Analyze original song
    2. Separate all stems
    3. Apply reharmonization
    4. Generate new instruments
    5. Mix everything
    6. Prepare for vocal addition
    """
    
    def __init__(self):
        self.logger = logger
        self.analysis = None
        self.stems = None
        self.reharmonized_chords = None
        self.generated_instruments = None
        self.mixed_output = None
    
    def generate_full_remix(self,
                           audio_path: str,
                           style: str = "indo_western",
                           target_raga: str = "yaman",
                           output_dir: str = "outputs") -> Dict:
        """
        Main method to generate full remix
        
        Workflow:
        1. Load audio
        2. Analyze (tempo, key, chords)
        3. Separate stems (remove vocals and instruments)
        4. Get target raga from style
        5. Reharmonize chords
        6. Generate new instruments
        7. Arrange and mix
        8. Output backing track
        
        Args:
            audio_path: Path to input song
            style: Fusion style (indo_western, coke_studio, edm_indian, jazz_fusion, orchestral)
            target_raga: Target raga for reharmonization
            output_dir: Output directory
        
        Returns:
            Dictionary with process details and output paths
        """
        
        self.logger.info(f"🎵 Starting Full Remix Generation")
        self.logger.info(f"  Style: {style}")
        self.logger.info(f"  Target Raga: {target_raga}")
        
        result = {
            "status": "processing",
            "style": style,
            "target_raga": target_raga,
            "steps": []
        }
        
        try:
            # Step 1: Load and analyze
            self.logger.info("📊 Step 1: Loading and analyzing original song...")
            from services.audio_processor import AudioProcessor
            from services.music_analyzer import MusicAnalyzer
            
            ap = AudioProcessor()
            ma = MusicAnalyzer()
            
            audio, sr = ap.load_audio(audio_path)
            self.analysis = ma.analyze_complete(audio)
            
            result["steps"].append({
                "name": "Analyze Original",
                "status": "✅ Complete",
                "data": {
                    "tempo": self.analysis['tempo'],
                    "key": self.analysis['key'],
                    "mode": self.analysis['mode']
                }
            })
            
            self.logger.info(f"  ✅ Tempo: {self.analysis['tempo']:.1f} BPM")
            self.logger.info(f"  ✅ Key: {self.analysis['key']} {self.analysis['mode']}")
            
            # Step 2: Separate stems
            self.logger.info("🎚️  Step 2: Separating stems (removing vocals and instruments)...")
            from services.stem_separator import StemSeparator
            
            separator = StemSeparator(sr=sr)
            self.stems = separator.separate(audio)
            
            result["steps"].append({
                "name": "Stem Separation",
                "status": "✅ Complete",
                "data": {
                    "stems_extracted": list(self.stems.keys())
                }
            })
            
            self.logger.info(f"  ✅ Stems separated: {list(self.stems.keys())}")
            
            # Step 3: Analyze chords and reharmonize
            self.logger.info("🎼 Step 3: Reharmonizing chords for target raga...")
            from services.reharmonizer import HarmonicReharmonizer
            
            reharmonizer = HarmonicReharmonizer()
            
            # Get chords from analysis
            original_chords = self.analysis.get('chords', [])
            
            # Reharmonize for target raga/style
            self.reharmonized_chords = reharmonizer.reharmonize_for_raga(
                original_chords,
                target_raga
            )
            
            result["steps"].append({
                "name": "Reharmonization",
                "status": "✅ Complete",
                "data": {
                    "original_chords": original_chords,
                    "reharmonized_chords": self.reharmonized_chords
                }
            })
            
            self.logger.info(f"  ✅ Original chords: {original_chords}")
            self.logger.info(f"  ✅ Reharmonized: {self.reharmonized_chords}")
            
            # Step 4: Generate new instruments
            self.logger.info("🎸 Step 4: Generating new instruments for style...")
            from services.instrument_synth import InstrumentSynthesizer
            
            synth = InstrumentSynthesizer(sr=sr)
            
            # Get instruments for this style
            from config.processing_modes import FUSION_STYLES_FOR_REMIX
            style_config = FUSION_STYLES_FOR_REMIX.get(style, {})
            instruments_list = style_config.get("instruments", ["sitar", "guitar", "drums", "bass"])
            
            self.generated_instruments = {}
            for instrument in instruments_list:
                self.logger.info(f"    Generating {instrument}...")
                
                # Map instrument to synthesis method
                if instrument.startswith("tabla"):
                    self.generated_instruments[instrument] = synth.synthesize_tabla_pattern(
                        'teentaal',
                        tempo_bpm=self.analysis['tempo'],
                        duration_seconds=len(audio) / sr
                    )
                elif instrument == "sitar":
                    self.generated_instruments[instrument] = synth.synthesize_sitar_performance(
                        self.reharmonized_chords,
                        np.ones(len(self.reharmonized_chords)),
                        target_raga
                    )
                elif instrument == "guitar":
                    self.generated_instruments[instrument] = synth.synthesize_guitar_strumming(
                        self.reharmonized_chords,
                        self.analysis['tempo'],
                        len(audio) / sr
                    )
                # Add more instruments as needed
            
            result["steps"].append({
                "name": "Instrument Synthesis",
                "status": "✅ Complete",
                "data": {
                    "instruments_generated": list(self.generated_instruments.keys()),
                    "style": style
                }
            })
            
            self.logger.info(f"  ✅ Generated instruments: {list(self.generated_instruments.keys())}")
            
            # Step 5: Arrange and mix
            self.logger.info("🎵 Step 5: Arranging and mixing...")
            from services.arranger import ArrangementEngine
            from services.mixer import MixingEngine
            
            arranger = ArrangementEngine()
            mixer = MixingEngine()
            
            # Detect song structure
            song_structure = arranger.analyze_song_structure(audio)
            
            # Build arrangement
            arranged = arranger.build_arrangement(
                self.generated_instruments,
                song_structure,
                style
            )
            
            # Mix
            mixing_config = {
                "style": style,
                "eq_preset": style,
                "compression": True,
                "reverb": 0.3
            }
            
            self.mixed_output = mixer.mix_stems(arranged, mixing_config)
            
            # Normalize loudness
            self.mixed_output = mixer.normalize_loudness(self.mixed_output, -18.0)
            
            result["steps"].append({
                "name": "Mixing",
                "status": "✅ Complete",
                "data": {
                    "mixing_config": mixing_config
                }
            })
            
            self.logger.info(f"  ✅ Mixing complete")
            
            # Step 6: Save output
            self.logger.info("💾 Step 6: Saving backing track...")
            
            output_path = Path(output_dir) / f"backing_track_{style}.wav"
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            ap.save_audio(self.mixed_output, str(output_path), sr)
            
            result["steps"].append({
                "name": "Save Output",
                "status": "✅ Complete",
                "data": {
                    "output_path": str(output_path),
                    "duration": len(self.mixed_output) / sr
                }
            })
            
            result["status"] = "completed"
            result["output_path"] = str(output_path)
            result["duration"] = len(self.mixed_output) / sr
            
            self.logger.info(f"🎉 Full Remix Complete!")
            self.logger.info(f"  Output: {output_path}")
            self.logger.info(f"  Duration: {result['duration']:.2f} seconds")
            
            return result
            
        except Exception as e:
            self.logger.error(f"❌ Error in full remix generation: {e}")
            result["status"] = "error"
            result["error"] = str(e)
            return result
    
    def get_summary(self) -> Dict:
        """Get summary of remix process"""
        return {
            "original_analysis": self.analysis,
            "reharmonized_chords": self.reharmonized_chords,
            "generated_instruments": list(self.generated_instruments.keys()) if self.generated_instruments else [],
            "output_duration": len(self.mixed_output) / 44100 if self.mixed_output is not None else 0
        }