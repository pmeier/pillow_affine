from typing import Tuple
from functools import reduce
from math import pi

__all__ = [
    "Coordinate",
    "Matrix",
    "matmul",
    "left_matmuls",
    "matinv",
    "deg2rad",
    "transform_coordinate",
]

Coordinate = Tuple[float, float]
Matrix = Tuple[float, float, float, float, float, float]


def matmul(matrix1: Matrix, matrix2: Matrix) -> Matrix:
    a1, b1, c1, d1, e1, f1 = matrix1
    a2, b2, c2, d2, e2, f2 = matrix2

    a = a1 * a2 + b1 * d2
    b = a1 * b2 + b1 * e2
    c = a1 * c2 + b1 * f2 + c1
    d = d1 * a2 + e1 * d2
    e = d1 * b2 + e1 * e2
    f = d1 * c2 + e1 * f2 + f1

    return (a, b, c, d, e, f)


def left_matmuls(*matrices: Matrix) -> Matrix:
    return reduce(lambda matrix1, matrix2: matmul(matrix2, matrix1), matrices)


def matinv(matrix: Matrix) -> Matrix:
    a, b, c, d, e, f = matrix

    det = a * e - b * d
    ainv = e / det
    binv = -b / det
    cinv = (b * f - c * e) / det
    dinv = -d / det
    einv = a / det
    finv = (c * d - a * f) / det

    return (ainv, binv, cinv, dinv, einv, finv)


def deg2rad(angle_in_deg: float) -> float:
    factor = pi / 180.0
    return (angle_in_deg % 360.0) * factor


def transform_coordinate(coordinate: Coordinate, matrix: Matrix) -> Coordinate:
    x, y = coordinate
    a, b, c, d, e, f = matrix

    xtrans = a * x + b * y + c
    ytrans = d * x + e * y + f

    return (xtrans, ytrans)
