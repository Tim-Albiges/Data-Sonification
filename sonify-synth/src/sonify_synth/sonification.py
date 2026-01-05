import numpy as np
from typing import List, Tuple
from .utils import scale_data, midi_to_freq

class DataSonifier:
    def __init__(self, engine):
        self.engine = engine

    def sonify_2d(self, x_data: np.ndarray, y_data: np.ndarray, duration: float) -> List[Tuple]:
        """
        Maps X -> Time
        Maps Y -> Pitch
        Returns a list of notes compatible with AudioEngine.render
        """
        # Map X to time (0 to duration)
        times = scale_data(x_data, 0, duration)
        
        # Map Y to MIDI notes (Range 48-84 is roughly C3 to C6)
        notes = scale_data(y_data, 48, 84).astype(int)
        
        sequence = []
        for t, n in zip(times, notes):
            freq = midi_to_freq(n)
            # Each data point is a short "blip" (0.2s)
            # Ideally, they overlap slightly to create a continuous stream
            sequence.append((freq, t, 0.2))
            
        return sequence

    def sonify_3d(self, x_data: np.ndarray, y_data: np.ndarray, z_data: np.ndarray, duration: float) -> List[Tuple]:
        """
        Maps X -> Time
        Maps Y -> Pitch
        Maps Z -> Filter Cutoff (Brightness)
        """
        times = scale_data(x_data, 0, duration)
        notes = scale_data(y_data, 48, 72).astype(int) # Lower range for bassier sounds
        
        # Map Z to Filter Cutoff (500Hz to 8000Hz)
        # Low Z = Muffled, High Z = Bright/Clear
        cutoffs = scale_data(z_data, 500, 8000)
        
        sequence = []
        for t, n, c in zip(times, notes, cutoffs):
            freq = midi_to_freq(n)
            # Note structure: (Freq, Start, Duration, Filter_Cutoff)
            sequence.append((freq, t, 0.3, c))
            
        return sequence