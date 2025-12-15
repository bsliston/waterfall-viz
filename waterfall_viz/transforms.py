from typing import Iterable

import numpy as np
import time

from waterfall_viz.signals import pulsed_tone_signal_generator
from waterfall_viz import constants

def waterfall_generator(
    signal_generator: Iterable[np.ndarray] = None,
    history: int = 200, 
    buffer_size: int = 50240,
    fft_size: int = 256,
) -> list:
    waterfall_data = np.zeros((history, fft_size))
    for signal in pulsed_tone_signal_generator(buffer_size):
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
        
        time.sleep(1.0 / constants.FRAMERATE_HZ)
        yield f"data:{sse_data}\n\n"

    
if __name__ == "__main__":
    for signal in waterfall_generator(history=5, buffer_size=128):
        breakpoint()