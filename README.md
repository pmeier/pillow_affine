[![Build Status](https://travis-ci.org/pmeier/pillow_affine.svg?branch=master)](https://travis-ci.org/pmeier/pillow_affine) [![codecov](https://codecov.io/gh/pmeier/pillow_affine/branch/master/graph/badge.svg)](https://codecov.io/gh/pmeier/pillow_affine) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# pillow_affine

`pillow_affine` provides affine transformation utilities for `Pillow`. While `Pillow` provides the functionality for affine transformations
```python
from PIL import Image

image = Image.new("L", (512, 512), color=255)
image.transform(image.size, Image.AFFINE, data=???)
```
the `data` parameter is not well documented. Even if you are familiar with affine transformations, it is inconvenient to use. `pillow_affine` can help with that by providing an intuitive and convenient interface:

```python
from PIL import Image
from pillow_affine import transforms

transform = transforms.Rotate(30.0)

image = Image.new("L", (512, 512), color=255)
transform_params = transform.extract_transform_params(image.size)
image.transform(*transform_params)
```

Similar to `image.rotate()`, `transform.extract_transform_params()` provides an `expand` flag, which if `True` enlarges the image to hold the complete motif. Be aware that this centers the motif and thus any final translation is removed.

## Coordinate System

| ATTENTION: `pillow_affine` uses a different, presumably more intuitive, coordinate system than `Pillow`. |
| --- |

|                               | `Pillow`   | `pillow_affine` |
| ----------------------------- | ---------- | --------------- |
| origin, i.e. `(0.0, 0.0)`     | top-left   | bottom-left     |
| horizontal positive direction | rightwards | rightwards      |
| vertical positive direction   | downwards  | upwards         |


## How it works

Every affine transformation is build from 4 `ElementaryTransform`s:

- `Shear`
- `Rotate`
- `Scale`
- `Translate`

They are combined within a `ComposedTransform`. 

You can find examples of the effect of the `ElementaryTransform`s as well as examplary `ComposedTransform`s on the following image below.

![](images/raw.png "girl with painted face - Steve Kelly")

### `Shear`

```python
from pillow_affine import Shear

transform1 = Shear(30.0)
transform2 = Shear(30.0, clockwise=True)
transform3 = Shear(30.0, center=(0.0, 0.0))
```

![](images/shear.png "Shear(30.0)") ![](images/shear_clockwise.png "Shear(30.0, clockwise=True)") ![](images/shear_off_center.png "Shear(30.0, center=(0.0, 0.0))")

### `Rotate`

```python
from pillow_affine import Rotate

transform1 = Rotate(30.0)
transform2 = Rotate(30.0, clockwise=True)
transform3 = Rotate(30.0, center=(0.0, 0.0))
```

![](images/rotate.png "Rotate(30.0)") ![](images/rotate_clockwise.png "Rotate(30.0, clockwise=True)") ![](images/rotate_off_center.png "Rotate(30.0, center=(0.0, 0.0))")

### `Scale`

```python
from pillow_affine import Scale

transform1 = Scale(2.0)
transform2 = Scale((0.3, 1.0))
transform3 = Scale(0.5, center=(0.0, 0.0))
```

![](images/scale.png "Scale(2.0)") ![](images/scale_async.png "Scale((0.3, 1.0))") ![](images/scale_off_center.png "Rotate(0.5, center=(0.0, 0.0))")

### `Translate`

```python
from pillow_affine import Translate

transform1 = Translate((100.0, 50.0))
transform2 = Translate((100.0, 50.0), inverse=True)
```

![](images/translate.png "Scale(2.0)") ![](images/translate_inverse.png "Scale((0.3, 1.0))") 

### `ComposedTransform`

```python
from pillow_affine import Shear, Rotate, Scale, Translate, ComposedTransform

transform1 = ComposedTransform(
    Shear(45.0),
    Rotate(30.0),
    Scale(0.7),
)
transform2 = ComposedTransform(
    Scale((0.3, 0.7)),
    Rotate(70.0, clockwise=True),
    Translate((50.0, 20.0))
)
```

![](images/composed_1.png "Scale(2.0)") ![](images/composed_2.png "Scale((0.3, 1.0))") 

### `Expand`

```python
from pillow_affine import Shear

transform = Shear(30.0)
transform_params1 = transform.extract_transform_params(size)
transform_params2 = transform.extract_transform_params(size, expand=True)

```

![](images/shear.png "Shear(30.0) with expand=False") ![](images/shear_expand.png "Shear(30.0) with expand=True") 

