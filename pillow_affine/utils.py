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
    r"""Matrix product

    .. math::

        \begin{pmatrix}
            a_1 & b_1 & c_1 \\
            d_1 & e_1 & f_1 \\
            0   & 0   & 1 \\
        \end{pmatrix}
        \cdot
        \begin{pmatrix}
            a_2 & b_2 & c_2 \\
            d_2 & e_2 & f_2 \\
            0   & 0   & 1 \\
        \end{pmatrix}
        =
        \begin{pmatrix}
            a & b & c \\
            d & e & f \\
            0 & 0 & 1 \\
        \end{pmatrix}


    Args:
        matrix1: Parameters :math:`a_1`, :math:`b_1`, :math:`c_1`, :math:`d_1`,
            :math:`e_1`, :math:`f_1`.
        matrix2: Parameters :math:`a_2`, :math:`b_2`, :math:`c_2`, :math:`d_2`,
            :math:`e_2`, :math:`f_2`.

    Returns:
        Parameters :math:`a`, :math:`b`, :math:`c`, :math:`d`, :math:`e`,
        :math:`f`.
    """
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
    r"""Matrix product of :math:`N` matrices from the left

    .. math::

        \begin{pmatrix}
            a_N & b_N & c_N \\
            d_N & e_N & f_N \\
            0   & 0   & 1 \\
        \end{pmatrix}
        \cdot
        \quad\dots\quad
        \cdot
        \begin{pmatrix}
            a_n & b_n & c_n \\
            d_n & e_n & f_n \\
            0   & 0   & 1 \\
        \end{pmatrix}
        \quad\dots\quad
        \cdot
        \begin{pmatrix}
            a_1 & b_1 & c_1 \\
            d_1 & e_1 & f_1 \\
            0   & 0   & 1 \\
        \end{pmatrix}
        =
        \begin{pmatrix}
            a & b & c \\
            d & e & f \\
            0 & 0 & 1 \\
        \end{pmatrix}

    Args:
        *matrices: Parameters :math:`a_n`, :math:`b_n`, :math:`c_n`, :math:`d_n`,
            :math:`e_n`, :math:`f_n` of each matrix.

    Returns:
        Parameters :math:`a`, :math:`b`, :math:`c`, :math:`d`, :math:`e`,
        :math:`f`.
    """
    return reduce(lambda matrix1, matrix2: matmul(matrix2, matrix1), matrices)


def matinv(matrix: Matrix) -> Matrix:
    r"""Matrix inverse

    .. math::

        \begin{pmatrix}
            a & b & c \\
            d & e & f \\
            0 & 0 & 1 \\
        \end{pmatrix}^{-1}
        =
        \begin{pmatrix}
            a^\prime & b^\prime & c^\prime \\
            d^\prime & e^\prime & f^\prime \\
            0        & 0        & 1 \\
        \end{pmatrix}

    Args:
        matrix: Parameters :math:`a`, :math:`b`, :math:`c`, :math:`d`, :math:`e`,
            :math:`f`.

    Returns:
        Parameters :math:`a^\prime`, :math:`b^\prime`, :math:`c^\prime`,
        :math:`d^\prime`, :math:`e^\prime`, :math:`f^\prime`.
    """
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
    """Converts an angle from degrees to radians

    Args:
        angle_in_deg: Angle in degrees.

    Returns:
        Angle in radians.
    """
    factor = pi / 180.0
    # FIXME: remove module operation
    return (angle_in_deg % 360.0) * factor


def transform_coordinate(coordinate: Coordinate, matrix: Matrix) -> Coordinate:
    r"""Transforms a ``coordinate`` based on an affine ``matrix``

    .. math::

        \begin{pmatrix}
            a & b & c \\
            d & e & f \\
            0 & 0 & 1 \\
        \end{pmatrix}
        \cdot
        \begin{pmatrix}
            x \\
            y \\
            1 \\
        \end{pmatrix}
        =
        \begin{pmatrix}
            x^\prime \\
            y^\prime \\
            1 \\
        \end{pmatrix}

    Args:
        coordinate: Coordinate (:math:`x`, :math:`y`).
        matrix: Affine parameters :math:`a`, :math:`b`, :math:`c`, :math:`d`,
            :math:`e`, :math:`f`.

    Returns:
        Transformed coordinate (:math:`x^\prime`, :math:`y^\prime`).
    """
    x, y = coordinate
    a, b, c, d, e, f = matrix

    xtrans = a * x + b * y + c
    ytrans = d * x + e * y + f

    return (xtrans, ytrans)
