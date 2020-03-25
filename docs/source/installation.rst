Installation
============

``pillow_affine`` is a proper Python package and listed on
`PyPI <https://pypi.org/project/pillow_affine/>`_. To install the latest stable
version run

.. code-block:: sh

  pip install pillow_affine

To install the latest unreleased version from source run

.. code-block:: sh

  git clone https://github.com/pmeier/pillow_affine
  cd pillow_affine
  pip install .


Installation for developers
---------------------------

If you want to contribute to ``pillow_affine`` please install from source with the
``[dev]`` extra in order to install all required development tools.

.. code-block:: sh

  git clone https://github.com/pmeier/pyimagetest
  cd pyimagetest
  pip install .[dev]


Since ``pillow_affine`` uses the 
`black code formatter <https://github.com/psf/black>`_, you should install it as
a pre-commit hook:

.. code-block:: sh

  pre-commit install
