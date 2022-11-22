# Copyright Viktor Fairuschin 2022


from abc import ABC
from abc import abstractmethod

import numpy as np


class AbstractElasticLayerClass(ABC):
    """Abstract elastic layer class.
    """

    @abstractmethod
    def __init__(self, cl: float, ct: float, rho: float, d: float, n: int, name: str):

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

        if isinstance(n, int):
            if n > 0:
                self._n = int(n)
            else:
                raise ValueError(f"'n' must be positive; got {n} instead.")
        else:
            raise TypeError(f"'n' must be of type 'int'; got '{type(n).__name__}' instead.")

        if isinstance(name, str):
            self._name = str(name)
        else:
            raise TypeError(f"'name' must be of type 'str'; got '{type(name).__name__}' instead.")

    @abstractmethod
    def __build__(self, n: int):
        pass

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
    def n(self):
        return self._n

    @property
    def name(self):
        return self._name


class ElasticLayer(AbstractElasticLayerClass):

    def __init__(self, cl: float, ct: float, rho: float, d: float, n: int = 16, name: str = 'layer'):
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
        n : int
            Number of collocation points, default 16
        name : str
            Layer's name (optional)
        """
        super(ElasticLayer, self).__init__(cl, ct, rho, d, n, name)

        self.lhs = np.array([])
        self.rhs = np.array([])
        self.sig = np.array([])
        self.eps = np.array([])

        self.__build__(self.n)

    def __build__(self, n: int):
        # TODO: continue here
        pass

    @classmethod
    def from_elastic_constants(cls, E: float, rho: float, nu: float, d: float, n: int = 16, name: str = "layer"):
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
        n : int
            Number of collocation points, default 16
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

        if isinstance(d, (float, int)):
            if d > 0:
                d = float(d)
            else:
                raise ValueError(f"'d' must be positive; got {d} instead.")
        else:
            raise TypeError(f"'d' must be of type 'float' or 'int'; got '{type(d).__name__}' instead.")

        if isinstance(n, int):
            if n > 0:
                n = int(n)
            else:
                raise ValueError(f"'n' must be positive; got {n} instead.")
        else:
            raise TypeError(f"'n' must be of type 'int'; got '{type(n).__name__}' instead.")

        if isinstance(name, str):
            name = str(name)
        else:
            raise TypeError(f"'name' must be of type 'str'; got '{type(name).__name__}' instead.")

        cl = np.sqrt((E * (1 - nu)) / (rho * (1 - nu - 2 * np.square(nu))))
        ct = np.sqrt(E / (2 * rho * (1 + nu)))

        return cls(cl, ct, rho, d, n, name)


if __name__ == '__main__':

    layer = ElasticLayer.from_elastic_constants(5, 13, 15, 4, n=16, name='hello')
    print(layer)
