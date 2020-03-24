from typing import Union, Tuple
from math import cos, sin
from .utils import Coordinate, Matrix, deg2rad

__all__ = [
    "shearing_matrix",
    "rotation_matrix",
    "scaling_matrix",
    "translation_matrix",
]


def shearing_matrix(angle: float, clockwise: bool = False) -> Matrix:
    angle = deg2rad(angle)
    if clockwise:
        angle *= -1.0
    return (1.0, -sin(angle), 0.0, 0.0, cos(angle), 0.0)


def rotation_matrix(angle: float, clockwise: bool = False) -> Matrix:
    angle = deg2rad(angle)
    if clockwise:
        angle *= -1.0
    return (cos(angle), -sin(angle), 0.0, sin(angle), cos(angle), 0.0)


def scaling_matrix(factor: Union[float, Tuple[float, float]]) -> Matrix:
    if isinstance(factor, float):
        factor_horz = factor_vert = factor
    else:
        factor_horz, factor_vert = factor
    return (factor_horz, 0.0, 0.0, 0.0, factor_vert, 0.0)


def translation_matrix(translation: Coordinate, inverse: bool = False) -> Matrix:
    horz_translation, vert_translation = translation
    if inverse:
        horz_translation *= -1.0
        vert_translation *= -1.0
    return (1.0, 0.0, horz_translation, 0.0, 1.0, vert_translation)
