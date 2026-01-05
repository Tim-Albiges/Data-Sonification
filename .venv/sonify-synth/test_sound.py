import numpy as np
import os
from sonify_synth import AudioEngine, DataSonifier, PRESETS, save_wav

def test_generation():
    print("Testing Sonification Engine...")
    
    # 1. Create Fake Data (A simple ascending sine wave)
    # 50 data points over 5 seconds
    x = np.linspace(0, 5, 50)  
    y = np.sin(x)              
    z = np.linspace(0, 1, 50)  # Increasing brightness (filter cutoff)

    # 2. Initialize Engine
    engine = AudioEngine(sample_rate=44100)
    sonifier = DataSonifier(engine)

    # 3. Test 2D Sonification (Piano)
    print("  - Rendering 2D Piano sequence...")
    notes_2d = sonifier.sonify_2d(x, y, duration=5.0)
    audio_2d = engine.render(notes_2d, PRESETS['piano'], total_duration=6.0)
    save_wav("test_piano_2d.wav", 44100, audio_2d)

    # 4. Test 3D Sonification (Violin with Filter)
    print("  - Rendering 3D Violin sequence...")
    notes_3d = sonifier.sonify_3d(x, y, z, duration=5.0)
    audio_3d = engine.render(notes_3d, PRESETS['violin'], total_duration=6.0)
    save_wav("test_violin_3d.wav", 44100, audio_3d)

    print("Success! Check your folder for 'test_piano_2d.wav' and 'test_violin_3d.wav'")

if __name__ == "__main__":
    test_generation()