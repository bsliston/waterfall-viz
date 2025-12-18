from rtlsdr import RtlSdr, RtlSdrAio
import matplotlib.pyplot as plt
import numpy as np
from rtlsdr.helpers import limit_calls

import time
from scipy.signal import firwin, resample_poly, resample
from pathlib import Path
import signal
import asyncio

import random

import pdb

# def plot_data(
#     center_freq_hz: float = 102.1e6,
#     sample_rate_hz: float = 1.024e6,
#     gain: float = 50.0,
#     snippet_duration_sec: float = 5.0
# ) -> None:
#     radio = RtlSdr()
    
#     radio.center_freq = center_freq_hz
#     radio.sample_rate = sample_rate_hz
#     radio.gain = gain
    
#     radio.read_samples(2048) # Clear buffer.

#     # Loop and receive data.
#     recv_num_samples: int = int(snippet_duration_sec * radio.sample_rate)
#     signal = radio.read_samples(recv_num_samples)
    
#     plt.close()
#     _ = plt.specgram(signal)
#     plt.savefig("specto.png")
    

# if __name__ == "__main__":
#     plot_data()



from rtlsdr import RtlSdr
from numpy import var, log10



from waterfall_viz.generators import SignalGenerator


class RTLSDRSignalGenerator(SignalGenerator):
    def __init__(
        self,
        carrier_freq_hz: float,
        sample_rate_hz: float,
        gain_db: int,
        buffer_size: int, 
    ) -> None:
        super().__init__(
            carrier_freq_hz, sample_rate_hz, gain_db, buffer_size
        )
        
        self._sdr = RtlSdr()
        self._sdr.sample_rate = self._sample_rate_hz
        self._sdr.center_freq = self._carrier_freq_hz
        self._sdr.gain = self._gain_db
    
    def __next__(self, samples, sdr_context) -> np.ndarray:
        # print(samples, sdr_context)
        pass
        
    def start_async_read(self):
        print("Starting async read...")
        self._sdr.read_samples_async(
            self.__next__, num_samples=self._buffer_size
        )
        print("HERE!!!")
        print()
        print()
        print()
        
        try:
            signal.pause() 
        except KeyboardInterrupt:
            self.stop_async_read()

    def stop_async_read(self):
        print("Cancelling async read and closing SDR...")
        self._sdr.cancel_read_async()
        self._sdr.close()
        print("Stopped.")


recvr = RTLSDRSignalGenerator(121.1e6, 1.024e6, 50, 1024)
recvr.start_async_read()

recvr.stop_async_read()