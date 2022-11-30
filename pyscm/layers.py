# Copyright Viktor Fairuschin 2022

from abc import ABC
from abc import abstractmethod

import numpy as np

from pyscm.utils import chebyshev_dm


class AbstractElasticLayerClass(ABC):
    """Abstract elastic layer class"""

    @abstractmethod
    def __init__(self, cl: float, ct: float, rho: float, d: float, name: str):

        if isinstance(cl, (float, int)):
            if cl > 0:
                self._cl = float(cl)
            else:
                raise ValueError(f"'cl' must be positive; got {cl} instead.")
        else:
            raise TypeError(f"'cl' must be of type 'float' or 'int'; got '{type(cl).__name__}' instead.")

        if isinstance(ct, (float, int)):
            if ct > 0:
                self._ct = float(ct)
            else:
                raise ValueError(f"'ct' must be positive; got {ct} instead.")
        else:
            raise TypeError(f"'ct' must be of type 'float' or 'int'; got '{type(ct).__name__}' instead.")

        if isinstance(rho, (float, int)):
            if rho > 0:
                self._rho = float(rho)
            else:
                raise ValueError(f"'rho' must be positive; got {rho} instead.")
        else:
            raise TypeError(f"'rho' must be of type 'float' or 'int'; got '{type(rho).__name__}' instead.")

        if isinstance(d, (float, int)):
            if d > 0:
                self._d = float(d)
            else:
                raise ValueError(f"'d' must be positive; got {d} instead.")
        else:
            raise TypeError(f"'d' must be of type 'float' or 'int'; got '{type(d).__name__}' instead.")

        if isinstance(name, str):
            self._name = str(name)
        else:
            raise TypeError(f"'name' must be of type 'str'; got '{type(name).__name__}' instead.")

    @abstractmethod
    def __call__(self, n: int):

        if isinstance(n, int):
            if n > 0:
                self._n = int(n)
            else:
                raise ValueError(f"'n' must be positive; got {n} instead.")
        else:
            raise TypeError(f"'n' must be of type 'int'; got '{type(n).__name__}' instead.")

    def __str__(self):
        return f"<ElasticLayer>({self._name})"

    @property
    def cl(self):
        return self._cl

    @property
    def ct(self):
        return self._ct

    @property
    def rho(self):
        return self._rho

    @property
    def d(self):
        return self._d

    @property
    def name(self):
        return self._name


class ElasticLayer(AbstractElasticLayerClass):
    """Elastic layer class"""

    def __init__(self, cl: float, ct: float, rho: float, d: float, name: str = 'layer'):
        """Create elastic layer object.

        Parameters
        ----------
        cl : float
            Layer's longitudinal wave velocity in m/s
        ct : float
            Layer's transverse wave velocity in m/s
        rho : float
            Layer's mass density in kg/m^3
        d : float
            Layer's thickness in m
        name : str
            Layer's name (optional)
        """
        super(ElasticLayer, self).__init__(cl, ct, rho, d, name)

    def __call__(self, n: int):
        """Return layer's equations.

        Parameters
        ----------
        n : int
            Number of collocation points.
        """
        super(ElasticLayer, self).__call__(n)

        # Rescale elastic constants to prevent numeric errors

        cl = self.cl / 1.0e3
        ct = self.ct / 1.0e3
        d = self.d * 1.0e6

        la = self.rho * (self.cl ** 2 - 2 * self.ct ** 2) / 10.0e18
        mu = self.rho * self.ct ** 2 / 10.0e18

        # Compute Chebyshev differentiation matrices

        _, dm = chebyshev_dm(n, 2)
        dm_one = dm[0, :, :] * (2 / d) ** 1
        dm_two = dm[1, :, :] * (2 / d) ** 2

        # Assemble the equations

        i = 1j
        eye = np.eye(n)
        zeros = np.zeros_like(eye)

        lhs = np.stack([
            np.block([[dm_two, zeros], [zeros, dm_two]]),
            np.block([[zeros, zeros], [zeros, zeros]]),
            np.block([[- eye, zeros], [zeros, - eye]])
        ])

        rhs = np.block([[(- 1 / cl ** 2) * eye, zeros], [zeros, (- 1 / ct ** 2) * eye]])

        sig = np.stack([
            np.block([[zeros, mu / i * dm_two], [(la + 2 * mu) * dm_two, zeros]]),
            np.block([[- 2 * mu / i * dm_one, zeros], [zeros, - 2 * mu * dm_one]]),
            np.block([[zeros, mu / i * eye], [- la * eye, zeros]])
        ])

        eps = np.stack([
            np.block([[dm_one, zeros], [zeros, - i * dm_one]]),
            np.block([[zeros, - eye], [i * eye, zeros]]),
            np.block([[zeros, zeros], [zeros, zeros]])
        ])

        return lhs, rhs, sig, eps

    @classmethod
    def from_elastic_constants(cls, E: float, rho: float, nu: float, d: float, name: str = "layer"):
        """Create elastic layer object using elastic constants.

        Parameters
        ----------
        E : float
            Layer's Young's modulus in N/m^2
        rho : float
            Layer's mass density in kg/m^3
        nu : float
            Layer's Poisson's ratio
        d : float
            Layer's thickness in m
        name : str
            Layer's name (optional)
        """

        if isinstance(E, (float, int)):
            if E > 0:
                E = float(E)
            else:
                raise ValueError(f"'E' must be positive; got {E} instead.")
        else:
            raise TypeError(f"'E' must be of type 'float' or 'int'; got '{type(E).__name__}' instead.")

        if isinstance(rho, (float, int)):
            if rho > 0:
                rho = float(rho)
            else:
                raise ValueError(f"'rho' must be positive; got {rho} instead.")
        else:
            raise TypeError(f"'rho' must be of type 'float' or 'int'; got '{type(rho).__name__}' instead.")

        if isinstance(nu, (float, int)):
            if nu > 0:
                nu = float(nu)
            else:
                raise ValueError(f"'nu' must be positive; got {nu} instead.")
        else:
            raise TypeError(f"'nu' must be of type 'float' or 'int'; got '{type(nu).__name__}' instead.")

        # this can still result in cl/ct <= 0!

        cl = np.sqrt((E * (1 - nu)) / (rho * (1 - nu - 2 * np.square(nu))))
        ct = np.sqrt(E / (2 * rho * (1 + nu)))

        return cls(cl, ct, rho, d, name)


if __name__ == '__main__':
    pass
