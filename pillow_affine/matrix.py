from typing import Union, Tuple
from functools import reduce
import numpy as np
from numpy.linalg import inv, norm

__all__ = [
    "left_matmuls",
    "inv",
    "verify_matrix",
    "shearing_matrix",
    "rotation_matrix",
    "scaling_matrix",
    "translation_matrix",
]


def left_matmuls(*matrices: np.ndarray) -> np.ndarray:
    return reduce(lambda x1, x2: np.matmul(x2, x1), matrices)


def verify_matrix(matrix: np.ndarray, eps: float = 1e-6) -> None:
    if not isinstance(matrix, np.ndarray):
        # TODO: add message
        raise RuntimeError
    elif matrix.dtype not in (np.half, np.single, np.double, np.longdouble):
        # TODO: add message
        raise RuntimeError
    elif matrix.shape != (3, 3):
        # TODO: add message
        raise RuntimeError
    elif norm(matrix[-1, :] - np.array((0.0, 0.0, 1.0))) > eps:
        # TODO: add message
        raise RuntimeError


def shearing_matrix(angle: float, clockwise: bool = False) -> np.ndarray:
    angle = np.deg2rad(angle)
    if clockwise:
        angle *= -1.0
    matrix = (
        (1.0, -np.sin(angle), 0.0),
        (0.0, np.cos(angle), 0.0),
        (0.0, 0.0, 1.0),
    )
    return np.array(matrix)


def rotation_matrix(angle: float, clockwise: bool = False) -> np.ndarray:
    angle = np.deg2rad(angle)
    if clockwise:
        angle *= -1.0
    matrix = (
        (np.cos(angle), -np.sin(angle), 0.0),
        (np.sin(angle), np.cos(angle), 0.0),
        (0.0, 0.0, 1.0),
    )
    return np.array(matrix)


def scaling_matrix(factor: Union[float, Tuple[float, float]]) -> np.array:
    if isinstance(factor, float):
        factor_horz = factor_vert = factor
    else:
        factor_horz, factor_vert = factor
    matrix = ((factor_horz, 0.0, 0.0), (0.0, factor_vert, 0.0), (0.0, 0.0, 1.0))
    return np.array(matrix)


def translation_matrix(
    translation: Tuple[float, float], inverse: bool = False
) -> np.array:
    horz_translation, vert_translation = translation
    if inverse:
        horz_translation *= -1.0
        vert_translation *= -1.0
    matrix = (
        (1.0, 0.0, horz_translation),
        (0.0, 1.0, vert_translation),
        (0.0, 0.0, 1.0),
    )
    return np.array(matrix)
