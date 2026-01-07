"""
Core Audio Synthesis Engine (Stereo/Spatial).

This module contains the AudioEngine class, responsible for generating
waveforms and positioning them in a 3D audio space relative to a listener.
"""

import numpy as np
from typing import Dict, List, Tuple, Optional


class AudioEngine:
    """
    A synthesizer engine for generating polyphonic, spatial audio.
    """

    def __init__(self, sample_rate: int = 44100):
        """
        Initialize the audio engine.

        Args:
            sample_rate (int): Samples per second (default 44100).
        """
        self.sample_rate = sample_rate

    def _generate_wave(self, freq: float, duration: float, params: Dict) -> np.ndarray:
        """
        Generate a raw mono waveform with harmonics and vibrato.

        Args:
            freq (float): Fundamental frequency in Hz.
            duration (float): Duration in seconds.
            params (Dict): Instrument parameter dictionary.

        Returns:
            np.ndarray: The raw generated 1D waveform.
        """
        t = np.linspace(0, duration, int(self.sample_rate * duration), endpoint=False)
        
        # Vibrato parameters
        v_rate = params.get('v_rate', 0)
        v_width = params.get('v_width', 0)

        if v_rate > 0:
            phase_shift = (v_width / v_rate) * np.sin(2 * np.pi * v_rate * t)
        else:
            phase_shift = 0

        wave = np.zeros_like(t)
        for i, weight in enumerate(params['harmonics']):
            harmonic_freq = freq * (i + 1)
            # Nyquist check
            if harmonic_freq < self.sample_rate / 2:
                wave += weight * np.sin(
                    2 * np.pi * harmonic_freq * t + (i + 1) * phase_shift
                )

        if np.max(np.abs(wave)) > 0:
            wave /= np.max(np.abs(wave))
            
        return wave

    def _apply_adsr(self, wave: np.ndarray, adsr: Dict) -> np.ndarray:
        """Apply Attack-Decay-Sustain-Release envelope."""
        total_len = len(wave)
        a_len = int(adsr['attack'] * self.sample_rate)
        d_len = int(adsr['decay'] * self.sample_rate)
        r_len = int(adsr['release'] * self.sample_rate)
        s_len = total_len - (a_len + d_len + r_len)

        if s_len < 0:
            s_len = 0
            remaining = total_len - a_len
            if remaining > 0:
                d_len = remaining // 2
                r_len = remaining - d_len
            else:
                d_len, r_len = 0, 0

        envelope = np.concatenate([
            np.linspace(0, 1, a_len),
            np.linspace(1, adsr['sustain'], d_len),
            np.full(s_len, adsr['sustain']),
            np.linspace(adsr['sustain'], 0, r_len)
        ])

        if len(envelope) < total_len:
            envelope = np.pad(envelope, (0, total_len - len(envelope)))
        
        return wave * envelope[:total_len]

    def _apply_lpf(self, audio: np.ndarray, cutoff: float) -> np.ndarray:
        """Apply simple Low Pass Filter."""
        rc = 1.0 / (2 * np.pi * cutoff + 1e-10)
        dt = 1.0 / self.sample_rate
        alpha = dt / (rc + dt)
        filtered = np.zeros_like(audio)
        prev = 0.0
        for i in range(len(audio)):
            filtered[i] = prev + alpha * (audio[i] - prev)
            prev = filtered[i]
        return filtered

    def _calculate_spatial_gains(
        self, 
        source_pos: Tuple[float, float, float], 
        listener_pos: Tuple[float, float, float]
    ) -> Tuple[float, float]:
        """
        Calculate stereo gains (Left, Right) based on 3D position.

        Uses Inverse Square Law for distance and trig panning for azimuth.
        Coordinates: X (Left/Right), Y (Back/Front), Z (Down/Up).

        Args:
            source_pos (tuple): (x, y, z) of the sound.
            listener_pos (tuple): (x, y, z) of the user.

        Returns:
            Tuple[float, float]: Gain for Left and Right channels.
        """
        sx, sy, sz = source_pos
        lx, ly, lz = listener_pos

        # Relative vector
        dx, dy, dz = sx - lx, sy - ly, sz - lz

        # 1. Distance Attenuation (Inverse Square Law)
        distance = np.sqrt(dx**2 + dy**2 + dz**2)
        # Adding 1.0 to denominator prevents division by zero at origin
        gain_dist = 1.0 / (1.0 + 0.5 * distance)

        # 2. Panning (Azimuth in X-Y plane)
        # angle 0 is Forward (Y+), angle pi/2 is Right (X+)
        angle = np.arctan2(dx, dy) 
        
        # Map angle to panning scalar (-1.0 Left to +1.0 Right)
        pan = np.sin(angle)
        
        # Constant Power Panning
        p_norm = (pan + 1) / 2
        gain_l = np.cos(p_norm * np.pi / 2) * gain_dist
        gain_r = np.sin(p_norm * np.pi / 2) * gain_dist

        return gain_l, gain_r

    def render(
        self, 
        note_sequence: List[Tuple], 
        instrument: Dict, 
        total_duration: float,
        listener_pos: Tuple[float, float, float] = (0, 0, 0)
    ) -> np.ndarray:
        """
        Render the sequence into a stereo audio buffer.

        Args:
            note_sequence: List of (freq, start, dur, cutoff, x, y, z).
            instrument: Instrument dictionary.
            total_duration: Total audio length in seconds.
            listener_pos: The (x, y, z) coordinates of the listener.

        Returns:
            np.ndarray: Stereo audio buffer of shape (2, N_samples).
        """
        master_len = int(self.sample_rate * total_duration)
        # Initialize Stereo Buffer (2 Channels x Samples)
        master_buffer = np.zeros((2, master_len))

        for item in note_sequence:
            # Unpack items (handling optional params)
            freq = item[0]
            start = item[1]
            dur = item[2]
            cutoff = item[3] if len(item) > 3 else None
            # Default to origin if no position data
            pos = item[4:] if len(item) > 4 else (0, 0, 0)

            # Generate Mono Source
            wave = self._generate_wave(freq, dur, instrument)
            wave = self._apply_adsr(wave, instrument['adsr'])
            if cutoff:
                wave = self._apply_lpf(wave, cutoff)

            # Calculate Spatial Position
            gain_l, gain_r = self._calculate_spatial_gains(pos, listener_pos)

            # Mix into Master Buffer
            start_idx = int(start * self.sample_rate)
            end_idx = start_idx + len(wave)

            if start_idx < master_len:
                if end_idx > master_len:
                    wave = wave[:master_len - start_idx]
                    end_idx = master_len
                
                # Apply gains to Left (row 0) and Right (row 1)
                master_buffer[0, start_idx:end_idx] += wave * gain_l
                master_buffer[1, start_idx:end_idx] += wave * gain_r

        # Master Normalization
        if np.max(np.abs(master_buffer)) > 0:
            master_buffer /= np.max(np.abs(master_buffer))

        return master_buffer