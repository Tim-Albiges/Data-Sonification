"""
Data Sonification Logic (Spatial).

This module translates raw data arrays into musical parameters and 
spatial coordinates for the audio engine.
"""

import numpy as np
from typing import List, Tuple
from .utils import scale_data, midi_to_freq


class DataSonifier:
    """
    Handles the mapping of N-dimensional data to audio parameters.
    """

    def __init__(self, engine):
        self.engine = engine

    def sonify_2d(self, x_data: np.ndarray, y_data: np.ndarray, duration: float) -> List[Tuple]:
        """
        Sonify 2D data (X, Y) -> (Time, Pitch).
        Position defaults to (0,0,0).
        """
        times = scale_data(x_data, 0, duration)
        notes = scale_data(y_data, 48, 84).astype(int)

        sequence = []
        for t, n in zip(times, notes):
            freq = midi_to_freq(n)
            # Tuple: (Freq, Start, Dur, Cutoff, X, Y, Z)
            sequence.append((freq, t, 0.2, None, 0, 0, 0))

        return sequence

    def sonify_3d(
        self, 
        x_data: np.ndarray, 
        y_data: np.ndarray, 
        z_data: np.ndarray, 
        duration: float
    ) -> List[Tuple]:
        """
        Sonify 3D data (X, Y, Z) -> (Time, Pitch, Timbre + Spatial Position).
        
        Mappings:
        - Data X -> Time AND Spatial Left/Right
        - Data Y -> Pitch AND Spatial Front/Back
        - Data Z -> Brightness AND Spatial Up/Down
        """
        # Musical Parameters
        times = scale_data(x_data, 0, duration)
        notes = scale_data(y_data, 48, 72).astype(int)
        cutoffs = scale_data(z_data, 500, 8000)

        # Spatial Coordinates (Simulated 20x20x10m room)
        # X: -10 (Left) to +10 (Right)
        s_x = scale_data(x_data, -10, 10)
        # Y: 0 (At listener) to 20 (Far forward)
        s_y = scale_data(y_data, 0, 20)
        # Z: -5 (Below) to 5 (Above)
        s_z = scale_data(z_data, -5, 5)

        sequence = []
        for i in range(len(times)):
            freq = midi_to_freq(notes[i])
            t = times[i]
            c = cutoffs[i]
            pos = (s_x[i], s_y[i], s_z[i])
            
            # (Freq, Start, Dur, Cutoff, PosX, PosY, PosZ)
            sequence.append((freq, t, 0.3, c, *pos))

        return sequence