"""
Data Extraction Utilities.

Extracts numerical arrays (x, y, z) from Matplotlib Figures, Pandas DataFrames,
and raw lists/arrays.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
from typing import Tuple, Union, Optional, List


def _extract_from_dataframe(
    df: pd.DataFrame, x_col: str, y_col: str, z_col: Optional[str] = None
) -> Tuple[np.ndarray, np.ndarray, Optional[np.ndarray]]:
    """Extract arrays from Pandas DataFrame."""
    if x_col not in df.columns or y_col not in df.columns:
        raise ValueError(f"Columns {x_col} and/or {y_col} not found.")

    x = df[x_col].to_numpy()
    y = df[y_col].to_numpy()
    z = df[z_col].to_numpy() if z_col and z_col in df.columns else None

    return x, y, z


def _extract_from_figure(fig: Figure) -> Tuple[np.ndarray, np.ndarray, Optional[np.ndarray]]:
    """Extract data from Matplotlib Figure (2D or 3D)."""
    if not fig.axes:
        raise ValueError("Figure has no axes.")

    ax = fig.axes[0]
    if not ax.lines:
        raise ValueError("No supported plot type (Line2D) found.")

    line = ax.lines[0]
    x_data = line.get_xdata()
    y_data = line.get_ydata()
    z_data = None

    # 3D Detection
    if hasattr(ax, 'name') and ax.name == '3d':
        try:
            z_data = line.get_3d_zdata()
        except AttributeError:
            if hasattr(line, '_verts3d'):
                z_data = line._verts3d[2]

    x_arr = np.array(x_data)
    y_arr = np.array(y_data)
    z_arr = np.array(z_data) if z_data is not None else None

    return x_arr, y_arr, z_arr


def get_xyz_data(
    data: Union[pd.DataFrame, Figure, np.ndarray, List],
    **kwargs
) -> Tuple[np.ndarray, np.ndarray, Optional[np.ndarray]]:
    """Main dispatcher for data extraction."""
    # 1. Matplotlib Figure
    if isinstance(data, Figure):
        return _extract_from_figure(data)

    # 2. Pandas DataFrame
    elif isinstance(data, pd.DataFrame):
        x_col = kwargs.get('x_col', 'x')
        y_col = kwargs.get('y_col', 'y')
        z_col = kwargs.get('z_col', None)
        return _extract_from_dataframe(data, x_col, y_col, z_col)

    # 3. Lists / Arrays
    elif isinstance(data, (list, np.ndarray)):
        arr = np.array(data)
        if arr.ndim == 1:
            y = arr
            x = np.arange(len(y))
            return x, y, None
        if len(arr) >= 2:
            x = np.array(data[0])
            y = np.array(data[1])
            z = np.array(data[2]) if len(data) > 2 else None
            return x, y, z

    # 4. Tuple
    elif isinstance(data, tuple):
        x = np.array(data[0])
        y = np.array(data[1])
        z = np.array(data[2]) if len(data) > 2 else None
        return x, y, z

    else:
        raise TypeError(f"Unsupported type: {type(data)}")