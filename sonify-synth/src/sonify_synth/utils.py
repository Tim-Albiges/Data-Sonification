"""
Utility functions for audio processing and mathematical conversions.

This module handles low-level operations such as frequency conversion,
data scaling/normalization, and WAV file export.
"""
import numpy as np
from scipy.io import wavfile

def midi_to_freq(note_number: int) -> float:
    """
    Convert a MIDI note number to its corresponding frequency in Hertz.

    Args:
        note_number (int): The MIDI note number (e.g., 69 for A4).

    Returns:
        float: The frequency of the note in Hz.
    """
    return 440.0 * 2**((note_number - 69) / 12)

def save_wav(filename: str, sample_rate: int, data: np.ndarray):
    """
    Save a NumPy audio array to a standard 16-bit PCM WAV file.

    This function automatically normalizes the audio to prevent clipping
    and converts floating-point data to 16-bit integers.

    Args:
        filename (str): The output file path (should end in .wav).
        sample_rate (int): The audio sample rate (e.g., 44100).
        data (np.ndarray): The 1D audio signal array.
    """
    # Normalize to prevent clipping (keep within -1.0 to 1.0)
    max_val = np.max(np.abs(data))
    if max_val > 0:
        data = data / max_val
    
    # Convert to 16-bit integer for standard WAV format
    audio_int16 = (data * 32767).astype(np.int16)
    wavfile.write(filename, sample_rate, audio_int16)

def scale_data(data: np.ndarray, out_min: float, out_max: float) -> np.ndarray:
    """
    Linearly scale an input array to a specific output range.

    Useful for mapping raw data dimensions to audio parameters
    (e.g., mapping temperature 0-100 to pitch 200Hz-800Hz).

    Args:
        data (np.ndarray): The input data array.
        out_min (float): The minimum value of the target range.
        out_max (float): The maximum value of the target range.

    Returns:
        np.ndarray: The scaled data array.
    """
    d_min, d_max = np.min(data), np.max(data)
    # Avoid division by zero if all data points are the same
    if d_max == d_min:
        return np.full_like(data, out_min)
    return out_min + (data - d_min) * (out_max - out_min) / (d_max - d_min)