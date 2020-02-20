import unittest
import numpy as np
from pillow_affine.matrix import left_matmuls, verify_matrix


class Tester(unittest.TestCase):
    def test_left_matmuls(self):
        np.random.seed(0)
        x1 = np.random.rand(3, 3)
        x2 = np.random.rand(3, 3)
        x3 = np.random.rand(3, 3)

        actual = left_matmuls(x1, x2, x3)
        desired = np.matmul(x3, np.matmul(x2, x1))
        np.testing.assert_allclose(actual, desired)

    def test_verify_matrix(self):
        matrix = None
        with self.assertRaises(RuntimeError):
            verify_matrix(matrix)

        matrix = np.eye(3, dtype=np.int)
        with self.assertRaises(RuntimeError):
            verify_matrix(matrix)

        matrix = np.eye(4)
        with self.assertRaises(RuntimeError):
            verify_matrix(matrix)

        matrix = np.ones((3, 3))
        with self.assertRaises(RuntimeError):
            verify_matrix(matrix)

        matrix = np.eye(3)
        verify_matrix(matrix)


if __name__ == "__main__":
    unittest.main()
