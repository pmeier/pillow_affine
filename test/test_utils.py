import unittest
import random
import numpy as np
from pillow_affine import utils


def randn(mu=0.0, sigma=1.0):
    return random.gauss(mu, sigma)


def random_matrix(seed=None):
    if seed is not None:
        random.seed(seed)
    return tuple([randn() for _ in range(6)])


def convert_matrix_to_numpy(pil_matrix):
    a, b, c, d, e, f = pil_matrix
    return np.array(((a, b, c), (d, e, f), (0.0, 0.0, 1.0)))


class Tester(unittest.TestCase):
    def assertMatrixAlmostEqual(self, matrix1, matrix2, **kwargs):
        def cast(matrix):
            if isinstance(matrix, np.ndarray):
                return matrix

            return convert_matrix_to_numpy(matrix)

        np.testing.assert_allclose(cast(matrix1), cast(matrix2), **kwargs)

    def test_matmul(self):
        random.seed(0)

        pil_matrix1 = random_matrix()
        pil_matrix2 = random_matrix()

        numpy_matrix1 = convert_matrix_to_numpy(pil_matrix1)
        numpy_matrix2 = convert_matrix_to_numpy(pil_matrix2)

        actual = utils.matmul(pil_matrix1, pil_matrix2)
        desired = np.matmul(numpy_matrix1, numpy_matrix2)
        self.assertMatrixAlmostEqual(actual, desired)

    def test_left_matmuls(self):
        random.seed(0)

        pil_matrix1 = random_matrix()
        pil_matrix2 = random_matrix()
        pil_matrix3 = random_matrix()

        numpy_matrix1 = convert_matrix_to_numpy(pil_matrix1)
        numpy_matrix2 = convert_matrix_to_numpy(pil_matrix2)
        numpy_matrix3 = convert_matrix_to_numpy(pil_matrix3)

        actual = utils.left_matmuls(pil_matrix1, pil_matrix2, pil_matrix3)
        desired = np.matmul(numpy_matrix3, np.matmul(numpy_matrix2, numpy_matrix1))
        self.assertMatrixAlmostEqual(actual, desired)

    def test_matinv(self):
        pil_matrix = random_matrix(seed=0)
        numpy_matrix = convert_matrix_to_numpy(pil_matrix)

        actual = utils.matinv(pil_matrix)
        desired = np.linalg.inv(numpy_matrix)
        self.assertMatrixAlmostEqual(actual, desired)

    def test_deg2rad(self):
        angles = (0.0, 90.0, -90.0, 30.0, 360.0, -360.0, 720.0)

        actual = np.array([utils.deg2rad(angle) for angle in angles])
        desired = np.deg2rad(np.array(angles)) % (2 * np.pi)
        np.testing.assert_allclose(actual, desired)

    def test_transform_coordinate(self):
        random.seed(0)

        pil_coordinate = (randn(), randn())
        pil_matrix = random_matrix()

        numpy_coordinate = np.array((*pil_coordinate, 1.0))
        numpy_matrix = convert_matrix_to_numpy(pil_matrix)

        actual = np.array(utils.transform_coordinate(pil_coordinate, pil_matrix))
        desired = np.matmul(numpy_matrix, numpy_coordinate)[:-1]
        np.testing.assert_allclose(actual, desired)
