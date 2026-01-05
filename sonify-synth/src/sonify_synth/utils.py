import numpy as np
from scipy.io import wavfile

def midi_to_freq(note_number: int) -> float:
    """Converts a MIDI note number to Frequency in Hz."""
    return 440.0 * 2**((note_number - 69) / 12)

def save_wav(filename: str, sample_rate: int, data: np.ndarray):
    """Saves a NumPy array as a WAV file (16-bit PCM)."""
    # Normalize to prevent clipping (keep within -1.0 to 1.0)
    max_val = np.max(np.abs(data))
    if max_val > 0:
        data = data / max_val
    
    # Convert to 16-bit integer for standard WAV format
    audio_int16 = (data * 32767).astype(np.int16)
    wavfile.write(filename, sample_rate, audio_int16)

def scale_data(data: np.ndarray, out_min: float, out_max: float) -> np.ndarray:
    """Linearly scales input data to a target range."""
    d_min, d_max = np.min(data), np.max(data)
    # Avoid division by zero if all data points are the same
    if d_max == d_min:
        return np.full_like(data, out_min)
    return out_min + (data - d_min) * (out_max - out_min) / (d_max - d_min)