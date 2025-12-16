import numpy as np


def tone(
    sample_rate_hz: float,
    offset_freq_hz: float,
    duration_sec: float,    
) -> np.ndarray:
    time_sec = np.arange(0.0, duration_sec, 1.0 / sample_rate_hz)
    return np.exp(1j * 2 * np.pi * offset_freq_hz * time_sec)
