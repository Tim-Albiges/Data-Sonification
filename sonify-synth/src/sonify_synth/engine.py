import numpy as np
from typing import Dict, List, Tuple, Optional
from .utils import midi_to_freq

class AudioEngine:
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate

    def _generate_wave(self, freq: float, duration: float, params: Dict) -> np.ndarray:
        """Generates a raw wave with harmonics and vibrato."""
        t = np.linspace(0, duration, int(self.sample_rate * duration), endpoint=False)
        
        # Vibrato: Frequency Modulation
        v_rate = params.get('v_rate', 0)
        v_width = params.get('v_width', 0)
        
        # Calculate phase shift if vibrato exists
        if v_rate > 0:
            phase_shift = (v_width / v_rate) * np.sin(2 * np.pi * v_rate * t)
        else:
            phase_shift = 0

        wave = np.zeros_like(t)
        # Additive Synthesis: Summing sine waves for harmonics
        for i, weight in enumerate(params['harmonics']):
            harmonic_freq = freq * (i + 1)
            # Stop if harmonic is above Nyquist frequency (half sample rate)
            if harmonic_freq < self.sample_rate / 2:
                wave += weight * np.sin(2 * np.pi * harmonic_freq * t + (i + 1) * phase_shift)
            
        # Normalize raw wave
        if np.max(np.abs(wave)) > 0:
            wave /= np.max(np.abs(wave))
        return wave

    def _apply_adsr(self, wave: np.ndarray, adsr: Dict) -> np.ndarray:
        """Applies Attack-Decay-Sustain-Release envelope."""
        total_len = len(wave)
        a_len = int(adsr['attack'] * self.sample_rate)
        d_len = int(adsr['decay'] * self.sample_rate)
        r_len = int(adsr['release'] * self.sample_rate)
        s_len = total_len - (a_len + d_len + r_len)

        # Handle edge case where note is too short for full envelope
        if s_len < 0:
            s_len = 0
            # Simple fallback: distribute remaining time
            remaining = total_len - a_len
            if remaining > 0:
                d_len = remaining // 2
                r_len = remaining - d_len
            else:
                a_len = total_len
                d_len = 0
                r_len = 0

        # Create envelope segments
        envelope = np.concatenate([
            np.linspace(0, 1, a_len),
            np.linspace(1, adsr['sustain'], d_len),
            np.full(s_len, adsr['sustain']),
            np.linspace(adsr['sustain'], 0, r_len)
        ])
        
        # Fix rounding errors in length
        if len(envelope) < total_len:
            envelope = np.pad(envelope, (0, total_len - len(envelope)))
        elif len(envelope) > total_len:
            envelope = envelope[:total_len]

        return wave * envelope

    def _apply_lpf(self, audio: np.ndarray, cutoff: float) -> np.ndarray:
        """Applies a simple IIR Low Pass Filter."""
        # Physics: RC filter simulation
        rc = 1.0 / (2 * np.pi * cutoff + 1e-10)
        dt = 1.0 / self.sample_rate
        alpha = dt / (rc + dt)
        
        filtered = np.zeros_like(audio)
        prev = 0.0
        for i in range(len(audio)):
            filtered[i] = prev + alpha * (audio[i] - prev)
            prev = filtered[i]
        return filtered

    def render(self, note_sequence: List[Tuple], instrument: Dict, total_duration: float) -> np.ndarray:
        """
        Renders a full polyphonic sequence.
        note_sequence: List of tuples (freq, start_time, duration, [optional_cutoff])
        """
        master_len = int(self.sample_rate * total_duration)
        master_buffer = np.zeros(master_len)

        for item in note_sequence:
            # Unpack variable arguments safely
            freq = item[0]
            start = item[1]
            dur = item[2]
            cutoff = item[3] if len(item) > 3 else None

            # 1. Generate
            wave = self._generate_wave(freq, dur, instrument)
            # 2. Envelope
            wave = self._apply_adsr(wave, instrument['adsr'])
            # 3. Filter (Optional)
            if cutoff:
                wave = self._apply_lpf(wave, cutoff)

            # 4. Mix into Master Buffer
            start_idx = int(start * self.sample_rate)
            end_idx = start_idx + len(wave)
            
            # Boundary check
            if start_idx < master_len:
                if end_idx > master_len:
                    wave = wave[:master_len - start_idx]
                    end_idx = master_len
                
                master_buffer[start_idx:end_idx] += wave

        # Final Master Normalization
        if np.max(np.abs(master_buffer)) > 0:
            master_buffer /= np.max(np.abs(master_buffer))

        return master_buffer