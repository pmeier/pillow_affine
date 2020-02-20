from typing import Union, Optional, Tuple
from abc import ABC, abstractmethod
from PIL import Image
import numpy as np
from .matrix import (
    left_matmuls,
    inv,
    verify_matrix,
    shearing_matrix,
    rotation_matrix,
    scaling_matrix,
    translation_matrix,
)

__all__ = [
    "AffineTransform",
    "Shear",
    "Rotate",
    "Scale",
    "Translate",
    "ComposedTransform",
]


def calculate_image_center(size: Tuple[int, int]) -> Tuple[float, float]:
    width, height = size
    horz_center = width / 2.0
    vert_center = height / 2.0
    return horz_center, vert_center


class AffineTransform(ABC):
    @abstractmethod
    def create_matrix(self, size: Tuple[int, int]) -> np.ndarray:
        pass

    def extract_transform_params(
        self, size: Tuple[int, int], expand: bool = False
    ) -> Tuple[Tuple[int, int], int, Tuple[int, int, int, int, int, int]]:
        transform_matrix = self.create_matrix(size)
        verify_matrix(transform_matrix)

        if expand:
            expanded_size, transform_matrix = self._expand_canvas(
                size, transform_matrix
            )
        else:
            expanded_size = size

        transform_matrix = self._coordinate_transform(size, transform_matrix)

        data = self._extract_affine_data(transform_matrix)

        return expanded_size, Image.AFFINE, data

    @staticmethod
    def _expand_canvas(
        size: Tuple[int, int], transform_matrix: np.ndarray
    ) -> Tuple[Tuple[int, int], np.ndarray]:
        def calculate_motif_vertices(transform_matrix: np.ndarray) -> np.ndarray:
            width, height = size
            image_vertices = np.array(
                (
                    # fmt:off
                    (0.0, width,    0.0, width),
                    (0.0,   0.0, height, height),
                    # fmt:on
                )
            )
            image_vertices = np.concatenate((image_vertices, np.ones((1, 4))))
            return np.matmul(transform_matrix, image_vertices)[:-1, :]

        def calculate_expanded_size(motif_vertices: np.ndarray) -> Tuple[int, int]:
            left_bottom_vertex = np.floor(np.min(motif_vertices, axis=1))
            right_top_vertex = np.ceil(np.max(motif_vertices, axis=1))
            expanded_size = right_top_vertex - left_bottom_vertex
            return tuple(expanded_size.astype(np.int).tolist())

        def recenter_motif(
            expanded_size: Tuple[int, int], transform_matrix: np.ndarray
        ) -> np.ndarray:
            matrix = left_matmuls(
                translation_matrix(calculate_image_center(size), inverse=True),
                translation_matrix(calculate_image_center(expanded_size)),
            )
            # TODO: Investigate and document why this extra step is needed
            matrix = AffineTransform._coordinate_transform(size, matrix)
            return left_matmuls(transform_matrix, matrix)

        motif_vertices = calculate_motif_vertices(transform_matrix)
        expanded_size = calculate_expanded_size(motif_vertices)
        transform_matrix = recenter_motif(expanded_size, transform_matrix)

        return expanded_size, transform_matrix

    @staticmethod
    def _coordinate_transform(
        size: Tuple[int, int], transform_matrix: np.ndarray
    ) -> np.ndarray:
        width, height = size
        matrix = np.array(((1.0, 0.0, 0.0), (0.0, -1.0, height), (0.0, 0.0, 1.0)))
        return left_matmuls(matrix, transform_matrix, inv(matrix))

    @staticmethod
    def _extract_affine_data(
        transform_matrix: np.ndarray,
    ) -> Tuple[int, int, int, int, int, int]:
        inv_transform_params = inv(transform_matrix)[:-1, :]
        return tuple(inv_transform_params.reshape(6).tolist())

    @staticmethod
    def _transform_around_point(
        point: Tuple[float, float], transform_matrix: np.array
    ) -> np.array:
        return left_matmuls(
            translation_matrix(point, inverse=True),
            transform_matrix,
            translation_matrix(point, inverse=False),
        )


class ElementaryTransform(AffineTransform):
    @abstractmethod
    def create_matrix(self, size: Tuple[int, int]) -> np.ndarray:
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
        center: Optional[Tuple[float, float]] = None,
    ):
        self.angle = angle % 360.0
        self.clockwise = clockwise
        self.center = center

    def create_matrix(self, size: Tuple[int, int]) -> np.ndarray:
        matrix = shearing_matrix(self.angle, clockwise=self.clockwise)
        if self.center is None:
            center = calculate_image_center(size)
        else:
            center = self.center
        matrix = self._transform_around_point(center, matrix)
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
        center: Optional[Tuple[float, float]] = None,
    ):
        self.angle = angle % 360.0
        self.clockwise = clockwise
        self.center = center

    def create_matrix(self, size: Tuple[int, int]) -> np.ndarray:
        matrix = rotation_matrix(self.angle, clockwise=self.clockwise)
        if self.center is None:
            center = calculate_image_center(size)
        else:
            center = self.center
        matrix = self._transform_around_point(center, matrix)
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
        center: Optional[Tuple[float, float]] = None,
    ):
        self.factor = factor
        self.center = center

    def create_matrix(self, size: Tuple[int, int]) -> np.ndarray:
        matrix = scaling_matrix(self.factor)
        if self.center is None:
            center = calculate_image_center(size)
        else:
            center = self.center
        matrix = self._transform_around_point(center, matrix)
        return matrix

    def extra_repr(self) -> str:
        if isinstance(self.factor, float):
            factor = round(self.factor, 2)
        else:
            factor = tuple([round(coord_factor, 2) for coord_factor in self.factor])
        extras = [str(factor)]
        if self.center is not None:
            extras.append(f"center={self.center}")
        return ", ".join(extras)


class Translate(ElementaryTransform):
    def __init__(self, translation: Tuple[float, float], inverse: bool = False) -> None:
        self.translation = translation
        self.inverse = inverse

    def create_matrix(self, size: Tuple[int, int]) -> np.ndarray:
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

    def create_matrix(self, size: Tuple[int, int]) -> np.ndarray:
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
