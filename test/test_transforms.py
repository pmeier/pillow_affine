from typing import Tuple
from os import path
import unittest
import re
from pyimagetest import ImageTestcase
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


def has_valid_single_transform_repr(transform, special_chars=""):
    name = transform.__class__.__name__
    valid_extra_repr_chars = r"\w\s.,=()" + special_chars
    valid_pattern = name + f"[(][{valid_extra_repr_chars}]*[)]"
    return re.fullmatch(valid_pattern, repr(transform)) is not None


class Tester(ImageTestcase, unittest.TestCase):
    @property
    def default_test_image_file(self) -> str:
        here = path.abspath(path.dirname(__file__))
        return path.join(here, "..", "images", "raw.png")

    def test_AffineTransform(self):
        with self.assertRaises(TypeError):
            transforms.AffineTransform()

    def test_ElementaryTransform(self):
        with self.assertRaises(TypeError):
            transforms.ElementaryTransform()

    def test_Shear(self):
        angle = 30.0

        transform = transforms.Shear(angle)
        self.assertTrue(has_valid_single_transform_repr(transform, special_chars="°"))

    def test_Shear_clockwise(self):
        angle = 30.0
        clockwise = True

        transform = transforms.Shear(angle, clockwise=clockwise)
        self.assertTrue(has_valid_single_transform_repr(transform, special_chars="°"))

    def test_Shear_off_image_center(self):
        angle = 30.0
        center = (0.0, 0.0)

        transform = transforms.Shear(angle, center=center)
        self.assertTrue(has_valid_single_transform_repr(transform, special_chars="°"))

    def test_Rotate(self):
        image = self.load_image("PIL")
        angle = 30.0

        transform = transforms.Rotate(angle)
        transform_params = transform.extract_transform_params(image.size)
        actual = image.transform(*transform_params)

        desired = image.rotate(convert_angle(angle))

        self.assertImagesAlmostEqual(actual, desired)
        self.assertTrue(has_valid_single_transform_repr(transform, special_chars="°"))

    def test_Rotate_clockwise(self):
        image = self.load_image("PIL")
        angle = 30.0
        clockwise = True

        transform = transforms.Rotate(angle, clockwise=clockwise)
        transform_params = transform.extract_transform_params(image.size)
        actual = image.transform(*transform_params)

        desired = image.rotate(convert_angle(angle, clockwise=clockwise))

        self.assertImagesAlmostEqual(actual, desired)
        self.assertTrue(has_valid_single_transform_repr(transform, special_chars="°"))

    def test_Rotate_off_image_center(self):
        image = self.load_image("PIL")
        angle = 30.0
        image_center = transforms.calculate_image_center(image.size)
        center = (image_center[0] - 50.0, image_center[1] + 100.0)

        transform = transforms.Rotate(angle, center=center)
        transform_params = transform.extract_transform_params(image.size)
        actual = image.transform(*transform_params)

        desired = image.rotate(angle, center=convert_center(center, image.size))

        self.assertImagesAlmostEqual(actual, desired)
        self.assertTrue(has_valid_single_transform_repr(transform, special_chars="°"))

    def test_Scale(self):
        factor = 0.5

        transform = transforms.Scale(factor)
        self.assertTrue(has_valid_single_transform_repr(transform))

    def test_Scale_async(self):
        factor = (0.5, 2.0)

        transform = transforms.Scale(factor)
        self.assertTrue(has_valid_single_transform_repr(transform))

    def test_Scale_off_image_center(self):
        factor = 0.5
        center = (0.0, 0.0)

        transform = transforms.Scale(factor, center=center)
        self.assertTrue(has_valid_single_transform_repr(transform))

    def test_Translate(self):
        image = self.load_image("PIL")
        translation = (100.0, 50.0)

        transform = transforms.Translate(translation)
        transform_params = transform.extract_transform_params(image.size)
        actual = image.transform(*transform_params)

        desired = image.rotate(0.0, translate=convert_translation(translation))

        self.assertImagesAlmostEqual(actual, desired)
        self.assertTrue(has_valid_single_transform_repr(transform))

    def test_Translate_inverse(self):
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
        self.assertTrue(has_valid_single_transform_repr(transform))

    def test_empty_ComposedTransform(self):
        with self.assertRaises(RuntimeError):
            transforms.ComposedTransform()

    def test_ComposedTransform(self):
        image = self.load_image("PIL")
        angle = 30.0
        translation = (100.0, 50.0)

        transform = transforms.ComposedTransform(
            transforms.Rotate(angle), transforms.Translate(translation)
        )
        transform_params = transform.extract_transform_params(image.size)
        actual = image.transform(*transform_params)

        angle = convert_angle(angle)
        translate = convert_translation(translation)
        desired = image.rotate(angle, translate=translate)

        self.assertImagesAlmostEqual(actual, desired)

    def test_expand(self):
        image = self.load_image("PIL")
        angle = 30.0
        expand = True

        transform = transforms.Rotate(angle)
        transform_params = transform.extract_transform_params(image.size, expand=expand)
        actual = image.transform(*transform_params)

        desired = image.rotate(convert_angle(angle), expand=expand)

        self.assertImagesAlmostEqual(actual, desired)


if __name__ == "__main__":
    unittest.main()
