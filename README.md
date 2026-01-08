
# Data Sonification Suite

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Tim-Albiges/Data-Sonification/blob/main/Data_Sonification_Library.ipynb)

A comprehensive Python ecosystem for transforming data into sound. This suite allows researchers, artists, and developers to "listen" to their datasets using high-quality wavetable synthesis and 3D spatial audio.

## 📦 Project Overview

The suite is modular and divided into two distinct packages:

1.  **`sonify-synth` (The Engine)**
    * **Role:** The core audio synthesizer.
    * **Features:** Polyphonic wavetable synthesis, ADSR envelopes, filters, and a 3D spatial rendering engine (Stereo/Binaural simulation).
    * **Best for:** Users who want raw control over audio generation or want to build their own mapping logic.

2.  **`sonify-plot` (The Wrapper)**
    * **Role:** The high-level translator.
    * **Features:** Converts Pandas DataFrames, Matplotlib Plots (2D/3D), and NumPy arrays directly into audio.
    * **Best for:** Data scientists who want to hear a plot with one line of code.

---

## 🚀 Installation Guide

This project is designed to be installed from source. 

### Prerequisites
* Python 3.8 or higher
* Git

### Quick Start (One-Line Install)

**For Google Colab / Jupyter:**
Run this in a cell to download and install the suite immediately:
```python
!curl -sSL https://raw.githubusercontent.com/Tim-Albiges/Data-Sonification/main/install.py | python3

```

**For Local Terminal (Linux/macOS/Windows):**
If you have cloned the repository, you can use the included helper script to install dependencies in the correct order:

```bash
# 1. Clone the repository (Clean URL, no brackets)
!git clone https://github.com/Tim-Albiges/Data-Sonification.git

# 2. Enter the folder (Use %cd, not !cd)
%cd Data-Sonification

# 3. Run the installer
!python install.py

```

---

## 🎧 Usage Guide

### 1. Using `sonify-plot` (Recommended for Beginners)

The easiest way to get started. Just pass your data, and it returns audio.

#### Example A: Sonify a Pandas DataFrame

Maps the `time` column to the timeline and the `sales` column to Pitch.

```python
import pandas as pd
from sonify_plot import sonify
from sonify_synth.utils import save_wav

# 1. Load your data
df = pd.DataFrame({
    'time': [0, 1, 2, 3, 4],
    'sales': [100, 120, 90, 200, 250] 
})

# 2. Convert to Audio
audio = sonify(
    df,
    mode='2d',
    x_col='time',
    y_col='sales',
    instrument='piano',
    duration=5.0
)

# 3. Save to disk
save_wav("sales_data.wav", 44100, audio)

```

#### Example B: 3D Spatial Audio (The "Sitting in Data" Effect)

If you have 3D data (X, Y, Z), the library automatically maps:

* **X:** Time & Left/Right Panning
* **Y:** Pitch & Front/Back Depth
* **Z:** Timbre (Brightness) & Vertical Height

You can specify where the "listener" is sitting relative to the data.

```python
import numpy as np
import matplotlib.pyplot as plt
from sonify_plot import sonify
from sonify_synth.utils import save_wav

# 1. Create a 3D Spiral Plot
theta = np.linspace(0, 4*np.pi, 100)
x = np.sin(theta)
y = np.cos(theta)
z = np.linspace(-1, 1, 100)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(x, y, z)

# 2. Render Audio (Listener at Origin)
# The sound will spin around your head!
audio = sonify(
    fig,
    mode='3d',
    instrument='flute',
    duration=10.0,
    listener_pos=(0, 0, 0) # You are sitting at x=0, y=0, z=0
)

save_wav("spiral_spatial.wav", 44100, audio)

```

### 2. Using `sonify-synth` (For Advanced Users)

Use the engine directly if you want to compose music or control specific note frequencies.

```python
from sonify_synth import AudioEngine, PRESETS
from sonify_synth.utils import save_wav

# 1. Initialize Engine
engine = AudioEngine(sample_rate=44100)

# 2. Define a Sequence of Notes
# Format: (Frequency, StartTime, Duration, Cutoff, PosX, PosY, PosZ)
notes = [
    (440.0, 0.0, 0.5, None, -2, 0, 0), # A4 to your Left
    (554.4, 0.5, 0.5, None,  2, 0, 0), # C#5 to your Right
    (659.3, 1.0, 1.0, None,  0, 5, 0), # E5 in Front of you
]

# 3. Render
audio = engine.render(
    notes, 
    PRESETS['violin'], 
    total_duration=2.5,
    listener_pos=(0, 0, 0)
)

save_wav("manual_chord.wav", 44100, audio)

```

---

## 📂 Included Demos

The project comes with built-in scripts to generate example audio files.

| Script Location | Description | Output Files |
| --- | --- | --- |
| `sonify-plot/demo_spatial.py` | Generates a 3D audio spiral that spins around the listener. | `spatial_origin.wav` (Spinning)<br>

<br>`spatial_distant.wav` (Quiet/Far) |
| `sonify-plot/demo_sonify.py` | Converts basic 2D DataFrames and Plots into Piano/Violin audio. | `output_dataframe.wav`<br>

<br>`output_matplotlib.wav` |

**To run a demo via terminal:**

```bash
cd sonify-plot
python demo_spatial.py

```

---

## 🛠 Project Structure

```text
DATA SONIFICATION/
├── sonify-synth/       # Core Audio Engine
│   ├── src/
│   │   └── sonify_synth/
│   │       ├── engine.py       # Spatial Rendering Logic
│   │       └── instruments.py  # Timbre Definitions
│
└── sonify-plot/        # High-Level Wrapper
    ├── src/
    │   └── sonify_plot/
    │       ├── wrapper.py      # Main user API
    │       └── extract.py      # Matplotlib/Pandas parsers
    └── tests/                  # Pytest suite

```

---

## 🤝 Contributing

1. Fork the repository.
2. Create a feature branch:
```bash
git checkout -b feature/NewInstrument

```


3. Commit your changes.
4. Run tests:
```bash
pytest

```


5. Push to the branch and open a Pull Request.

## 📜 License

This project is licensed under the MIT License.
