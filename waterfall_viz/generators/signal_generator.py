import numpy as np

import abc


class SignalGenerator:
    def __init__(
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
    
    def __iter__(self):
        return self
    
    @property
    def carrier_freq_hz(self) -> float:
        return self._carrier_freq_hz
    
    @property
    def sample_rate_hz(self) -> float:
        return self._sample_rate_hz
    
    @property
    def gain_db(self) -> int:
        return self._gain_db
    
    @property
    def buffer_size(self) -> int:
        return self._buffer_size
    
    @abc.abstractmethod
    def __next__(self) -> np.ndarray:
        pass