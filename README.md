# PySCM

PySCM is a Python package for computation of dispersion 
diagrams of guided acoustic waves based on the spectral 
collocation method.

The currently available code is a quick and dirty implementation, which only serves to prove basic functionality. The first official version of the package is currently under development and will be made available here soon.

[//]: # (## Installation)

[//]: # ()
[//]: # (Coming soon.)

[//]: # ()
[//]: # (## Usage)

[//]: # ()
[//]: # (The basic building blocks of the PySCM package are layer )

[//]: # (objects. A layer object carries the information about its )

[//]: # (properties and geometry. The following code demonstrates )

[//]: # (how to create a layer object:)

[//]: # ()
[//]: # (```python)

[//]: # (from pyscm.layers import ElasticLayer)

[//]: # ()
[//]: # (aluminium = ElasticLayer&#40;cl=6350, ct=3100, rho=2700, d=0.001, name='AL'&#41;)

[//]: # (```)

[//]: # ()
[//]: # (Layer objects are in turn the basic building blocks of )

[//]: # (waveguides. Within a waveguide, any number of Layer )

[//]: # (objects can be stacked on top of each other. However, )

[//]: # (a waveguide must consist of at least one layer object. )

[//]: # (To add a layer object to a waveguide, the `.add&#40;&#41;` )

[//]: # (method can be used:)

[//]: # ()
[//]: # (```python)

[//]: # (from pyscm.waveguides import WaveGuide)

[//]: # ()
[//]: # (waveguide = WaveGuide&#40;name='my_waveguide'&#41;.add&#40;aluminium&#41;)

[//]: # (```)

[//]: # ()
[//]: # (Note that the order in which the layer objects are )

[//]: # (added to the waveguide matters. All layer objects of )

[//]: # (a waveguide are arranged in the order in which they )

[//]: # (were added to the waveguide from bottom to top, with )

[//]: # (the first added layer object being at the top position.)

[//]: # ()
[//]: # (It is not necessary to create the layer objects )

[//]: # (explicitly before adding them to the waveguide. Instead, )

[//]: # (a list of layer objects can be passed when creating a )

[//]: # (waveguide:)

[//]: # ()
[//]: # (```python)

[//]: # (waveguide = WaveGuide&#40;[)

[//]: # (    ElasticLayer&#40;cl=6350, ct=3100, rho=2700, d=0.001, name='AL'&#41;,)

[//]: # (    ElasticLayer&#40;cl=5850, ct=3230, rho=5850, d=0.002, name='ST'&#41;)

[//]: # (]&#41;)

[//]: # (```)

[//]: # ()
[//]: # (After the assembly of the waveguide has been completed, )

[//]: # (its differential equations must be build by calling the )

[//]: # (`.build&#40;&#41;` method. The `.build&#40;&#41;` method accepts as the )

[//]: # (only parameter the number of collocation points `n` used )

[//]: # (to solve the differential equations of the individual )

[//]: # (layers. Note that the total number of equations which )

[//]: # (is solved for a waveguide is equal to the number of )

[//]: # (layers multiplied by 2n.)

[//]: # ()
[//]: # (```python)

[//]: # (waveguide.build&#40;n=16&#41;)

[//]: # (```)

[//]: # ()
[//]: # (Thereafter, the wavenumbers of propagating modes at )

[//]: # (arbitrary frequencies can be determined:)

[//]: # ()
[//]: # (```python)

[//]: # (k = waveguide&#40;f=1.0e6&#41;)
[//]: # (```)