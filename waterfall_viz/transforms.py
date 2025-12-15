import numpy as np
import time

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
        t0 = time.time()
        sxx = np.fft.fftshift(np.fft.fft(signal, n=fft_size))
        sxx = 10.0 * np.log10(np.abs(sxx) ** 2.0)
        t1 = time.time()
        waterfall_data[:-1] = waterfall_data[1:]
        waterfall_data[-1] = sxx
        t2 = time.time()
        
        waterfall_data_dbfs = waterfall_data - waterfall_data.max()
        waterfall_data_dbfs = np.clip(waterfall_data_dbfs, -100.0, 0.0)
        t3 = time.time()
        
        sse_data = waterfall_data_dbfs.tolist()
        t4 = time.time()
        
        # time.sleep(0.001)
        # print(time.time() - t0)
        # print(time.time() - t1)
        # print(time.time() - t2)
        # print(time.time() - t3)
        # print(time.time() - t4)
        # print()
        
        # Sleep for simulated duration of generated signal length.
        signal_duration_sec = signal.size / signal_generator.sample_rate_hz
        print(signal_duration_sec)
        time.sleep(signal_duration_sec)
        yield f"data:{sse_data}\n\n"
