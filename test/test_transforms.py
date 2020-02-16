from typing import Tuple
from os import path
import unittest
from pyimagetest import ImageTestcase
import numpy as np
from pillow_affine import transforms


def convert_angle(angle: float, clockwise: bool = False) -> float:
    return -angle if clockwise else angle


def convert_center(
    center: Tuple[float, float], size: Tuple[int, int]
) -> Tuple[float, float]:
    width, height = size
    return center[0], height - center[1]


def convert_translation(
    translation: Tuple[float, float], inverse: bool = False
) -> Tuple[float, float]:
    translate = translation[0], -translation[1]
    if inverse:
        translate = (-translate[0], -translate[1])
    return translate


class Tester(ImageTestcase, unittest.TestCase):
    @property
    def default_test_image_file(self) -> str:
        # The test image was downloaded from
        # http://www.r0k.us/graphics/kodak/kodim15.html
        # and is cleared for unrestricted usage
        here = path.abspath(path.dirname(__file__))
        return path.join(here, "test_image.png")

    def test_rotate(self):
        image = self.load_image("PIL")
        angle = 30.0

        transform = transforms.Rotate(angle)
        transform_params = transform.extract_transform_params(image.size)
        actual = image.transform(*transform_params)

        desired = image.rotate(convert_angle(angle))

        self.assertImagesAlmostEqual(actual, desired)

    def test_rotate_clockwise(self):
        image = self.load_image("PIL")
        angle = 30.0
        clockwise = True

        transform = transforms.Rotate(angle, clockwise=clockwise)
        transform_params = transform.extract_transform_params(image.size)
        actual = image.transform(*transform_params)

        desired = image.rotate(convert_angle(angle, clockwise=clockwise))

        self.assertImagesAlmostEqual(actual, desired)

    def test_rotate_off_image_center(self):
        image = self.load_image("PIL")
        angle = 30.0
        image_center = transforms.calculate_image_center(image.size)
        center = (image_center[0] - 50.0, image_center[1] + 100.0)

        transform = transforms.Rotate(angle, center=center)
        transform_params = transform.extract_transform_params(image.size)
        actual = image.transform(*transform_params)

        desired = image.rotate(angle, center=convert_center(center, image.size))

        self.assertImagesAlmostEqual(actual, desired)

    def test_translate(self):
        image = self.load_image("PIL")
        translation = (100.0, 50.0)

        transform = transforms.Translate(translation)
        transform_params = transform.extract_transform_params(image.size)
        actual = image.transform(*transform_params)

        desired = image.rotate(0.0, translate=convert_translation(translation))

        self.assertImagesAlmostEqual(actual, desired)

    def test_translate_inverse(self):
        image = self.load_image("PIL")
        translation = (100.0, 50.0)
        inverse = True

        transform = transforms.Translate(translation, inverse=inverse)
        transform_params = transform.extract_transform_params(image.size)
        actual = image.transform(*transform_params)

        desired = image.rotate(
            0.0, translate=convert_translation(translation, inverse=inverse)
        )

        self.assertImagesAlmostEqual(actual, desired)

    def test_affine(self):
        image = self.load_image("PIL")
        angle = 30.0
        translation = (100.0, 50.0)

        transform = transforms.ComposedTransform(
            transforms.Rotate(angle), transforms.Translate(translation),
        )
        transform_params = transform.extract_transform_params(image.size)
        actual = image.transform(*transform_params)

        angle = convert_angle(angle)
        translate = convert_translation(translation)
        desired = image.rotate(angle, translate=translate)

        self.assertImagesAlmostEqual(actual, desired)


if __name__ == "__main__":
    unittest.main()
