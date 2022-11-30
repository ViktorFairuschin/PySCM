# Copyright Viktor Fairuschin 2022

import numpy as np

import matplotlib.pyplot as plt
from matplotlib import ticker

from pyscm.layers import ElasticLayer
from pyscm.waveguides import WaveGuide


waveguide = WaveGuide([
    ElasticLayer(6350, 3100, 2700, 2e-3, 'AL'),
    # ElasticLayer(6350, 3100, 2700, 2e-3, 'AL')
]).build(n=16)


def flag_modes(k, u, n_layers):
    """Description.
    """
    n = int(len(k) / n_layers / 4)

    results = []
    for i in np.argwhere(~np.isnan(k)).flatten():
        vec = u[(n * 2 * n_layers):(n * 2 * n_layers + n), i]
        mid = int(n / 2)
        if np.sign(vec[0] - vec[mid]) == np.sign(vec[-1] - vec[mid]):
            flag = 'S'
        else:
            flag = 'A'
        results.append((k[i], flag))

    return results


fig, ax = plt.subplots()


for f in np.linspace(1, 1.0e7, 100):
    k, u = waveguide(f)
    results = flag_modes(k, u, len(waveguide.layers))

    for k, flag in results:
        cph = 2 * np.pi * f / k
        color = 'red' if flag == 'A' else 'blue'
        ax.scatter(f, cph, color=color, s=5, alpha=1)

ax.set_title('aluminium 2 mm')

ax.spines.right.set_color('none')
ax.spines.top.set_color('none')
ax.spines.left.set_position(('outward', 10))
ax.spines.bottom.set_position(('outward', 10))

ax.xaxis.set_major_locator(ticker.MultipleLocator(1e6))
ax.xaxis.set_minor_locator(ticker.MultipleLocator(5e5))
ax.xaxis.set_major_formatter(lambda x, pos: str(x / 1e6))
ax.set_xlabel('frequency (MHz)')
ax.set_xlim(0, 1e7)

ax.yaxis.set_major_locator(ticker.MultipleLocator(1e3))
ax.yaxis.set_minor_locator(ticker.MultipleLocator(5e2))
ax.yaxis.set_major_formatter(lambda y, pos: str(y / 1e3))
ax.set_ylabel('phase velocity (km/s)')
ax.set_ylim(0, 1e4)

fig.tight_layout()
plt.show()
