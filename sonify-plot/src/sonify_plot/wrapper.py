"""
Main Sonification Wrapper (Stereo/Spatial).

Integrates extraction and synthesis into a single user-friendly function.
"""

import numpy as np
from typing import Any, Tuple
from sonify_synth import AudioEngine, DataSonifier, PRESETS
from .extract import get_xyz_data


def sonify(
    data: Any,
    mode: str = '2d',
    instrument: str = 'piano',
    duration: float = 5.0,
    sample_rate: int = 44100,
    listener_pos: Tuple[float, float, float] = (0, 0, 0),
    **kwargs
) -> np.ndarray:
    """
    Convert data object to stereo spatial audio.

    Args:
        data: Input data (Plot, DataFrame, etc.).
        mode: '2d' or '3d'.
        instrument: 'piano', 'violin', 'cello', 'flute'.
        duration: Audio length in seconds.
        sample_rate: Default 44100.
        listener_pos: (x, y, z) coordinates of the user.
        **kwargs: Extraction arguments.

    Returns:
        np.ndarray: Stereo audio buffer (2 x Samples).
    """
    if instrument not in PRESETS:
        raise ValueError(f"Unknown instrument '{instrument}'.")

    if mode not in ['2d', '3d']:
        raise ValueError("Mode must be '2d' or '3d'.")

    # Extract
    x, y, z = get_xyz_data(data, **kwargs)

    # Setup Engine
    engine = AudioEngine(sample_rate=sample_rate)
    sonifier = DataSonifier(engine)
    inst_params = PRESETS[instrument]

    # Map Data
    if mode == '2d':
        sequence = sonifier.sonify_2d(x, y, duration)
    else:
        if z is None:
            z = np.zeros_like(x)
        sequence = sonifier.sonify_3d(x, y, z, duration)

    # Render
    audio = engine.render(
        sequence, 
        inst_params, 
        total_duration=duration + 1.0, 
        listener_pos=listener_pos
    )

    return audio


def play(audio: np.ndarray, sample_rate: int = 44100) -> None:
    """Play audio in Jupyter Notebook."""
    try:
        from IPython.display import Audio, display
        display(Audio(data=audio, rate=sample_rate))
    except ImportError:
        print("IPython not found.")