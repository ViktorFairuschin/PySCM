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

        self._is_build = False
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
        if len(self._layers) > 0:
            pass
        else:
            raise RuntimeError("Nothing to build. Add layers first.")

    @abstractmethod
    def __call__(self, f: float):
        if isinstance(f, (float, int)):
            if f > 0:
                pass
            else:
                raise ValueError(f"'f' must be positive; got {f} instead.")
        else:
            raise TypeError(f"'f' must be of type 'float' or 'int'; got '{type(f).__name__}' instead.")

        if not self.is_build:
            raise RuntimeError("Waveguide has not been built yet. Call 'build' method first.")

    def __str__(self):
        return f"<WaveGuid>({self._name})"

    @property
    def name(self):
        return self._name

    @property
    def layers(self):
        return self._layers

    @property
    def is_build(self):
        return self._is_build


class WaveGuide(AbstractWaveGuideClass):
    """Waveguide class"""

    def __init__(self, layers=None, name: str = 'waveguide'):
        """Create waveguide object.

        Parameters
        ----------
        layers : list
            List of layers.
        name : str
            Waveguide's name (optional).
        """
        super(WaveGuide, self).__init__(layers, name)

        if layers is None:
            layers = []

        self.lhs = None
        self.rhs = None
        self.sig = None
        self.eps = None

    def add(self, layer: ElasticLayer):
        """Add layer to waveguide.

        Parameters
        ----------
        layer : ElasticLayer
            Layer to be added to waveguide.
        """
        super(WaveGuide, self).add(layer)
        self._is_build = False
        return self

    def build(self, n: int = 16):
        """Assemble waveguide's equations.

        Parameters
        ----------
        n : int
            Number of collocation points.
        """
        super(WaveGuide, self).build(n)

        dim = len(self.layers) * 2 * n

        self.lhs = np.zeros((3, dim, dim), dtype='complex')
        self.rhs = np.zeros((dim, dim), dtype='complex')
        self.sig = np.zeros((3, dim, dim), dtype='complex')
        self.eps = np.zeros((3, dim, dim), dtype='complex')

        for i, layer in enumerate(self.layers):

            il = 0 + 2 * n * i
            ih = 2 * n + 2 * n * i

            lhs, rhs, sig, eps = layer(n)

            self.lhs[:, il:ih, il:ih] = lhs
            self.rhs[il:ih, il:ih] = rhs
            self.sig[:, il:ih, il:ih] = sig
            self.eps[:, il:ih, il:ih] = eps

        # boundary conditions

        self.lhs[:, 0, :] = self.sig[:, 0, :]
        self.lhs[:, n, :] = self.sig[:, n, :]
        self.rhs[0, :] = np.zeros((1, dim))
        self.rhs[n, :] = np.zeros((1, dim))
        self.lhs[:, dim - 1, :] = self.sig[:, dim - 1, :]
        self.lhs[:, dim - 1 - n, :] = self.sig[:, dim - 1 - n, :]
        self.rhs[dim - 1, :] = np.zeros((1, dim))
        self.rhs[dim - 1 - n, :] = np.zeros((1, dim))

        # interface conditions

        if len(self.layers) > 1:

            adjacent_layers = []
            for i in range(len(self.layers) - 1):
                adjacent_layers.append((self.layers[i], self.layers[i + 1]))

            for i, (upper_layer, lower_layer) in enumerate(adjacent_layers):
                il = 0 + 2 * n * i
                ih = 4 * n + 2 * n * i

                _, _, upper_layer_sig, upper_layer_eps = upper_layer(n)
                _, _, lower_layer_sig, lower_layer_eps = lower_layer(n)

                upper_sig = np.append(upper_layer_sig[:, (n - 1), :], lower_layer_sig[:, 0, :], axis=-1)
                lower_sig = np.append(upper_layer_sig[:, (2 * n - 1), :], lower_layer_sig[:, n, :], axis=-1)
                upper_eps = np.append(upper_layer_eps[:, (n - 1), :], lower_layer_eps[:, 0, :], axis=-1)
                lower_eps = np.append(upper_layer_eps[:, (2 * n - 1), :], lower_layer_eps[:, n, :], axis=-1)

                self.lhs[:, (n - 1 + 2 * n * i), il:ih] = upper_sig
                self.rhs[(n - 1 + 2 * n * i), :] = np.zeros((1, self.rhs.shape[-1]))
                self.lhs[:, (2 * n - 1 + 2 * n * i), il:ih] = upper_eps
                self.rhs[(2 * n - 1 + 2 * n * i), :] = np.zeros((1, self.rhs.shape[-1]))
                self.lhs[:, (2 * n + 2 * n * i), il:ih] = lower_sig
                self.rhs[(2 * n + 2 * n * i), :] = np.zeros((1, self.rhs.shape[-1]))
                self.lhs[:, (3 * n + 2 * n * i), il:ih] = lower_eps
                self.rhs[(3 * n + 2 * n * i), :] = np.zeros((1, self.rhs.shape[-1]))

        self._is_build = True

        return self

    def __call__(self, f: float):
        """Solve the equations for provided frequency.

        Parameters
        ----------
        f : float
            Frequency in Hz.
        """
        super(WaveGuide, self).__call__(f)

        # Rescale frequency to prevent numeric errors

        f /= 1.0e9
        omega = 2 * np.pi * f

        eye = np.eye(self.rhs.shape[0])
        zeros = np.zeros_like(eye)

        lhs = np.block([[- self.lhs[1], - (self.lhs[0] - omega ** 2 * self.rhs)], [eye, zeros]])
        rhs = np.block([[self.lhs[2], zeros], [zeros, eye]])

        k, u = eig(a=lhs, b=rhs, left=False, right=True)

        # Rescale wave numbers to original order of magnitude

        k = np.where(np.isinf(k), 0, k) * 1.0e6

        # Keep only positive wave numbers with small imaginary part

        k = np.where(np.abs(np.imag(k)) < 1, k, np.nan)
        k = np.where(k > 0, np.abs(k), np.nan)

        return k, u

    @staticmethod
    def process_results(results):
        pass


if __name__ == '__main__':
    pass


