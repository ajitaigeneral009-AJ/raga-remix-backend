"""
Fusion Styles Database
Complete definitions for 9 fusion music styles
"""

FUSION_STYLES = {
    "indo_western_classical": {
        "name": "Indo-Western Classical Fusion",
        "base_ragas": ["Yaman", "Bihag", "Kafi"],
        "primary_instruments": {
            "indian": ["Tabla", "Sitar", "Bansuri", "Tanpura"],
            "western": ["Violin", "Cello", "Piano"],
            "electronic": []
        },
        "tempo_adjustment_range": (0.8, 1.2),
        "energy_progression": [0.3, 0.5, 0.7, 0.9],
        "characteristic_features": [
            "Classical raga structure",
            "Western orchestration",
            "Gradual energy build"
        ],
        "mixing_guidelines": {
            "vocals": 0.0,  # dB
            "tabla": -2.0,
            "sitar": -4.0,
            "violin": -5.0,
            "tanpura": -12.0
        },
        "description": "Elegant blend of Hindustani classical with Western classical elements"
    },
    
    "jazz_indian_fusion": {
        "name": "Jazz-Indian Fusion",
        "base_ragas": ["Bhairav", "Marwa", "Puriya"],
        "primary_instruments": {
            "indian": ["Tabla", "Bansuri", "Sitar"],
            "western": ["Saxophone", "Piano", "Bass Guitar", "Drums"],
            "electronic": []
        },
        "tempo_adjustment_range": (0.9, 1.3),
        "energy_progression": [0.4, 0.6, 0.8, 0.7],
        "characteristic_features": [
            "Swing rhythms",
            "Improvisation",
            "Modal harmony",
            "Complex time signatures"
        ],
        "mixing_guidelines": {
            "vocals": 0.0,
            "saxophone": -3.0,
            "tabla": -4.0,
            "piano": -5.0,
            "bass": -6.0
        },
        "description": "Sophisticated fusion of jazz improvisation with raga-based melodies"
    },
    
    "rock_raga_fusion": {
        "name": "Rock-Raga Fusion",
        "base_ragas": ["Bhairav", "Darbari", "Malkauns"],
        "primary_instruments": {
            "indian": ["Sitar", "Tabla"],
            "western": ["Electric Guitar", "Bass Guitar", "Drums"],
            "electronic": ["Synth Pad"]
        },
        "tempo_adjustment_range": (1.0, 1.4),
        "energy_progression": [0.5, 0.7, 0.9, 1.0],
        "characteristic_features": [
            "Heavy distortion",
            "Sitar lead lines",
            "Driving rhythms",
            "Power chords"
        ],
        "mixing_guidelines": {
            "vocals": 0.0,
            "electric_guitar": -2.0,
            "sitar": -3.0,
            "drums": -4.0,
            "bass": -5.0
        },
        "description": "High-energy combination of rock power with raga melodies"
    },
    
    "bollywood_electronic": {
        "name": "Bollywood Electronic",
        "base_ragas": ["Kafi", "Khamaj", "Bhairavi"],
        "primary_instruments": {
            "indian": ["Tabla", "Harmonium"],
            "western": ["Violin", "Guitar"],
            "electronic": ["Synth Pad", "Drum Machine", "Bass Synth"]
        },
        "tempo_adjustment_range": (0.95, 1.25),
        "energy_progression": [0.4, 0.6, 0.9, 0.8],
        "characteristic_features": [
            "Catchy hooks",
            "Electronic beats",
            "Orchestral strings",
            "Romantic themes"
        ],
        "mixing_guidelines": {
            "vocals": 0.0,
            "synth_pad": -6.0,
            "tabla": -4.0,
            "violin": -5.0,
            "drum_machine": -3.0
        },
        "description": "Modern Bollywood sound with electronic production"
    },
    
    "edm_indian_fusion": {
        "name": "EDM-Indian Fusion",
        "base_ragas": ["Flexible"],
        "primary_instruments": {
            "indian": ["Tabla", "Bansuri"],
            "western": [],
            "electronic": ["Synth Lead", "Bass Synth", "Drum Machine", "Synth Pad"]
        },
        "tempo_adjustment_range": (1.1, 1.5),
        "energy_progression": [0.3, 0.5, 0.8, 1.0],
        "characteristic_features": [
            "Build-ups and drops",
            "Heavy bass",
            "Indian melody samples",
            "Festival energy"
        ],
        "mixing_guidelines": {
            "vocals": 0.0,
            "bass_synth": -2.0,
            "synth_lead": -4.0,
            "tabla": -6.0,
            "kick": -1.0
        },
        "description": "High-energy electronic dance music with Indian classical elements"
    },
    
    "hip_hop_indian": {
        "name": "Hip-Hop Indian",
        "base_ragas": ["Bhairavi", "Kafi", "Yaman"],
        "primary_instruments": {
            "indian": ["Tabla", "Sitar", "Bansuri"],
            "western": [],
            "electronic": ["Bass Synth", "Drum Machine", "Synth Pad"]
        },
        "tempo_adjustment_range": (0.85, 1.15),
        "energy_progression": [0.5, 0.6, 0.7, 0.8],
        "characteristic_features": [
            "Boom-bap beats",
            "Sampled tabla loops",
            "Sitar melodies",
            "Heavy bass"
        ],
        "mixing_guidelines": {
            "vocals": 0.0,
            "drum_machine": -2.0,
            "bass_synth": -3.0,
            "sitar": -6.0,
            "tabla_loop": -5.0
        },
        "description": "Hip-hop beats infused with Indian classical samples and instruments"
    },
    
    "sufi_rock": {
        "name": "Sufi Rock",
        "base_ragas": ["Kafi", "Bhairavi", "Pilu"],
        "primary_instruments": {
            "indian": ["Harmonium", "Tabla", "Dholak"],
            "western": ["Electric Guitar", "Bass Guitar", "Drums"],
            "electronic": []
        },
        "tempo_adjustment_range": (0.9, 1.2),
        "energy_progression": [0.3, 0.5, 0.8, 0.9],
        "characteristic_features": [
            "Devotional vocals",
            "Guitar-driven",
            "Spiritual intensity",
            "Tabla-drum fusion"
        ],
        "mixing_guidelines": {
            "vocals": 0.0,
            "harmonium": -5.0,
            "electric_guitar": -3.0,
            "tabla": -4.0,
            "drums": -4.0
        },
        "description": "Spiritual Sufi traditions meet rock intensity"
    },
    
    "carnatic_jazz": {
        "name": "Carnatic Jazz",
        "base_ragas": ["Kalyani", "Mohanam", "Sankarabharanam"],
        "primary_instruments": {
            "indian": ["Violin", "Mridangam", "Ghatam"],
            "western": ["Piano", "Saxophone", "Double Bass", "Drums"],
            "electronic": []
        },
        "tempo_adjustment_range": (0.9, 1.35),
        "energy_progression": [0.4, 0.7, 0.9, 0.8],
        "characteristic_features": [
            "Complex rhythmic cycles",
            "Improvisation",
            "Carnatic violin",
            "Jazz harmony"
        ],
        "mixing_guidelines": {
            "vocals": 0.0,
            "violin": -3.0,
            "mridangam": -4.0,
            "piano": -5.0,
            "saxophone": -4.0
        },
        "description": "South Indian Carnatic music meets jazz sophistication"
    },
    
    "edm_bhangra": {
        "name": "EDM Bhangra",
        "base_ragas": ["Flexible"],
        "primary_instruments": {
            "indian": ["Dhol", "Tumbi"],
            "western": [],
            "electronic": ["Synth Lead", "Bass Synth", "Drum Machine"]
        },
        "tempo_adjustment_range": (1.15, 1.45),
        "energy_progression": [0.6, 0.8, 1.0, 1.0],
        "characteristic_features": [
            "High energy",
            "Festival vibe",
            "Dhol patterns",
            "Electronic drops"
        ],
        "mixing_guidelines": {
            "vocals": 0.0,
            "dhol": -2.0,
            "bass_synth": -3.0,
            "synth_lead": -4.0,
            "drum_machine": -2.0
        },
        "description": "Punjabi Bhangra energy with modern EDM production"
    }
}


def get_fusion_style(style_id: str):
    """Get fusion style by ID"""
    return FUSION_STYLES.get(style_id)


def get_all_fusion_styles():
    """Get all fusion style names"""
    return list(FUSION_STYLES.keys())


def get_instruments_for_style(style_id: str):
    """Get recommended instruments for a fusion style"""
    style = FUSION_STYLES.get(style_id)
    if not style:
        return []
    
    instruments = []
    for category, inst_list in style["primary_instruments"].items():
        instruments.extend(inst_list)
    
    return instruments


def get_mixing_levels(style_id: str):
    """Get mixing level guidelines for a style"""
    style = FUSION_STYLES.get(style_id)
    if not style:
        return {}
    
    return style.get("mixing_guidelines", {})


if __name__ == "__main__":
    print(f"✅ Fusion Styles Database loaded: {len(FUSION_STYLES)} styles")
    
    # Test
    style = get_fusion_style("indo_western_classical")
    print(f"\\nIndo-Western Classical:")
    print(f"  Base Ragas: {style['base_ragas']}")
    print(f"  Indian Instruments: {style['primary_instruments']['indian']}")
    print(f"  Description: {style['description']}")
