"""
Style-specific configuration for cover generation
"""

STYLE_TEMPLATES = {
    'hindustani_classical': {
        'display_name': 'Hindustani Classical',
        'recommended_ragas': ['yaman', 'bhairav', 'khamaaj', 'ahir_bhairav', 'marwa', 'todi'],
        'recommended_instruments': {
            'primary': ['sitar', 'sarangi', 'bansuri'],
            'secondary': ['harmonium', 'tabla', 'mridangam'],
        },
        'arrangement_style': 'traditional_raga',
        'mixing_preset': 'classical_dry',
        'tempo_adaptation': 'minimal',
        'vocal_treatment': 'preserved_prominent',
        'characteristic_features': {
            'allows_meend': True,
            'allows_gamak': True,
            'allows_improvisation': True,
            'rhythm_based_on': 'taal',
        }
    },
    
    'carnatic_classical': {
        'display_name': 'Carnatic Classical',
        'recommended_ragas': ['dheerashankarabharanam', 'mayamalavagowla'],
        'recommended_instruments': {
            'primary': ['veena', 'vina'],
            'secondary': ['mridangam', 'kanjira'],
        },
        'arrangement_style': 'south_indian_raga',
        'mixing_preset': 'classical_dry',
        'tempo_adaptation': 'rhythmic_cycles',
        'vocal_treatment': 'preserved_prominent',
    },
    
    'qawwali_sufi': {
        'display_name': 'Qawwali + Sufi Music',
        'recommended_ragas': [],
        'recommended_instruments': {
            'primary': ['harmonium', 'tabla'],
            'secondary': ['sarangi', 'dholak'],
        },
        'arrangement_style': 'qawwali_devotional',
        'mixing_preset': 'warm_reverb',
        'vocal_treatment': 'call_response',
    },
    
    'bollywood_pop': {
        'display_name': 'Bollywood / Film Pop',
        'recommended_ragas': ['yaman', 'khamaaj'],
        'recommended_instruments': {
            'primary': ['sitar', 'guitar', 'violin'],
            'secondary': ['tabla', 'drums', 'bass', 'keyboards'],
        },
        'arrangement_style': 'film_orchestral',
        'mixing_preset': 'film_polished',
        'tempo_adaptation': 'moderate',
        'vocal_treatment': 'featured_lead',
        'energy_progression': [0.4, 0.6, 0.9, 1.0],
    },
    
    'rock_metal': {
        'display_name': 'Rock / Metal',
        'recommended_ragas': ['bhairav'],  # Angular, aggressive
        'recommended_instruments': {
            'primary': ['electric_guitar', 'drums', 'bass'],
            'secondary': ['sitar_heavy', 'synthesizer'],
        },
        'arrangement_style': 'western_rock',
        'mixing_preset': 'rock_compressed',
        'tempo_adaptation': 'fast',
        'vocal_treatment': 'powerful_distorted',
        'energy_progression': [0.2, 0.5, 0.8, 1.0],
    },
    
    'jazz_fusion': {
        'display_name': 'Jazz / Jazz Fusion',
        'recommended_ragas': ['yaman', 'bhairav'],
        'recommended_instruments': {
            'primary': ['saxophone', 'piano', 'bass'],
            'secondary': ['sitar', 'tabla', 'drums'],
        },
        'arrangement_style': 'jazz_improvisational',
        'mixing_preset': 'jazz_organic',
        'tempo_adaptation': 'swung_syncopated',
        'vocal_treatment': 'jazz_phrasing',
    },
    
    'edm_electronic': {
        'display_name': 'EDM / Electronic',
        'recommended_ragas': ['yaman', 'khamaaj'],
        'recommended_instruments': {
            'primary': ['synthesizer', 'drums', 'bass'],
            'secondary': ['sitar_synth', 'tabla_electronic'],
        },
        'arrangement_style': 'beat_driven_electronic',
        'mixing_preset': 'edm_compressed',
        'tempo_adaptation': 'fast_quantized',
        'vocal_treatment': 'processed_electronic',
        'energy_progression': [0.2, 0.4, 0.8, 1.0],
    },
    
    'acoustic_folk': {
        'display_name': 'Acoustic / Folk',
        'recommended_ragas': ['khamaaj', 'yaman'],
        'recommended_instruments': {
            'primary': ['acoustic_guitar', 'bansuri'],
            'secondary': ['harmonium', 'tabla'],
        },
        'arrangement_style': 'organic_acoustic',
        'mixing_preset': 'acoustic_natural',
        'tempo_adaptation': 'minimal',
        'vocal_treatment': 'intimate_natural',
    },
    
    'ambient_chillout': {
        'display_name': 'Ambient / Chillout',
        'recommended_ragas': ['yaman'],
        'recommended_instruments': {
            'primary': ['sitar', 'harmonium', 'pad_synth'],
            'secondary': ['tabla_light', 'bansuri'],
        },
        'arrangement_style': 'ambient_spacious',
        'mixing_preset': 'ambient_reverb_heavy',
        'tempo_adaptation': 'slow',
        'vocal_treatment': 'ethereal_padded',
        'energy_progression': [0.1, 0.3, 0.5, 0.6],
    },
}

# Processing Mode Configurations
PROCESSING_MODES = {
    'remove_instruments_only': {
        'description': 'Keep original vocals, replace instruments',
        'removes': ['drums', 'guitar', 'bass', 'piano', 'strings', 'wind'],
        'preserves': ['vocals'],
        'typical_use': 'Karaoke-style covers with new arrangement',
        'output_quality_factor': 0.9,
    },
    
    'remove_vocals_only': {
        'description': 'Keep instrumental, remove vocals',
        'removes': ['vocals'],
        'preserves': ['drums', 'guitar', 'bass', 'all_instruments'],
        'typical_use': 'Instrumental versions, backing tracks',
        'output_quality_factor': 0.85,
    },
    
    'full_remix': {
        'description': 'Process entire song - extract, reharmonize, rebuild',
        'removes': ['everything'],
        'preserves': ['melody_concept'],
        'typical_use': 'Complete stylistic transformation',
        'output_quality_factor': 0.8,  # Most complex
    },
}