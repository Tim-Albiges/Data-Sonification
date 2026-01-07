import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pytest
from src.sonify_plot import sonify
from src.sonify_plot.extract import get_xyz_data

@pytest.fixture
def sample_df():
    return pd.DataFrame({'a': [0, 1], 'b': [10, 20]})

def test_dataframe_extraction(sample_df):
    x, y, z = get_xyz_data(sample_df, x_col='a', y_col='b')
    assert np.array_equal(x, sample_df['a'].values)
    assert z is None

def test_sonify_return_type_stereo(sample_df):
    """Ensure output is 2D stereo array."""
    audio = sonify(sample_df, x_col='a', y_col='b', duration=1.0)
    assert isinstance(audio, np.ndarray)
    assert audio.ndim == 2
    assert audio.shape[0] == 2  # Left/Right channels
    assert audio.shape[1] >= 44100 # Approx 1 sec samples