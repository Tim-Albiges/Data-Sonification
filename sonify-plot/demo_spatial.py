"""
Demo for 3D Spatial Audio.
"""
import numpy as np
import matplotlib.pyplot as plt
from sonify_plot import sonify
from sonify_synth.utils import save_wav

def test_spatial():
    print("Generating Spatial Audio...")
    
    # Spiral Data
    theta = np.linspace(0, 4*np.pi, 100)
    x = np.sin(theta)
    y = np.cos(theta)
    z = np.linspace(-1, 1, 100)
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(x, y, z)
    
    # 1. User at Origin (Audio spins around head)
    print("1. Rendering Listener at Origin (Spinning)...")
    audio = sonify(fig, mode='3d', instrument='flute', duration=5.0, listener_pos=(0,0,0))
    save_wav("spatial_origin.wav", 44100, audio)

    # 2. User Far Away (Audio is distant/quiet)
    print("2. Rendering Listener Far Away (Distant)...")
    audio = sonify(fig, mode='3d', instrument='cello', duration=5.0, listener_pos=(10,10,0))
    save_wav("spatial_distant.wav", 44100, audio)
    
    print("Success. Listen to output WAVs with headphones.")

if __name__ == "__main__":
    test_spatial()