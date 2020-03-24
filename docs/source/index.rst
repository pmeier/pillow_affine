Welcome to pillow_affine's documentation!
=========================================

``pillow_affine`` provides affine transformation utilities for ``Pillow``. While
``Pillow`` includes functionality for affine transformations

.. code-block:: python

  from PIL import Image

  image = Image.new("L", (512, 512), color=255)
  image.transform(image.size, Image.AFFINE, data=None)

the ``data`` parameter is not well documented. Even if you are familiar with
affine transformations, it is inconvenient to use. ``pillow_affine`` can help
with that by providing an intuitive and convenient interface::

  from PIL import Image
  from pillow_affine import transforms

  image = Image.open(...)
  transform = transforms.Rotate(30.0)

  transform_params = transform.extract_transform_params(image.size)
  image.transform(*transform_params)

``pillow_affine`` requires Python 3.6 or later. The code lives on
`GitHub <https://github.com/pmeier/pillow_affine>`_ and is licensed under the
`3-Clause BSD License <https://opensource.org/licenses/BSD-3-Clause>`_.

.. toctree::
  :maxdepth: 2

  Getting Started <getting_started>
  Reference <reference>
