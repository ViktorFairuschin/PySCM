# Copyright Viktor Fairuschin 2022

import pytest

from pyscm.layers import ElasticLayer
from pyscm.waveguides import WaveGuide


def test_init_default_waveguide():
    waveguide = WaveGuide()
    assert waveguide.name == 'waveguide'
    assert len(waveguide.layers) == 0


def test_init_raises_type_error():
    with pytest.raises(TypeError):
        _ = WaveGuide(name=3)


def test_init_waveguide_with_layers():
    waveguide = WaveGuide([
        ElasticLayer(cl=1, ct=1, rho=1, d=1, name='name')
    ])
    assert len(waveguide.layers) == 1


def test_add():
    waveguide = WaveGuide()
    waveguide.add(ElasticLayer(cl=1, ct=1, rho=1, d=1, name='name'))
    assert len(waveguide.layers) == 1


def test_add_raises_type_error():
    with pytest.raises(TypeError):
        _ = WaveGuide().add(5)


def test_build():
    waveguide = WaveGuide([
        ElasticLayer(cl=1, ct=1, rho=1, d=1, name='name')
    ]).build(n=16)
    assert waveguide.is_build


def test_build_raises_value_error():
    with pytest.raises(ValueError):
        _ = WaveGuide([
            ElasticLayer(cl=1, ct=1, rho=1, d=1, name='name')
        ]).build(n=0)


def test_build_raises_type_error():
    with pytest.raises(TypeError):
        _ = WaveGuide([
            ElasticLayer(cl=1, ct=1, rho=1, d=1, name='name')
        ]).build(n=5.3)


def test_output_shape():
    waveguide = WaveGuide([
        ElasticLayer(cl=1, ct=1, rho=1, d=1, name='name')
    ]).build(n=16)
    k, u = waveguide(f=1)
    assert k.shape == (64,)
    assert u.shape == (64, 64)


def test_call_raises_type_error():
    with pytest.raises(TypeError):
        waveguide = WaveGuide([
            ElasticLayer(cl=1, ct=1, rho=1, d=1, name='name')
        ]).build(n=16)
        _, _ = waveguide(f='a')


def test_call_raises_value_error():
    with pytest.raises(ValueError):
        waveguide = WaveGuide([
            ElasticLayer(cl=1, ct=1, rho=1, d=1, name='name')
        ]).build(n=16)
        _, _ = waveguide(f=-1)


def test_call_raises_runtime_error():
    with pytest.raises(RuntimeError):
        waveguide = WaveGuide([
            ElasticLayer(cl=1, ct=1, rho=1, d=1, name='name')
        ])
        _, _ = waveguide(f=1.0e6)


