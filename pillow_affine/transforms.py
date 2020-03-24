from typing import Union, Optional, Sequence, Tuple
from abc import ABC, abstractmethod
from math import floor, ceil
from PIL import Image
from .matrix import (
    shearing_matrix,
    rotation_matrix,
    scaling_matrix,
    translation_matrix,
)
from .utils import Coordinate, Matrix, left_matmuls, matinv, transform_coordinate

__all__ = [
    "AffineTransform",
    "Shear",
    "Rotate",
    "Scale",
    "Translate",
    "ComposedTransform",
]

Size = Tuple[int, int]


def calculate_image_center(size: Size) -> Coordinate:
    """Calculates the center of an image

    Args:
        size: Image size (width, height).

    Returns:
        Image center.
    """
    width, height = size
    horz_center = width / 2.0
    vert_center = height / 2.0
    return horz_center, vert_center


class AffineTransform(ABC):
    """ABC for all affine transformations.
    """

    @abstractmethod
    def _create_matrix(self, size: Size) -> Matrix:
        pass

    def extract_transform_params(
        self, size: Size, expand: bool = False
    ) -> Tuple[Size, int, Matrix]:
        """Extracts the transformation parameters that need to be passed to
        `Image.transform() <https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.transform>`_
        for the affine transformation. An simple call might look like::

            from PIL import Image
            from pillow_affine import transforms


            image = Image.open(...)
            transform = transforms.Rotate(30.0)

            transform_params = transform.extract_transform_params(image.size)
            transformed_image = image.transform(*transform_params)

        Args:
            size: Image size (width, height).
            expand: If ``True``, expands the canvas to hold the complete
                transformed motif. Defaults to ``False``.

        .. note::
            If you use the ``expand`` flag the motif is centered on the canvas
            and thus any final translation is removed.

        Returns:
            ``size``, ``method``, and ``data`` parameters for
            `Image.transform() <https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.transform>`_
             .
        """
        transform_matrix = self._create_matrix(size)

        if expand:
            expanded_size, transform_matrix = self._expand_canvas(
                size, transform_matrix
            )
        else:
            expanded_size = size

        transform_matrix = self._coordinate_system_transform(size, transform_matrix)

        data = self._extract_affine_data(transform_matrix)

        return expanded_size, Image.AFFINE, data

    @staticmethod
    def _expand_canvas(size: Size, transform_matrix: Matrix) -> Tuple[Size, Matrix]:
        def calculate_motif_vertices(transform_matrix: Matrix) -> Sequence[Coordinate]:
            width, height = size
            image_vertices = ((0.0, 0.0), (width, 0.0), (0.0, height), (width, height))
            return [
                transform_coordinate(coordinate, transform_matrix)
                for coordinate in image_vertices
            ]

        def calculate_expanded_size(motif_vertices: Sequence[Coordinate]) -> Size:
            xs, ys = zip(*motif_vertices)
            left = floor(min(xs))
            bottom = floor(min(ys))
            right = ceil(max(xs))
            top = ceil(max(ys))

            expanded_width = right - left
            expanded_height = top - bottom
            return expanded_width, expanded_height

        def recenter_motif(expanded_size: Size, transform_matrix: Matrix) -> Matrix:
            matrix = left_matmuls(
                translation_matrix(calculate_image_center(size), inverse=True),
                translation_matrix(calculate_image_center(expanded_size)),
            )
            # TODO: Investigate and document why this extra step is needed
            matrix = AffineTransform._coordinate_system_transform(size, matrix)
            return left_matmuls(transform_matrix, matrix)

        motif_vertices = calculate_motif_vertices(transform_matrix)
        expanded_size = calculate_expanded_size(motif_vertices)
        transform_matrix = recenter_motif(expanded_size, transform_matrix)

        return expanded_size, transform_matrix

    @staticmethod
    def _coordinate_system_transform(size: Size, transform_matrix: Matrix) -> Matrix:
        width, height = size
        matrix = (1.0, 0.0, 0.0, 0.0, -1.0, height)
        return left_matmuls(matrix, transform_matrix, matinv(matrix))

    @staticmethod
    def _extract_affine_data(transform_matrix: Matrix) -> Matrix:
        return matinv(transform_matrix)

    @staticmethod
    def _off_center_transform(
        coordinate: Coordinate, transform_matrix: Matrix
    ) -> Matrix:
        return left_matmuls(
            translation_matrix(coordinate, inverse=True),
            transform_matrix,
            translation_matrix(coordinate, inverse=False),
        )


class ElementaryTransform(AffineTransform):
    @abstractmethod
    def _create_matrix(self, size: Size) -> Matrix:
        pass

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._extra_repr()})"

    def _extra_repr(self) -> str:
        return ""


class Shear(ElementaryTransform):
    """Affine horizontal shearing transformation.

    Args:
        angle: Shearing angle in degrees.
        clockwise: If ``True``, the shearing will be performed clockwise.
            Defaults to ``False``.
        center: Optional center of the shearing. Defaults to the center of
            the image.
    """

    def __init__(
        self,
        angle: float,
        clockwise: bool = False,
        center: Optional[Coordinate] = None,
    ):
        self.angle = angle % 360.0
        self.clockwise = clockwise
        self.center = center

    def _create_matrix(self, size: Size) -> Matrix:
        matrix = shearing_matrix(self.angle, clockwise=self.clockwise)
        if self.center is None:
            center = calculate_image_center(size)
        else:
            center = self.center
        matrix = self._off_center_transform(center, matrix)
        return matrix

    def _extra_repr(self) -> str:
        extras = [f"{self.angle:4.1f}°"]
        if self.clockwise:
            extras.append(f"clockwise={self.clockwise}")
        if self.center is not None:
            extras.append(f"center={self.center}")
        return ", ".join(extras)


class Rotate(ElementaryTransform):
    """Affine rotation transformation.

    Args:
        angle: Rotation angle in degrees.
        clockwise: If ``True``, the rotation will be performed clockwise.
            Defaults to ``False``.
        center: Optional center of the rotation. Defaults to the center of the
            image.
    """

    def __init__(
        self,
        angle: float,
        clockwise: bool = False,
        center: Optional[Coordinate] = None,
    ):
        self.angle = angle % 360.0
        self.clockwise = clockwise
        self.center = center

    def _create_matrix(self, size: Size) -> Matrix:
        matrix = rotation_matrix(self.angle, clockwise=self.clockwise)
        if self.center is None:
            center = calculate_image_center(size)
        else:
            center = self.center
        matrix = self._off_center_transform(center, matrix)
        return matrix

    def _extra_repr(self) -> str:
        extras = [f"{self.angle:4.1f}°"]
        if self.clockwise:
            extras.append(f"clockwise={self.clockwise}")
        if self.center is not None:
            extras.append(f"center={self.center}")
        return ", ".join(extras)


class Scale(ElementaryTransform):
    """Affine scaling transformation

    Args:
        factor: Horizontal and vertical scaling factors. If scalar, the
            same factor is used for both directions.
        center: Optional center of the scaling. Defaults to the center of
            the image.
    """

    def __init__(
        self,
        factor: Union[float, Tuple[float, float]],
        center: Optional[Coordinate] = None,
    ):
        self.factor = factor
        self.center = center

    def _create_matrix(self, size: Size) -> Matrix:
        matrix = scaling_matrix(self.factor)
        if self.center is None:
            center = calculate_image_center(size)
        else:
            center = self.center
        matrix = self._off_center_transform(center, matrix)
        return matrix

    def _extra_repr(self) -> str:
        def format_factor(factor: float) -> str:
            return f"{factor:.2f}"

        extras = []
        if isinstance(self.factor, float):
            extras.append(format_factor(self.factor))
        else:
            horz_factor, vert_factor = [
                format_factor(dim_factor) for dim_factor in self.factor
            ]
            extras.append(f"({horz_factor}, {vert_factor})")
        if self.center is not None:
            extras.append(f"center={self.center}")
        return ", ".join(extras)


class Translate(ElementaryTransform):
    """Affine translation transformation

    Args:
        translation: Horizontal and vertical translation.
        inverse: If ``True``, the translation will be performed in the
            opposite direction. Defaults to ``False``.
    """

    def __init__(self, translation: Coordinate, inverse: bool = False) -> None:
        self.translation = translation
        self.inverse = inverse

    def _create_matrix(self, size: Size) -> Matrix:
        return translation_matrix(self.translation, inverse=self.inverse)

    def _extra_repr(self) -> str:
        extras = [f"{tuple([round(coord, 1) for coord in self.translation])}"]
        if self.inverse:
            extras.append(f"inverse={self.inverse}")
        return ", ".join(extras)


class ComposedTransform(AffineTransform):
    """Composed affine transformation by chaining multiple
    :class:`AffineTransform` s together. An simple example might look like::

        from PIL import Image
        from pillow_affine import transforms

        image = Image.open(...)
        transform = transforms.ComposedTransform(
            transforms.Rotate(30.0), transforms.Translate((50.0, 100.0))
        )

        transform_params = transform.extract_transform_params(image.size)
        transformed_image = image.transform(*transform_params)

    Args:
        transforms: Individual :class:`AffineTransform` s.
    """

    def __init__(self, *transforms: AffineTransform) -> None:
        if len(transforms) == 0:
            msg = "A ComposedTransform must comprise at least one other transform."
            raise RuntimeError(msg)
        self.transforms = transforms

    def _create_matrix(self, size: Size) -> Matrix:
        return left_matmuls(
            *[transform._create_matrix(size) for transform in self.transforms]
        )

    def __repr__(self) -> str:
        head = f"{self.__class__.__name__}("
        tail = ")"

        if len(self.transforms) == 1:
            return head + repr(self.transforms[0]) + tail

        body = [" " * 2 + repr(transform) for transform in self.transforms]
        return "\n".join((head, *body, tail))
