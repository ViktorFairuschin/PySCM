# Copyright Viktor Fairuschin 2022

import pytest

from pyscm.layers import ElasticLayer


def test_setting_elastic_layers_properties():
    layer = ElasticLayer(cl=1, ct=1, rho=1, d=1, name='name')
    assert layer.cl == 1
    assert layer.ct == 1
    assert layer.rho == 1
    assert layer.d == 1
    assert layer.name == 'name'


def test_elastic_layers_output_shape():
    layer = ElasticLayer(cl=1, ct=1, rho=1, d=1, name='name')
    n = 16
    lhs, rhs, sig, eps = layer(n)
    assert lhs.shape == (3, 2 * n, 2 * n)
    assert rhs.shape == (2 * n, 2 * n)
    assert sig.shape == (3, 2 * n, 2 * n)
    assert eps.shape == (3, 2 * n, 2 * n)


def test_elastic_layer_raises_value_error():
    with pytest.raises(ValueError):
        _ = ElasticLayer(cl=0, ct=1, rho=1, d=1, name='name')
        _ = ElasticLayer(cl=1, ct=0, rho=1, d=1, name='name')
        _ = ElasticLayer(cl=1, ct=1, rho=0, d=1, name='name')
        _ = ElasticLayer(cl=1, ct=1, rho=1, d=0, name='name')


def test_elastic_layer_raises_type_error():
    with pytest.raises(TypeError):
        _ = ElasticLayer(cl='e', ct=1, rho=1, d=1, name='name')
        _ = ElasticLayer(cl=1, ct='e', rho=1, d=1, name='name')
        _ = ElasticLayer(cl=1, ct=1, rho='e', d=1, name='name')
        _ = ElasticLayer(cl=1, ct=1, rho=1, d='e', name='name')
        _ = ElasticLayer(cl=1, ct=1, rho=1, d='e', name=0)

