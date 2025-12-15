import numpy as np

from waterfall_viz.signals import tone
from waterfall_viz.generators import SignalGenerator


class PulsedToneGenerator(SignalGenerator):
    def __init__(
        self,
        carrier_freq_hz: float,
        sample_rate_hz: float,
        gain_db: int,
        buffer_size: int, 
        offset_freq_hz: float = 10e3,
        duration_sec: float = 1.0
    ) -> None:
        super().__init__(carrier_freq_hz, sample_rate_hz, gain_db, buffer_size)
        
        self._offset_freq_hz = offset_freq_hz
        self._duration_sec = duration_sec
        
        self._start_idx: int = 0
        self._signal = tone(sample_rate_hz, offset_freq_hz, duration_sec)
        self._signal[:self._signal.size//2] = 0.0
        
    def __next__(self) -> np.ndarray:
        while True:
            stop_idx = self._start_idx + self._buffer_size
            signal_buffer = self._signal[self._start_idx:stop_idx]
            
            self._start_idx += self._buffer_size
            if self._start_idx >= self._signal.size:
                self._start_idx = 0
            return signal_buffer