"""
Instrument Database
Comprehensive database of 30+ Indian, Western, and Electronic instruments
"""

INSTRUMENT_DATABASE = {
    # ============================================================
    # INDIAN CLASSICAL INSTRUMENTS
    # ============================================================
    
    "Tabla": {
        "category": "Indian",
        "type": "percussion",
        "role": "rhythm",
        "frequency_range": (150, 1000),  # Hz
        "midi_program": 116,  # Taiko Drum
        "playing_techniques": ["bols", "tihai", "peshkar"],
        "taal_patterns": ["teentaal", "dadra", "keherwa", "jhaptaal"],
        "fusion_compatibility": {
            "rock": 0.8,
            "jazz": 0.9,
            "edm": 0.85,
            "hip_hop": 0.9
        },
        "description": "Twin drums fundamental to Hindustani classical music"
    },
    
    "Sitar": {
        "category": "Indian",
        "type": "string",
        "role": "melody",
        "frequency_range": (196, 1976),  # C3 to B6
        "midi_program": 104,
        "playing_techniques": ["meend", "gamaka", "murki", "zamzama"],
        "tunings": ["kharaj_pancham", "instrumental"],
        "fusion_compatibility": {
            "rock": 0.95,
            "jazz": 0.85,
            "blues": 0.9
        },
        "description": "Iconic plucked string instrument with sympathetic strings"
    },
    
    "Sarod": {
        "category": "Indian",
        "type": "string",
        "role": "melody",
        "frequency_range": (147, 1568),  # D3 to G6
        "midi_program": 104,
        "playing_techniques": ["meend", "jhala", "stroke"],
        "fusion_compatibility": {
            "classical": 1.0,
            "fusion": 0.9,
            "jazz": 0.8
        },
        "description": "Fretless string instrument with metallic tone"
    },
    
    "Bansuri": {
        "category": "Indian",
        "type": "wind",
        "role": "melody",
        "frequency_range": (262, 2093),  # C4 to C7
        "midi_program": 73,  # Flute
        "playing_techniques": ["krintan", "murki", "gamaka"],
        "fusion_compatibility": {
            "world": 0.95,
            "jazz": 0.9,
            "ambient": 1.0
        },
        "description": "Bamboo flute with breathy, expressive tone"
    },
    
    "Harmonium": {
        "category": "Indian",
        "type": "keyboard",
        "role": "harmony",
        "frequency_range": (131, 1047),  # C3 to C6
        "midi_program": 21,  # Accordion
        "playing_techniques": ["drone", "melody", "accompaniment"],
        "fusion_compatibility": {
            "devotional": 1.0,
            "folk": 0.95,
            "classical": 0.9
        },
        "description": "Hand-pumped reed organ used for accompaniment"
    },
    
    "Santoor": {
        "category": "Indian",
        "type": "string",
        "role": "melody",
        "frequency_range": (262, 2093),  # C4 to C7
        "midi_program": 15,  # Dulcimer
        "playing_techniques": ["tremolo", "glissando"],
        "fusion_compatibility": {
            "world": 0.9,
            "new_age": 0.95,
            "classical": 0.85
        },
        "description": "Hammered dulcimer with shimmering cascading notes"
    },
    
    "Tanpura": {
        "category": "Indian",
        "type": "string",
        "role": "drone",
        "frequency_range": (98, 392),  # G2 to G4
        "midi_program": 89,  # Pad 2 (warm)
        "playing_techniques": ["drone"],
        "fusion_compatibility": {
            "classical": 1.0,
            "ambient": 0.95,
            "meditation": 1.0
        },
        "description": "Four-stringed drone instrument providing tonal foundation"
    },
    
    "Dholak": {
        "category": "Indian",
        "type": "percussion",
        "role": "rhythm",
        "frequency_range": (150, 800),
        "midi_program": 117,
        "playing_techniques": ["open", "closed", "slap"],
        "fusion_compatibility": {
            "folk": 1.0,
            "bhangra": 1.0,
            "bollywood": 0.95
        },
        "description": "Two-headed hand drum used in folk music"
    },
    
    # ============================================================
    # WESTERN CLASSICAL & CONTEMPORARY INSTRUMENTS
    # ============================================================
    
    "Acoustic Guitar": {
        "category": "Western",
        "type": "string",
        "role": "harmony",
        "frequency_range": (82, 1319),  # E2 to E6
        "midi_program": 24,
        "playing_techniques": ["strumming", "fingerpicking", "arpeggio"],
        "tuning": ["standard", "drop_d", "open_g"],
        "fusion_compatibility": {
            "fusion": 1.0,
            "folk": 0.95,
            "pop": 1.0
        },
        "description": "Versatile stringed instrument for chords and melody"
    },
    
    "Electric Guitar": {
        "category": "Western",
        "type": "string",
        "role": "lead",
        "frequency_range": (82, 1319),  # E2 to E6
        "midi_program": 29,
        "playing_techniques": ["bending", "vibrato", "distortion", "tapping"],
        "fusion_compatibility": {
            "rock": 1.0,
            "fusion": 0.95,
            "blues": 1.0
        },
        "description": "Amplified guitar with sustain and effects"
    },
    
    "Bass Guitar": {
        "category": "Western",
        "type": "string",
        "role": "bass",
        "frequency_range": (41, 392),  # E1 to G4
        "midi_program": 33,
        "playing_techniques": ["fingerstyle", "slap", "plucking"],
        "fusion_compatibility": {
            "rock": 1.0,
            "funk": 1.0,
            "jazz": 0.95
        },
        "description": "Low-frequency instrument providing rhythmic foundation"
    },
    
    "Piano": {
        "category": "Western",
        "type": "keyboard",
        "role": "harmony",
        "frequency_range": (27, 4186),  # A0 to C8
        "midi_program": 0,  # Acoustic Grand Piano
        "playing_techniques": ["legato", "staccato", "tremolo"],
        "fusion_compatibility": {
            "classical": 1.0,
            "jazz": 1.0,
            "fusion": 0.95
        },
        "description": "88-key keyboard instrument with rich harmonic range"
    },
    
    "Violin": {
        "category": "Western",
        "type": "string",
        "role": "melody",
        "frequency_range": (196, 2637),  # G3 to E7
        "midi_program": 40,
        "playing_techniques": ["bowing", "pizzicato", "vibrato"],
        "fusion_compatibility": {
            "classical": 1.0,
            "carnatic": 0.95,
            "folk": 0.9
        },
        "description": "Bowed string instrument with expressive capabilities"
    },
    
    "Cello": {
        "category": "Western",
        "type": "string",
        "role": "bass_melody",
        "frequency_range": (65, 988),  # C2 to B5
        "midi_program": 42,
        "playing_techniques": ["bowing", "pizzicato"],
        "fusion_compatibility": {
            "classical": 1.0,
            "cinematic": 0.95
        },
        "description": "Low-register string instrument with warm tone"
    },
    
    "Saxophone": {
        "category": "Western",
        "type": "wind",
        "role": "melody",
        "frequency_range": (138, 880),  # Bb2 to A5
        "midi_program": 66,  # Tenor Sax
        "playing_techniques": ["vibrato", "bending", "altissimo"],
        "fusion_compatibility": {
            "jazz": 1.0,
            "funk": 0.95,
            "fusion": 0.9
        },
        "description": "Jazz woodwind with expressive, vocal-like quality"
    },
    
    "Drums": {
        "category": "Western",
        "type": "percussion",
        "role": "rhythm",
        "frequency_range": (60, 12000),
        "midi_program": 0,  # Standard Kit
        "components": ["kick", "snare", "hi-hat", "toms", "cymbals"],
        "fusion_compatibility": {
            "rock": 1.0,
            "fusion": 0.95,
            "pop": 1.0
        },
        "description": "Kit of percussion instruments for rhythm section"
    },
    
    # ============================================================
    # ELECTRONIC INSTRUMENTS
    # ============================================================
    
    "Synth Pad": {
        "category": "Electronic",
        "type": "synthesizer",
        "role": "texture",
        "frequency_range": (20, 20000),
        "midi_program": 88,
        "playing_techniques": ["sustained", "swelling", "layering"],
        "fusion_compatibility": {
            "edm": 1.0,
            "ambient": 1.0,
            "fusion": 0.9
        },
        "description": "Sustained synthesizer sound for atmosphere"
    },
    
    "Synth Lead": {
        "category": "Electronic",
        "type": "synthesizer",
        "role": "melody",
        "frequency_range": (20, 20000),
        "midi_program": 80,
        "playing_techniques": ["monophonic", "portamento"],
        "fusion_compatibility": {
            "edm": 1.0,
            "pop": 0.95
        },
        "description": "Bright synthesizer for lead melodies"
    },
    
    "Bass Synth": {
        "category": "Electronic",
        "type": "synthesizer",
        "role": "bass",
        "frequency_range": (20, 500),
        "midi_program": 38,
        "playing_techniques": ["wobble", "sub_bass"],
        "fusion_compatibility": {
            "edm": 1.0,
            "dubstep": 1.0,
            "hip_hop": 0.9
        },
        "description": "Low-frequency synthesizer bass"
    },
    
    "Drum Machine": {
        "category": "Electronic",
        "type": "percussion",
        "role": "rhythm",
        "frequency_range": (60, 12000),
        "midi_program": 0,
        "playing_techniques": ["programmed_patterns"],
        "fusion_compatibility": {
            "edm": 1.0,
            "hip_hop": 1.0,
            "pop": 0.95
        },
        "description": "Electronic percussion with programmable patterns"
    }
}


def get_instrument_by_name(name: str):
    """Get instrument data by name"""
    return INSTRUMENT_DATABASE.get(name)


def get_instruments_by_category(category: str):
    """Get all instruments in a category"""
    return {
        name: data
        for name, data in INSTRUMENT_DATABASE.items()
        if data["category"] == category
    }


def get_compatible_instruments(instrument_name: str, style: str):
    """Get instruments compatible with given instrument and style"""
    compatible = []
    
    for name, data in INSTRUMENT_DATABASE.items():
        if name == instrument_name:
            continue
        
        compatibility = data.get("fusion_compatibility", {}).get(style, 0)
        if compatibility >= 0.7:
            compatible.append({
                "name": name,
                "compatibility": compatibility
            })
    
    return sorted(compatible, key=lambda x: x["compatibility"], reverse=True)


if __name__ == "__main__":
    print(f"✅ Instrument Database loaded: {len(INSTRUMENT_DATABASE)} instruments")
    
    # Test
    tabla = get_instrument_by_name("Tabla")
    print(f"Tabla: {tabla['description']}")
    
    indian = get_instruments_by_category("Indian")
    print(f"Indian instruments: {list(indian.keys())}")
