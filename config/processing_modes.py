"""
Processing Modes Configuration
Defines the 3 different cover generation modes
"""

PROCESSING_MODES = {
    "remove_instruments": {
        "id": 1,
        "name": "Remove Instruments Only",
        "description": "Keep vocals, remove instruments. User adds custom instruments and performs.",
        "steps": [
            "Load audio",
            "Separate stems (extract vocals & instruments)",
            "Keep vocals only",
            "Select fusion style (Indo-Western, EDM-Indian, Jazz, etc.)",
            "User adds new instruments and sings"
        ],
        "output": "Vocals track ready for user performance",
        "use_case": "User wants to add their own instruments and sing",
        "complexity": "Low"
    },
    
    "remove_vocals": {
        "id": 2,
        "name": "Remove Vocals Only",
        "description": "Keep instruments, remove vocals. Create karaoke or add different singer.",
        "steps": [
            "Load audio",
            "Separate stems (extract vocals & instruments)",
            "Keep instruments only",
            "User can sing over it or use different singer's voice (RVC)"
        ],
        "output": "Instrumental track ready for vocal addition",
        "use_case": "Create karaoke or add different singer's voice",
        "complexity": "Low"
    },
    
    "full_remix": {
        "id": 3,
        "name": "Full Remix (Coke Studio Style)",
        "description": "Remove both vocals & instruments. System creates new cover in selected style.",
        "steps": [
            "Load audio",
            "Analyze: tempo, key, chords, melody",
            "Separate stems (remove all)",
            "Select fusion style (Indo-Western, EDM-Indian, Jazz, etc.)",
            "Apply reharmonization for target style",
            "Generate new instruments matching style",
            "Apply mixing & effects",
            "Generate backing track",
            "User sings or provides different singer's voice",
            "Apply pitch shifting if needed to match original"
        ],
        "output": "Professional backing track in selected style, ready for vocal performance",
        "use_case": "Create completely new cover in different style",
        "complexity": "High",
        "features": [
            "Reharmonization",
            "Style-specific instruments",
            "Tempo matching",
            "Melody preservation",
            "Voice conversion (pitch shifting)"
        ]
    }
}

# Fusion styles available for Full Remix mode
FUSION_STYLES_FOR_REMIX = {
    "indo_western": {
        "name": "Indo-Western Fusion",
        "description": "Blend Indian classical with Western pop/rock",
        "instruments": ["sitar", "guitar", "drums", "bass", "strings"],
        "raga_preference": "yaman",  # Default raga
        "tempo_modifier": 1.0  # Keep original tempo
    },
    "coke_studio": {
        "name": "Coke Studio Style",
        "description": "Minimalist acoustic with rich harmonies",
        "instruments": ["acousticguitar", "strings", "tabla_light", "harmonium"],
        "raga_preference": "bhairav",
        "tempo_modifier": 0.95
    },
    "edm_indian": {
        "name": "EDM + Indian Classical",
        "description": "Electronic dance beats with traditional instruments",
        "instruments": ["synth", "drums_electronic", "tabla", "flute"],
        "raga_preference": "khamaaj",
        "tempo_modifier": 1.2  # Slightly faster
    },
    "jazz_fusion": {
        "name": "Jazz Fusion",
        "description": "Smooth jazz with Indian touches",
        "instruments": ["piano", "bass_jazz", "drums_jazz", "tabla_light"],
        "raga_preference": "yaman",
        "tempo_modifier": 0.9
    },
    "orchestral": {
        "name": "Orchestral Arrangement",
        "description": "Full orchestra with Indian elements",
        "instruments": ["violin", "cello", "piano", "flute", "tabla"],
        "raga_preference": "bhairav",
        "tempo_modifier": 1.0
    }
}

# Separation quality settings
SEPARATION_QUALITY = {
    "fast": {
        "model": "htdemucs",
        "quality": "medium",
        "time": "~30 seconds"
    },
    "high": {
        "model": "htdemucs_ft",  # Fine-tuned, better quality
        "quality": "high",
        "time": "~2 minutes"
    }
}