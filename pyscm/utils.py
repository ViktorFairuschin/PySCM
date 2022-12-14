# Copyright Viktor Fairuschin 2022

import numpy as np
from scipy.linalg import toeplitz


def chebyshev_dm(n: int, m: int) -> (np.ndarray, np.ndarray):
    """Compute Chebyshev differentiation matrices.

    Parameters
    ----------
    n : int
        Number of collocation points.
    m : int
        Order of the highest derivative.

    Returns
    -------
    x : array of shape (n)
        Chebyshev collocation points.
    dm : array of shape (m, n, n)
        Chebyshev differentiation matrices.
    """

    x = np.cos(np.pi * np.linspace(n - 1, 0, n) / (n - 1))
    x = x[::-1]

    dm = np.zeros((m, n, n))

    n1 = int(n / 2)
    n2 = int(round(n / 2.))
    k = np.arange(n)
    th = k * np.pi / (n - 1)

    T = np.tile(th / 2, (n, 1))
    dx = 2 * np.sin(T.T + T) * np.sin(T.T - T)
    dx[n1:, :] = -np.flipud(np.fliplr(dx[0:n2, :]))
    dx[range(n), range(n)] = 1.
    dx = dx.T

    c = toeplitz((-1.) ** k)
    c[0, :] *= 2
    c[-1, :] *= 2
    c[:, 0] *= 0.5
    c[:, -1] *= 0.5

    z = 1. / dx
    z[range(n), range(n)] = 0.

    d = np.eye(n)

    for ell in range(m):
        d = (ell + 1) * z * (c * np.tile(np.diag(d), (n, 1)).T - d)
        d[range(n), range(n)] = -np.sum(d, axis=1)
        dm[ell, :, :] = d

    return x, dm

