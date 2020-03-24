Coordinate system
=================

.. warning::
  ``pillow_affine`` uses a different, presumably more intuitive, coordinate
  system than ``Pillow``:

  =============================  ==========  =================
  Property                       ``Pillow``  ``pillow_affine``
  =============================  ==========  =================
  origin, i.e. `(0.0, 0.0)`      top-left    bottom-left
  horizontal positive direction  rightwards  rightwards
  vertical positive direction    downwards   upwards
  =============================  ==========  =================