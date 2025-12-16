import numpy as np

from waterfall_viz.generators.signal_generator import SignalGenerator


FREQUENCY_CONVERSIONS: dict[str, float] = {
    "Hz": 1.0,
    "kHz": 1.0e3,
    "MHz": 1.0e6,
    "GHz": 1.0e9,
}


def convert_frequency_units(value: float, unit: str, target_unit: str = "Hz") -> float:
    value_hz = value * FREQUENCY_CONVERSIONS[unit]
    return value_hz / FREQUENCY_CONVERSIONS[target_unit]
    

def waterfall_generator(
    signal_generator: SignalGenerator,
    waterfall_duration_sec: float, 
    fft_size: int,
) -> list:
    history_num_samples = int(
        waterfall_duration_sec * signal_generator.sample_rate_hz
    )
    history_depth_size = history_num_samples // signal_generator.buffer_size
    waterfall_data = np.zeros((history_depth_size, fft_size))
    for signal in signal_generator:
        sxx = np.fft.fftshift(np.fft.fft(signal, n=fft_size))
        sxx = 10.0 * np.log10(np.abs(sxx) ** 2.0)
        waterfall_data[:-1] = waterfall_data[1:]
        waterfall_data[-1] = sxx
        
        waterfall_data_dbfs = waterfall_data - waterfall_data.max()
        waterfall_data_dbfs = np.clip(waterfall_data_dbfs, -100.0, 0.0)
        
        sse_data = waterfall_data_dbfs.tolist()
        yield f"data:{sse_data}\n\n"
