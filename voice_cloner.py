"""
Voice cloning module using RVC (Retrieval-based Voice Conversion)
"""

import os
##from rvc_python.infer import RVCInference
from typing import Optional


class VoiceCloner:
    def __init__(self, models_dir: str = "models/rvc_models"):
        self.models_dir = models_dir
        self.rvc = None
        self.current_model = None
        
    def load_model(self, model_name: str, device: str = "cuda:0"):
        """
        Load RVC model for voice cloning
        model_name: name of the model folder (e.g., "kishore_kumar")
        """
        model_path = os.path.join(self.models_dir, model_name)
        
        # Find .pth file
        pth_file = None
        index_file = None
        
        for file in os.listdir(model_path):
            if file.endswith(".pth"):
                pth_file = os.path.join(model_path, file)
            elif file.endswith(".index"):
                index_file = os.path.join(model_path, file)
        
        if not pth_file:
            raise FileNotFoundError(f"No .pth model file found in {model_path}")
        
        ## Initialize RVC
        #if self.rvc is None:
        #    self.rvc = RVCInference(device=device)
        
        ## Load model
        #self.rvc.load_model(pth_file, index_file)
        #self.current_model = model_name
        #
        #print(f"✅ Loaded voice model: {model_name}")
        self.current_model = model_name
        print(f"✅ Found voice model files for: {model_name}")
    
    def clone_voice(self, input_audio: str, output_audio: str,
                    pitch_shift: int = 0,
                    index_rate: float = 0.5,
                    filter_radius: int = 3,
                    rms_mix_rate: float = 0.25,
                    protect: float = 0.33) -> str:
        """
        Convert voice in input audio to target voice.
        Temporarily disabled direct RVC library; will be replaced by RVC WebUI bridge.
        """
        raise NotImplementedError(
            "Voice cloning via RVC will be wired through RVC WebUI bridge."
        )
        
    
    def list_available_models(self) -> list:
        """
        List all available voice models
        """
        if not os.path.exists(self.models_dir):
            return []
        
        models = []
        for item in os.listdir(self.models_dir):
            item_path = os.path.join(self.models_dir, item)
            if os.path.isdir(item_path):
                # Check if contains .pth file
                has_pth = any(f.endswith(".pth") for f in os.listdir(item_path))
                if has_pth:
                    models.append(item)
        
        return models