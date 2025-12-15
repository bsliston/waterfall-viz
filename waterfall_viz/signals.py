import numpy as np


def tone(
    sample_rate_hz: float,
    offset_freq_hz: float,
    duration_sec: float,    
) -> np.ndarray:
    time_sec = np.arange(0.0, duration_sec, 1.0 / sample_rate_hz)
    return np.exp(1j * 2 * np.pi * offset_freq_hz * time_sec)


def pulsed_tone_signal_generator(buffer_size: int) -> np.ndarray:
    sample_rate_hz: float = 1.024e6
    offset_freq_hz: float = sample_rate_hz * 0.35 # 1e3
    duration_sec: float = 1.0
    signal = tone(sample_rate_hz, offset_freq_hz, duration_sec)
    signal[:signal.size//2] = 0.0
    
    start_idx: int = 0
    while True:
        stop_idx = start_idx + buffer_size
        signal_buffer = signal[start_idx:stop_idx]
        
        start_idx += buffer_size
        if start_idx >= signal.size:
            start_idx = 0
        yield signal_buffer
    
    
if __name__ == "__main__":
    for signal in pulsed_tone_signal_generator():
        breakpoint()