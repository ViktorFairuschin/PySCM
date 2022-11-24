# Copyright Viktor Fairuschin 2022

from abc import ABC
from abc import abstractmethod

import numpy as np
from scipy.linalg import eig

from pyscm.layers import ElasticLayer


class AbstractWaveGuideClass(ABC):
    """Abstract waveguide class"""

    @abstractmethod
    def __init__(self, layers: list, name: str):

        if isinstance(name, str):
            self._name = str(name)
        else:
            raise TypeError(f"'name' must be of type 'str'; got '{type(name).__name__}' instead.")

    @abstractmethod
    def __build__(self, n: int):
        pass

    @abstractmethod
    def __call__(self, f: float):
        pass

    def __str__(self):
        return f"<WaveGuid>({self._name})"

    @property
    def name(self):
        return self._name


class WaveGuide(AbstractWaveGuideClass):
    """Waveguide class"""

    def __init__(self, layers: list = [], name: str = 'waveguide'):
        """Create waveguide object.

        Parameters
        ----------
        layers : list of ElasticLayer objects
            List of layers.
        name : str
            Waveguide's name (optional).
        """
        super(WaveGuide, self).__init__(layers, name)

    def __build__(self, n: int):
        """Build waveguide.

        Parameters
        ----------
        n : int
            Number of collocation points.
        """
        super(WaveGuide, self).__build__()

    def __call__(self, f: float):
        """Compute wave velocities.

        Parameters
        ----------
        f : float
            Frequency in Hz.
        """
        super(WaveGuide, self).__call__()


if __name__ == '__main__':

    waveguide = WaveGuide([5])
    print(waveguide)

