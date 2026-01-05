# Dictionary containing harmonic weights (timbre) and ADSR envelopes.

PRESETS = {
    'piano': {
        'harmonics': [1.0, 0.5, 0.2, 0.1],
        'v_rate': 0.0,
        'v_width': 0.0,
        'adsr': {'attack': 0.01, 'decay': 0.1, 'sustain': 0.6, 'release': 0.4}
    },
    'violin': {
        'harmonics': [1.0, 0.8, 0.7, 0.6, 0.5, 0.4],
        'v_rate': 5.0,  # 5Hz Vibrato
        'v_width': 2.0, # Depth
        'adsr': {'attack': 0.2, 'decay': 0.1, 'sustain': 0.8, 'release': 0.3}
    },
    'cello': {
        'harmonics': [1.0, 0.8, 0.5, 0.3],
        'v_rate': 4.5,
        'v_width': 3.0,
        'adsr': {'attack': 0.15, 'decay': 0.1, 'sustain': 0.7, 'release': 0.4}
    },
    'flute': {
        'harmonics': [1.0, 0.0, 0.5, 0.0, 0.2], # Odd harmonics
        'v_rate': 6.0,
        'v_width': 1.5,
        'adsr': {'attack': 0.1, 'decay': 0.05, 'sustain': 0.9, 'release': 0.2}
    }
}