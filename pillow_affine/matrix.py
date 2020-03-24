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
    r"""Creates an affine horizontal shearing matrix in the form

    .. math::

        \mathrm{\mathbf{S}} =
        \begin{pmatrix}
            1 & - \sin \varphi & 0 \\
            0 & \cos \varphi   & 0 \\
            0 & 0              & 1 \\
        \end{pmatrix}
        =
        \begin{pmatrix}
            a & b & c \\
            d & e & f \\
            0 & 0 & 1 \\
        \end{pmatrix}

    Args:
        angle: Angle :math:`\varphi` in degrees.
        clockwise: If ``True``, the shearing will be performed clockwise.
            Defaults to ``False``.

    Returns:
        Parameters :math:`a`, :math:`b`, :math:`c`, :math:`d`, :math:`e`,
        :math:`f`.
    """
    angle = deg2rad(angle)
    if clockwise:
        angle *= -1.0
    return (1.0, -sin(angle), 0.0, 0.0, cos(angle), 0.0)


def rotation_matrix(angle: float, clockwise: bool = False) -> Matrix:
    r"""Creates an affine rotation matrix in the form

    .. math::

        \mathrm{\mathbf{R}} =
        \begin{pmatrix}
            \cos \varphi & - \sin \varphi & 0 \\
            \sin \varphi & \cos \varphi   & 0 \\
            0            & 0              & 1 \\
        \end{pmatrix}
        =
        \begin{pmatrix}
            a & b & c \\
            d & e & f \\
            0 & 0 & 1 \\
        \end{pmatrix}

    Args:
        angle: Angle :math:`\varphi` in degrees.
        clockwise: If ``True``, the rotation will be performed clockwise.
            Defaults to ``False``.

    Returns:
        Parameters :math:`a`, :math:`b`, :math:`c`, :math:`d`, :math:`e`,
        :math:`f`.
    """
    angle = deg2rad(angle)
    if clockwise:
        angle *= -1.0
    return (cos(angle), -sin(angle), 0.0, sin(angle), cos(angle), 0.0)


def scaling_matrix(factor: Union[float, Tuple[float, float]]) -> Matrix:
    r"""Creates an affine scaling matrix in the form

    .. math::

        \mathrm{\mathbf{C}} =
        \begin{pmatrix}
            c_\text{horz} &               & 0 \\
            0             & c_\text{vert} & 0 \\
            0             & 0             & 1 \\
        \end{pmatrix}
        =
        \begin{pmatrix}
            a & b & c \\
            d & e & f \\
            0 & 0 & 1 \\
        \end{pmatrix}

    Args:
        factor: Horizontal and vertical scaling factors
            (:math:`c_\text{horz}`, :math:`c_\text{vert}`). If scalar, the
            same factor is used for both directions.

    Returns:
        Parameters :math:`a`, :math:`b`, :math:`c`, :math:`d`, :math:`e`,
        :math:`f`.
    """
    if isinstance(factor, float):
        factor_horz = factor_vert = factor
    else:
        factor_horz, factor_vert = factor
    return (factor_horz, 0.0, 0.0, 0.0, factor_vert, 0.0)


def translation_matrix(translation: Coordinate, inverse: bool = False) -> Matrix:
    r"""Creates an affine scaling matrix in the form

    .. math::

        \mathrm{\mathbf{T}} =
        \begin{pmatrix}
            1 & 0 & t_\text{horz} \\
            0 & 1 & t_\text{vert} \\
            0 & 0 & 1 \\
        \end{pmatrix}
        =
        \begin{pmatrix}
            a & b & c \\
            d & e & f \\
            0 & 0 & 1 \\
        \end{pmatrix}

    Args:
        translation: Horizontal and vertical translation.
            (:math:`t_\text{horz}`, :math:`t_\text{vert}`)
        inverse: If ``True``, the translation will be performed in the opposite
            direction. Defaults to ``False``.

    Returns:
        Parameters :math:`a`, :math:`b`, :math:`c`, :math:`d`, :math:`e`,
        :math:`f`.
    """
    horz_translation, vert_translation = translation
    if inverse:
        horz_translation *= -1.0
        vert_translation *= -1.0
    return (1.0, 0.0, horz_translation, 0.0, 1.0, vert_translation)
