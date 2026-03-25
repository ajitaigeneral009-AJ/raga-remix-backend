"""
Complete Raga Music Database for RAG/LLM System
Contains comprehensive information about ragas, instruments, and fusion styles
"""

# ============================================================================
# RAGAS - Indian Classical Music Scales
# ============================================================================

RAGAS = {
    'yaman': {
        'name': 'Yaman (Kalyan)',
        'notes': ['Sa', 'Re', 'Ga', 'Ma#', 'Pa', 'Dha', 'Ni'],
        'time': 'Evening (7 PM - 10 PM)',
        'mood': 'Peaceful, devotional, romantic',
        'arohana': 'Ni Re Ga Ma# Dha Ni Sa',
        'avarohana': 'Sa Ni Dha Pa Ma# Ga Re Sa',
        'pakad': 'Ni Re Ga, Ma# Pa, Ni Dha Pa',
        'vadi': 'Ga',
        'samvadi': 'Ni',
        'description': 'One of the most popular ragas in Hindustani classical music. Yaman uses all natural notes except Ma which is sharp (tivra). Known for creating peaceful and devotional atmosphere. Ideal for evening concerts and bhajans.',
        'scale': 'major'
    },
    
    'bhairav': {
        'name': 'Bhairav',
        'notes': ['Sa', 'Re♭', 'Ga', 'Ma', 'Pa', 'Dha♭', 'Ni'],
        'time': 'Early morning (6 AM - 9 AM)',
        'mood': 'Serious, intense, meditative',
        'arohana': 'Sa Re♭ Ga Ma Pa Dha♭ Ni Sa',
        'avarohana': 'Sa Ni Dha♭ Pa Ma Ga Re♭ Sa',
        'pakad': 'Re♭ Sa, Ma Ga Ma Dha♭ Pa',
        'vadi': 'Dha♭',
        'samvadi': 'Re♭',
        'description': 'An ancient and austere morning raga. Uses flat Re and Dha (komal). Creates a solemn, serious atmosphere. Associated with Lord Shiva. Excellent for meditation and spiritual practices.',
        'scale': 'phrygian'
    },
    
    'bihag': {
        'name': 'Bihag',
        'notes': ['Sa', 'Re', 'Ga', 'Ma', 'Pa', 'Dha', 'Ni'],
        'time': 'Late evening (9 PM - 12 AM)',
        'mood': 'Romantic, playful, light',
        'arohana': 'Sa Ga Ma Dha Ni Re Sa',
        'avarohana': 'Sa Ni Dha Pa Ma Ga Re Sa',
        'pakad': 'Ga Ma Dha Ni, Ni Sa Re Ga',
        'vadi': 'Ga',
        'samvadi': 'Ni',
        'description': 'A light and romantic late evening raga. Uses all natural notes (shuddha). Popular in light classical and semi-classical music. Creates joyful and romantic mood.',
        'scale': 'major'
    },
    
    'bhupali': {
        'name': 'Bhupali (Bhoop)',
        'notes': ['Sa', 'Re', 'Ga', 'Pa', 'Dha'],
        'time': 'Early evening (6 PM - 9 PM)',
        'mood': 'Peaceful, meditative, serene',
        'arohana': 'Sa Re Ga Pa Dha Sa',
        'avarohana': 'Sa Dha Pa Ga Re Sa',
        'pakad': 'Sa Ga Pa, Dha Pa Ga Re',
        'vadi': 'Ga',
        'samvadi': 'Dha',
        'description': 'A pentatonic raga (5 notes). Omits Ma and Ni. Very popular and easy to recognize. Creates peaceful, serene atmosphere. Widely used in light music and film songs.',
        'scale': 'pentatonic'
    },
    
    'desh': {
        'name': 'Desh',
        'notes': ['Sa', 'Re', 'Ga', 'Ma', 'Pa', 'Dha', 'Ni♭'],
        'time': 'Late night (12 AM - 3 AM)',
        'mood': 'Patriotic, devotional, serene',
        'arohana': 'Sa Re Ma Pa Ni♭ Sa',
        'avarohana': 'Sa Ni♭ Dha Pa Ma Ga Re Sa',
        'pakad': 'Ma Pa Ni♭ Dha Pa, Ga Ma Re',
        'vadi': 'Re',
        'samvadi': 'Pa',
        'description': 'Associated with monsoon season and patriotic sentiment. Uses flat Ni (komal). Famous for patriotic songs and rain songs. Creates longing and devotional mood.',
        'scale': 'mixolydian'
    },
    
    'bageshri': {
        'name': 'Bageshri',
        'notes': ['Sa', 'Re', 'Ga♭', 'Ma', 'Pa', 'Dha', 'Ni♭'],
        'time': 'Late night (12 AM - 3 AM)',
        'mood': 'Romantic, longing, tender',
        'arohana': 'Sa Ga♭ Ma Dha Ni♭ Sa',
        'avarohana': 'Sa Ni♭ Dha Pa Ma Ga♭ Re Sa',
        'pakad': 'Ma Dha Ni♭, Dha Ma Ga♭ Re',
        'vadi': 'Ma',
        'samvadi': 'Sa',
        'description': 'A deeply romantic and tender night raga. Uses flat Ga and Ni (komal). Creates longing and peaceful atmosphere. Very popular in semi-classical forms.',
        'scale': 'minor'
    },
    
    'kafi': {
        'name': 'Kafi',
        'notes': ['Sa', 'Re', 'Ga♭', 'Ma', 'Pa', 'Dha', 'Ni♭'],
        'time': 'Night (9 PM - 12 AM)',
        'mood': 'Light, devotional, folk-like',
        'arohana': 'Sa Re Ga♭ Ma Pa Dha Ni♭ Sa',
        'avarohana': 'Sa Ni♭ Dha Pa Ma Ga♭ Re Sa',
        'pakad': 'Ga♭ Ma Pa Dha Pa, Ma Ga♭ Re Sa',
        'vadi': 'Pa',
        'samvadi': 'Sa',
        'description': 'One of the most versatile ragas. Used extensively in folk, semi-classical, and film music. Both Ga and Ni can be flat or natural. Creates light, devotional mood.',
        'scale': 'dorian'
    },
    
    'durga': {
        'name': 'Durga',
        'notes': ['Sa', 'Re', 'Ma', 'Pa', 'Dha'],
        'time': 'Late evening (9 PM - 12 AM)',
        'mood': 'Devotional, powerful, majestic',
        'arohana': 'Sa Re Ma Pa Dha Sa',
        'avarohana': 'Sa Dha Pa Ma Re Sa',
        'pakad': 'Re Ma Pa, Dha Pa Ma Re',
        'vadi': 'Ma',
        'samvadi': 'Sa',
        'description': 'A pentatonic raga. Omits Ga and Ni. Associated with Goddess Durga. Creates powerful and majestic atmosphere. Used in devotional music.',
        'scale': 'pentatonic'
    },
    
    'marwa': {
        'name': 'Marwa',
        'notes': ['Sa', 'Re♭', 'Ga', 'Ma#', 'Dha', 'Ni'],
        'time': 'Late afternoon (4 PM - 7 PM)',
        'mood': 'Serious, intense, contemplative',
        'arohana': 'Re♭ Ga Ma# Dha Ni Sa',
        'avarohana': 'Sa Ni Dha Ma# Ga Re♭ (omit Pa)',
        'pakad': 'Re♭ Ga Ma# Dha, Ni Dha Ma# Ga',
        'vadi': 'Dha',
        'samvadi': 'Re♭',
        'description': 'A complex afternoon raga. Uses flat Re and sharp Ma. Omits Pa. Creates intense and contemplative mood. Requires expertise to perform.',
        'scale': 'altered'
    },
    
    'todi': {
        'name': 'Todi (Miyan ki Todi)',
        'notes': ['Sa', 'Re♭', 'Ga♭', 'Ma#', 'Pa', 'Dha♭', 'Ni'],
        'time': 'Late morning (10 AM - 1 PM)',
        'mood': 'Serious, devotional, pathetic',
        'arohana': 'Sa Re♭ Ga♭ Ma# Pa Dha♭ Ni Sa',
        'avarohana': 'Sa Ni Dha♭ Pa Ma# Ga♭ Re♭ Sa',
        'pakad': 'Ga♭ Ma# Pa, Dha♭ Ni Dha♭ Pa',
        'vadi': 'Dha♭',
        'samvadi': 'Ga♭',
        'description': 'One of the most profound ragas in Hindustani music. Uses flat Re, Ga, Dha and sharp Ma. Creates deep emotional and devotional atmosphere. Named after legendary Miyan Tansen.',
        'scale': 'phrygian_dominant'
    }
}

# ============================================================================
# INSTRUMENTS - Detailed Properties
# ============================================================================

INSTRUMENTS = {
    # ===== INDIAN STRING INSTRUMENTS =====
    'sitar': {
        'name': 'Sitar',
        'category': 'string',
        'frequency_range': (100, 8000),
        'characteristic_timbre': 'Bright, resonant with sympathetic strings',
        'attack_type': 'Plucked with mezrab',
        'sustain_capability': 'High with chikari strings',
        'fusion_suitability': 0.9,
        'description': 'Primary melodic instrument in Hindustani classical music. Features movable frets and sympathetic strings for rich harmonic texture.'
    },
    
    'sarod': {
        'name': 'Sarod',
        'category': 'string',
        'frequency_range': (80, 6000),
        'characteristic_timbre': 'Deep, mellow, resonant',
        'attack_type': 'Plucked with plectrum',
        'sustain_capability': 'High',
        'fusion_suitability': 0.85,
        'description': 'Fretless string instrument with metallic timbre. Known for smooth meend (glides) and deep bass resonance.'
    },
    
    'veena': {
        'name': 'Veena',
        'category': 'string',
        'frequency_range': (60, 4000),
        'characteristic_timbre': 'Warm, resonant, sustained',
        'attack_type': 'Plucked with fingers',
        'sustain_capability': 'Very high',
        'fusion_suitability': 0.8,
        'description': 'Ancient South Indian string instrument. Produces warm, sustained tones. Essential in Carnatic classical music.'
    },
    
    'sarangi': {
        'name': 'Sarangi',
        'category': 'string',
        'frequency_range': (100, 5000),
        'characteristic_timbre': 'Vocal-like, emotional',
        'attack_type': 'Bowed',
        'sustain_capability': 'Very high',
        'fusion_suitability': 0.75,
        'description': 'Bowed instrument that closely mimics human voice. Highly expressive. Used in classical and folk music.'
    },
    
    # ===== INDIAN PERCUSSION =====
    'tabla': {
        'name': 'Tabla',
        'category': 'percussion',
        'frequency_range': (80, 10000),
        'characteristic_timbre': 'Sharp, resonant with varied tones',
        'attack_type': 'Hand percussion',
        'sustain_capability': 'Low to medium',
        'fusion_suitability': 0.95,
        'description': 'Twin-drum percussion instrument. Extremely versatile with complex rhythmic vocabulary. Essential in Hindustani music and fusion.'
    },
    
    'mridangam': {
        'name': 'Mridangam',
        'category': 'percussion',
        'frequency_range': (60, 8000),
        'characteristic_timbre': 'Deep bass with sharp treble',
        'attack_type': 'Hand percussion',
        'sustain_capability': 'Medium',
        'fusion_suitability': 0.85,
        'description': 'Primary percussion in Carnatic music. Barrel-shaped drum with complex tonal capabilities. Produces both bass and treble sounds.'
    },
    
    # ===== WIND INSTRUMENTS =====
    'bansuri': {
        'name': 'Bansuri',
        'category': 'wind',
        'frequency_range': (200, 8000),
        'characteristic_timbre': 'Soft, breathy, flute-like',
        'attack_type': 'Blown',
        'sustain_capability': 'High',
        'fusion_suitability': 0.9,
        'description': 'Indian bamboo flute. Produces soft, meditative tones. Popular in devotional and classical music.'
    },
    
    'shehnai': {
        'name': 'Shehnai',
        'category': 'wind',
        'frequency_range': (300, 6000),
        'characteristic_timbre': 'Bright, auspicious, reedy',
        'attack_type': 'Double-reed',
        'sustain_capability': 'High',
        'fusion_suitability': 0.7,
        'description': 'Double-reed instrument traditionally played at weddings and ceremonies. Bright, penetrating tone.'
    },
    
    'flute': {
        'name': 'Flute',
        'category': 'wind',
        'frequency_range': (250, 8000),
        'characteristic_timbre': 'Clear, bright, pure',
        'attack_type': 'Blown',
        'sustain_capability': 'High',
        'fusion_suitability': 0.95,
        'description': 'Western concert flute. Clear, bright tone. Highly versatile in fusion settings.'
    },
    
    # ===== KEYBOARD =====
    'harmonium': {
        'name': 'Harmonium',
        'category': 'keyboard',
        'frequency_range': (100, 4000),
        'characteristic_timbre': 'Warm, sustained, organ-like',
        'attack_type': 'Keyboard + bellows',
        'sustain_capability': 'Very high',
        'fusion_suitability': 0.8,
        'description': 'Portable reed organ. Provides harmonic support in Indian classical and devotional music.'
    },
    
    'piano': {
        'name': 'Piano',
        'category': 'keyboard',
        'frequency_range': (27, 4200),
        'characteristic_timbre': 'Rich, resonant, percussive',
        'attack_type': 'Hammered strings',
        'sustain_capability': 'High',
        'fusion_suitability': 0.95,
        'description': 'Grand or upright piano. Full-range keyboard instrument. Essential in jazz, classical, and fusion.'
    },
    
    'keyboard': {
        'name': 'Electronic Keyboard',
        'category': 'electronic',
        'frequency_range': (20, 20000),
        'characteristic_timbre': 'Versatile, programmable',
        'attack_type': 'Electronic',
        'sustain_capability': 'Infinite',
        'fusion_suitability': 1.0,
        'description': 'Electronic synthesizer keyboard. Can emulate any instrument. Essential in modern fusion and production.'
    },
    
    # ===== WESTERN STRING =====
    'guitar': {
        'name': 'Guitar',
        'category': 'string',
        'frequency_range': (82, 5000),
        'characteristic_timbre': 'Bright to warm, versatile',
        'attack_type': 'Plucked or strummed',
        'sustain_capability': 'Medium',
        'fusion_suitability': 1.0,
        'description': 'Acoustic or electric guitar. Extremely versatile. Essential in fusion, rock, jazz, and pop.'
    },
    
    'violin': {
        'name': 'Violin',
        'category': 'string',
        'frequency_range': (196, 10000),
        'characteristic_timbre': 'Bright, expressive, vocal',
        'attack_type': 'Bowed',
        'sustain_capability': 'Very high',
        'fusion_suitability': 0.95,
        'description': 'Used in both Carnatic and Western classical. Highly expressive. Excellent for fusion.'
    },
    
    'cello': {
        'name': 'Cello',
        'category': 'string',
        'frequency_range': (65, 1500),
        'characteristic_timbre': 'Deep, warm, resonant',
        'attack_type': 'Bowed',
        'sustain_capability': 'Very high',
        'fusion_suitability': 0.9,
        'description': 'Deep-voiced string instrument. Provides bass and melodic support. Popular in fusion arrangements.'
    },
    
    # ===== WESTERN PERCUSSION =====
    'drums': {
        'name': 'Drum Kit',
        'category': 'percussion',
        'frequency_range': (40, 15000),
        'characteristic_timbre': 'Varied: bass, snare, cymbals',
        'attack_type': 'Struck with sticks/hands',
        'sustain_capability': 'Low to high',
        'fusion_suitability': 1.0,
        'description': 'Standard Western drum set. Essential rhythm section instrument in fusion, rock, jazz, and pop.'
    },
    
    # ===== BRASS =====
    'saxophone': {
        'name': 'Saxophone',
        'category': 'wind',
        'frequency_range': (100, 8000),
        'characteristic_timbre': 'Smooth, jazzy, expressive',
        'attack_type': 'Single-reed',
        'sustain_capability': 'High',
        'fusion_suitability': 0.9,
        'description': 'Jazz and fusion staple. Smooth, expressive tone. Blends well with Indian instruments.'
    },
    
    'trumpet': {
        'name': 'Trumpet',
        'category': 'wind',
        'frequency_range': (165, 4200),
        'characteristic_timbre': 'Bright, powerful, piercing',
        'attack_type': 'Brass',
        'sustain_capability': 'Medium',
        'fusion_suitability': 0.85,
        'description': 'Bright brass instrument. Powerful in orchestral and jazz settings. Effective in fusion.'
    },
    
    # ===== ELECTRONIC =====
    'synth_pad': {
        'name': 'Synthesizer Pad',
        'category': 'electronic',
        'frequency_range': (20, 20000),
        'characteristic_timbre': 'Ambient, atmospheric, sustained',
        'attack_type': 'Electronic',
        'sustain_capability': 'Infinite',
        'fusion_suitability': 1.0,
        'description': 'Ambient synthesizer textures. Creates atmospheric backgrounds. Essential in electronic fusion.'
    },
    
    'bass': {
        'name': 'Bass Guitar',
        'category': 'string',
        'frequency_range': (40, 400),
        'characteristic_timbre': 'Deep, punchy, rhythmic',
        'attack_type': 'Plucked',
        'sustain_capability': 'Medium',
        'fusion_suitability': 1.0,
        'description': 'Electric or acoustic bass. Provides rhythmic and harmonic foundation. Essential in fusion.'
    }
}

# ============================================================================
# INSTRUMENT COMPATIBILITY - Numerical Scores (0.0 - 1.0)
# ============================================================================

INSTRUMENT_COMPATIBILITY = {
    'sitar': {
        'tabla': 1.0,
        'harmonium': 0.9,
        'bansuri': 0.85,
        'violin': 0.8,
        'sarangi': 0.75,
        'guitar': 0.7,
        'flute': 0.85,
        'keyboard': 0.8,
        'drums': 0.6,
        'saxophone': 0.65
    },
    'tabla': {
        'sitar': 1.0,
        'sarod': 1.0,
        'bansuri': 0.95,
        'harmonium': 0.9,
        'violin': 0.9,
        'sarangi': 0.85,
        'drums': 0.7,
        'guitar': 0.75
    },
    'bansuri': {
        'tabla': 0.95,
        'sitar': 0.85,
        'harmonium': 0.9,
        'violin': 0.85,
        'sarangi': 0.8,
        'guitar': 0.8,
        'keyboard': 0.85,
        'flute': 0.9
    },
    'guitar': {
        'drums': 1.0,
        'bass': 1.0,
        'keyboard': 0.95,
        'piano': 0.9,
        'violin': 0.85,
        'saxophone': 0.9,
        'flute': 0.85,
        'sitar': 0.7,
        'tabla': 0.75
    },
    'drums': {
        'guitar': 1.0,
        'bass': 1.0,
        'keyboard': 0.95,
        'piano': 0.9,
        'saxophone': 0.9,
        'trumpet': 0.85,
        'sitar': 0.6,
        'tabla': 0.7
    },
    'violin': {
        'tabla': 0.9,
        'sitar': 0.8,
        'harmonium': 0.85,
        'bansuri': 0.85,
        'piano': 0.9,
        'cello': 0.95,
        'guitar': 0.85
    },
    'saxophone': {
        'drums': 0.9,
        'guitar': 0.9,
        'bass': 0.85,
        'piano': 0.9,
        'trumpet': 0.85,
        'sitar': 0.65,
        'tabla': 0.7
    },
    'keyboard': {
        'drums': 0.95,
        'guitar': 0.95,
        'bass': 0.9,
        'saxophone': 0.85,
        'sitar': 0.8,
        'tabla': 0.75,
        'bansuri': 0.85,
        'violin': 0.9
    },
    'harmonium': {
        'tabla': 0.9,
        'sitar': 0.9,
        'sarod': 0.85,
        'bansuri': 0.9,
        'violin': 0.85,
        'sarangi': 0.8
    },
    'piano': {
        'violin': 0.9,
        'cello': 0.9,
        'guitar': 0.9,
        'drums': 0.9,
        'saxophone': 0.9,
        'trumpet': 0.85,
        'sitar': 0.75
    }
}

# ============================================================================
# FUSION STYLES - Complete Definitions
# ============================================================================

FUSION_STYLES = {
    'indo_western_fusion': {
        'name': 'Indo-Western Fusion',
        'description': 'Blend of Indian classical elements with Western harmony and rhythm. Perfect balance of East and West.',
        'primary_instruments': {
            'indian': ['sitar', 'tabla', 'bansuri'],
            'western': ['guitar', 'drums', 'keyboard'],
            'electronic': []
        },
        'base_ragas': ['yaman', 'bihag', 'kafi'],
        'tempo_adjustment_range': (0.8, 1.3),
        'energy_progression': [0.3, 0.5, 0.8, 1.0],
        'characteristic_features': ['Raga-based melodies', 'Western chord progressions', 'Hybrid rhythm patterns'],
        'arrangement_pattern': 'Verse-Chorus with Alap-Jor-Jhala influences',
        'mixing_style': 'Equal emphasis on Indian and Western elements'
    },
    
    'indo_jazz': {
        'name': 'Indo-Jazz',
        'description': 'Sophisticated fusion of Indian ragas with jazz improvisation and harmony. Intellectual and expressive.',
        'primary_instruments': {
            'indian': ['sitar', 'tabla', 'sarod'],
            'western': ['saxophone', 'piano', 'drums'],
            'electronic': []
        },
        'base_ragas': ['yaman', 'bhupali', 'desh'],
        'tempo_adjustment_range': (0.9, 1.2),
        'energy_progression': [0.4, 0.6, 0.8, 0.9],
        'characteristic_features': ['Modal jazz harmony', 'Complex time signatures', 'Extended improvisations'],
        'arrangement_pattern': 'Jazz structure with raga development',
        'mixing_style': 'Subtle blend with space for improvisation'
    },
    
    'edm_indian': {
        'name': 'EDM-Indian',
        'description': 'High-energy electronic dance music with Indian classical and folk elements. Perfect for dance floors.',
        'primary_instruments': {
            'indian': ['tabla', 'bansuri', 'sitar'],
            'western': [],
            'electronic': ['synth_pad', 'keyboard', 'drums']
        },
        'base_ragas': ['bhupali', 'durga', 'kafi'],
        'tempo_adjustment_range': (1.1, 1.5),
        'energy_progression': [0.5, 0.7, 0.9, 1.0],
        'characteristic_features': ['Heavy bass', 'Four-on-the-floor beat', 'Indian melodic hooks'],
        'arrangement_pattern': 'EDM structure (Intro-Build-Drop) with Indian samples',
        'mixing_style': 'Electronic dominance with Indian flavors'
    },
    
    'classical_crossover': {
        'name': 'Classical Crossover',
        'description': 'Fusion of Indian and Western classical traditions. Orchestral arrangements with Indian elements.',
        'primary_instruments': {
            'indian': ['sitar', 'sarod', 'tabla'],
            'western': ['violin', 'cello', 'piano'],
            'electronic': []
        },
        'base_ragas': ['yaman', 'todi', 'marwa'],
        'tempo_adjustment_range': (0.7, 1.1),
        'energy_progression': [0.3, 0.5, 0.7, 0.9],
        'characteristic_features': ['Orchestral arrangements', 'Classical forms', 'Sophisticated harmony'],
        'arrangement_pattern': 'Symphonic structure with raga development',
        'mixing_style': 'Balanced orchestral blend'
    },
    
    'sufi_rock': {
        'name': 'Sufi Rock',
        'description': 'Powerful fusion of Sufi devotional music with rock energy. Spiritual and energetic.',
        'primary_instruments': {
            'indian': ['harmonium', 'tabla', 'sarangi'],
            'western': ['guitar', 'drums', 'bass'],
            'electronic': []
        },
        'base_ragas': ['kafi', 'bhairavi', 'desh'],
        'tempo_adjustment_range': (0.9, 1.4),
        'energy_progression': [0.4, 0.6, 0.9, 1.0],
        'characteristic_features': ['Powerful vocals', 'Distorted guitars', 'Devotional lyrics'],
        'arrangement_pattern': 'Rock structure with Sufi devotional themes',
        'mixing_style': 'Rock power with Sufi spirituality'
    },
    
    'ambient_indian': {
        'name': 'Ambient Indian',
        'description': 'Meditative and atmospheric fusion. Perfect for relaxation, yoga, and meditation.',
        'primary_instruments': {
            'indian': ['bansuri', 'sitar', 'sarangi'],
            'western': [],
            'electronic': ['synth_pad', 'keyboard']
        },
        'base_ragas': ['bhupali', 'yaman', 'bageshri'],
        'tempo_adjustment_range': (0.5, 0.8),
        'energy_progression': [0.2, 0.3, 0.4, 0.5],
        'characteristic_features': ['Slow tempo', 'Atmospheric textures', 'Meditative mood'],
        'arrangement_pattern': 'Free-flowing with minimal structure',
        'mixing_style': 'Spacious with reverb and delay'
    },
    
    'bollywood_fusion': {
        'name': 'Bollywood Fusion',
        'description': 'Modern Bollywood style with diverse influences. Catchy and commercial.',
        'primary_instruments': {
            'indian': ['tabla', 'harmonium', 'bansuri'],
            'western': ['guitar', 'drums', 'bass'],
            'electronic': ['keyboard', 'synth_pad']
        },
        'base_ragas': ['kafi', 'bhupali', 'desh'],
        'tempo_adjustment_range': (0.9, 1.3),
        'energy_progression': [0.4, 0.6, 0.8, 1.0],
        'characteristic_features': ['Catchy melodies', 'Dance rhythms', 'Orchestral sections'],
        'arrangement_pattern': 'Verse-Chorus-Bridge with interludes',
        'mixing_style': 'Polished and commercial'
    },
    
    'carnatic_contemporary': {
        'name': 'Carnatic Contemporary',
        'description': 'South Indian classical music meets modern production. Traditional meets innovation.',
        'primary_instruments': {
            'indian': ['veena', 'mridangam', 'violin'],
            'western': ['keyboard', 'bass'],
            'electronic': ['synth_pad']
        },
        'base_ragas': ['kalyani', 'sankarabharanam', 'mohanam'],
        'tempo_adjustment_range': (0.8, 1.2),
        'energy_progression': [0.3, 0.5, 0.8, 1.0],
        'characteristic_features': ['Complex rhythms', 'Gamaka-heavy vocals', 'Kriti structures'],
        'arrangement_pattern': 'Carnatic structure with modern production',
        'mixing_style': 'Traditional sound with modern clarity'
    },
    
    'world_beat': {
        'name': 'World Beat',
        'description': 'Global fusion incorporating Indian, African, Latin, and Western elements.',
        'primary_instruments': {
            'indian': ['tabla', 'sitar', 'bansuri'],
            'western': ['guitar', 'drums', 'bass', 'percussion'],
            'electronic': ['keyboard']
        },
        'base_ragas': ['bhupali', 'desh', 'kafi'],
        'tempo_adjustment_range': (0.9, 1.4),
        'energy_progression': [0.4, 0.6, 0.8, 1.0],
        'characteristic_features': ['Polyrhythms', 'Global instrumentation', 'Diverse influences'],
        'arrangement_pattern': 'Verse-Chorus with extended instrumental sections',
        'mixing_style': 'Colorful and dynamic'
    },
    
    'acoustic_folk_fusion': {
        'name': 'Acoustic Folk Fusion',
        'description': 'Organic blend of Indian folk with acoustic Western instruments. Warm and earthy.',
        'primary_instruments': {
            'indian': ['bansuri', 'harmonium', 'tabla'],
            'western': ['guitar', 'violin', 'cello'],
            'electronic': []
        },
        'base_ragas': ['kafi', 'bhairavi', 'desh'],
        'tempo_adjustment_range': (0.8, 1.2),
        'energy_progression': [0.3, 0.5, 0.7, 0.9],
        'characteristic_features': ['Acoustic instruments', 'Folk melodies', 'Storytelling'],
        'arrangement_pattern': 'Folk song structure with instrumental breaks',
        'mixing_style': 'Natural and organic'
    }
}
