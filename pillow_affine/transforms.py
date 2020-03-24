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
    width, height = size
    horz_center = width / 2.0
    vert_center = height / 2.0
    return horz_center, vert_center


class AffineTransform(ABC):
    @abstractmethod
    def create_matrix(self, size: Size) -> Matrix:
        pass

    def extract_transform_params(
        self, size: Size, expand: bool = False
    ) -> Tuple[Size, int, Matrix]:
        transform_matrix = self.create_matrix(size)

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
    def create_matrix(self, size: Size) -> Matrix:
        pass

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.extra_repr()})"

    def extra_repr(self) -> str:
        return ""


class Shear(ElementaryTransform):
    def __init__(
        self,
        angle: float,
        clockwise: bool = False,
        center: Optional[Coordinate] = None,
    ):
        self.angle = angle % 360.0
        self.clockwise = clockwise
        self.center = center

    def create_matrix(self, size: Size) -> Matrix:
        matrix = shearing_matrix(self.angle, clockwise=self.clockwise)
        if self.center is None:
            center = calculate_image_center(size)
        else:
            center = self.center
        matrix = self._off_center_transform(center, matrix)
        return matrix

    def extra_repr(self) -> str:
        extras = [f"{self.angle:4.1f}°"]
        if self.clockwise:
            extras.append(f"clockwise={self.clockwise}")
        if self.center is not None:
            extras.append(f"center={self.center}")
        return ", ".join(extras)


class Rotate(ElementaryTransform):
    def __init__(
        self,
        angle: float,
        clockwise: bool = False,
        center: Optional[Coordinate] = None,
    ):
        self.angle = angle % 360.0
        self.clockwise = clockwise
        self.center = center

    def create_matrix(self, size: Size) -> Matrix:
        matrix = rotation_matrix(self.angle, clockwise=self.clockwise)
        if self.center is None:
            center = calculate_image_center(size)
        else:
            center = self.center
        matrix = self._off_center_transform(center, matrix)
        return matrix

    def extra_repr(self) -> str:
        extras = [f"{self.angle:4.1f}°"]
        if self.clockwise:
            extras.append(f"clockwise={self.clockwise}")
        if self.center is not None:
            extras.append(f"center={self.center}")
        return ", ".join(extras)


class Scale(ElementaryTransform):
    def __init__(
        self,
        factor: Union[float, Tuple[float, float]],
        center: Optional[Coordinate] = None,
    ):
        self.factor = factor
        self.center = center

    def create_matrix(self, size: Size) -> Matrix:
        matrix = scaling_matrix(self.factor)
        if self.center is None:
            center = calculate_image_center(size)
        else:
            center = self.center
        matrix = self._off_center_transform(center, matrix)
        return matrix

    def extra_repr(self) -> str:
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
    def __init__(self, translation: Coordinate, inverse: bool = False) -> None:
        self.translation = translation
        self.inverse = inverse

    def create_matrix(self, size: Size) -> Matrix:
        return translation_matrix(self.translation, inverse=self.inverse)

    def extra_repr(self) -> str:
        extras = [f"{tuple([round(coord, 1) for coord in self.translation])}"]
        if self.inverse:
            extras.append(f"inverse={self.inverse}")
        return ", ".join(extras)


class ComposedTransform(AffineTransform):
    def __init__(self, *transforms: AffineTransform) -> None:
        if len(transforms) == 0:
            msg = "A ComposedTransform must comprise at least one other transform."
            raise RuntimeError(msg)
        self.transforms = transforms

    def create_matrix(self, size: Size) -> Matrix:
        return left_matmuls(
            *[transform.create_matrix(size) for transform in self.transforms]
        )

    def __repr__(self) -> str:
        head = f"{self.__class__.__name__}("
        tail = ")"

        if len(self.transforms) == 1:
            return head + repr(self.transforms[0]) + tail

        body = [" " * 2 + repr(transform) for transform in self.transforms]
        return "\n".join((head, *body, tail))
