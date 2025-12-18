import numpy as np

import time

from rtlsdr import RtlSdr
from waterfall_viz.generators import SignalGenerator


class RTLSDRSignalGenerator(SignalGenerator):
    def __init__(
        self,
        carrier_freq_hz: float,
        sample_rate_hz: float,
        gain_db: int,
        buffer_size: int, 
    ) -> None:
        super().__init__(carrier_freq_hz, sample_rate_hz, gain_db, buffer_size)
        
        self._sdr = RtlSdr()
        self._sdr.sample_rate = self._sample_rate_hz
        self._sdr.center_freq = self._carrier_freq_hz
        self._sdr.gain = self._gain_db
        
        # Clear the beginning of the buffer.
        self._sdr.read_samples(2048)
        self._max_num_read_samples: int = 10240
        
    def __next__(self) -> np.ndarray:
        signal = np.zeros(self._buffer_size, dtype=np.complex128)
        idx: int = 0
        while True:
            samples = self._sdr.read_samples(self._max_num_read_samples)
            stop_idx = min(idx + samples.size, signal.size)
            num_samples = stop_idx - idx
            signal[idx:stop_idx] = samples[:num_samples]
            
            idx += samples.size
            if stop_idx >= signal.size:
                break
            
        return signal
    
    def update(
        self, 
        carrier_freq_hz: float,
        sample_rate_hz: float,
        gain_db: int,
        buffer_size: int, 
    ) -> None:
        self._carrier_freq_hz = carrier_freq_hz
        self._sample_rate_hz = sample_rate_hz
        self._gain_db = gain_db
        self._buffer_size = buffer_size
        
        self._sdr.sample_rate = self._sample_rate_hz
        self._sdr.center_freq = self._carrier_freq_hz
        self._sdr.gain = self._gain_db
            
            
if __name__ == "__main__":
    recvr = RTLSDRSignalGenerator(102.1e6, 1.024e6, 50, 50_000)
    for signal in recvr:
        print(signal.shape)