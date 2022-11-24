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

        self._layers = []

        if isinstance(layers, list):
            for layer in layers:
                self.add(layer)
        else:
            raise TypeError(f"'layers' must be of type 'list'; got '{type(layers).__name__}' instead.")

        if isinstance(name, str):
            self._name = str(name)
        else:
            raise TypeError(f"'name' must be of type 'str'; got '{type(name).__name__}' instead.")

    @abstractmethod
    def add(self, layer: ElasticLayer):
        if isinstance(layer, ElasticLayer):
            self._layers.append(layer)
        else:
            raise TypeError(f"'layer' must be of type 'ElasticLayer'; got '{type(layer).__name__}' instead.")

    @abstractmethod
    def build(self, n: int):
        pass

    @abstractmethod
    def __call__(self, f: float):
        if isinstance(f, (float, int)):
            if f > 0:
                pass
            else:
                raise ValueError(f"'f' must be positive; got {f} instead.")
        else:
            raise TypeError(f"'f' must be of type 'float' or 'int'; got '{type(f).__name__}' instead.")

    def __str__(self):
        return f"<WaveGuid>({self._name})"

    @property
    def name(self):
        return self._name

    @property
    def layers(self):
        return self._layers


class WaveGuide(AbstractWaveGuideClass):
    """Waveguide class"""

    def __init__(self, layers: list = None, name: str = 'waveguide'):
        """Create waveguide object.

        Parameters
        ----------
        layers : list
            List of layers.
        name : str
            Waveguide's name (optional).
        """
        super(WaveGuide, self).__init__(layers, name)

    def add(self, layer: ElasticLayer):
        """Add layer to waveguide.

        Parameters
        ----------
        layer : ElasticLayer
            Layer to be added to waveguide.
        """
        super(WaveGuide, self).add(layer)
        return self

    def build(self, n: int):
        """Build waveguide.

        Parameters
        ----------
        n : int
            Number of collocation points.
        """
        super(WaveGuide, self).build(n)
        return self

    def __call__(self, f: float):
        """Compute wave velocities for provided frequency.

        Parameters
        ----------
        f : float
            Frequency in Hz.
        """
        super(WaveGuide, self).__call__(f)


if __name__ == '__main__':

    layer = ElasticLayer(6350, 3100, 2400, 1e-3, 'aluminium')
    waveguide = WaveGuide([layer]).add(layer)
    print(waveguide.layers)


