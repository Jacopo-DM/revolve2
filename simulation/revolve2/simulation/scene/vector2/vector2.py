"""A representation of a 2d Vector."""

from __future__ import annotations

from numbers import Number
from typing import Any

import numpy as np
from pyrr.objects.base import BaseMatrix33, BaseVector, NpProxy

from simulation.scene.vector2 import vector2aux as vector2


class Vector2(BaseVector):  # type: ignore[misc]
    def __hash__(self) -> int:
        return hash(tuple(self))

    # TODO(jmdm): fix typing ↑
    """Represents a 2-dimensional Vector. The Vector2 class is based on the pyrr implementation of vectors."""

    _module = vector2
    _shape = (2,)

    x = NpProxy(0)  #: The X value of this Vector.
    y = NpProxy(1)  #: The Y value of this Vector.
    xy = NpProxy([0, 1])  #: The X,Y values of this Vector as a numpy.ndarray.

    ########################
    # Creation
    def __new__(
        # No solution exists
        cls,
        value: Any = None,
        w: float = 0.0,
        dtype: Any = None,
    ) -> Any:
        """
        Make a new Vector2.

        :param value: The value of the Vector2.
        :param w: unused rest.
        :param dtype: The data-type.
        :return: A new Vector2.
        """
        if value is not None:
            obj = value
            if not isinstance(value, np.ndarray):
                obj = np.array(value, dtype=dtype)

            # matrix33
            if obj.shape == 3 or isinstance(obj, BaseMatrix33):
                obj = vector2.create_from_matrix33_translation(obj, dtype=dtype)
        else:
            obj = np.zeros(cls._shape, dtype=dtype)
        obj = obj.view(cls)
        return super().__new__(cls, obj)

    ########################
    # Operators
    __NMB = (Number, np.number)
    __VCT = ("Vector2", np.ndarray, list)

    def __add__(self, other: Any) -> Vector2 | None:
        """
        Add to the existing Vector2.

        :param other: The other Vector2.
        :return: The added Vector2.
        """
        if type(other) in self.__NMB or type(other) in self.__VCT:
            return Vector2(super().__add__(other))
        self._unsupported_type("add", other)
        return None

    def __sub__(self, other: Any) -> Vector2 | None:
        """
        Subtract from the existing Vector2.

        :param other: The other Vector2.
        :return: The subtracted Vector2.
        """
        if type(other) in self.__NMB or type(other) in self.__VCT:
            return Vector2(super().__sub__(other))
        self._unsupported_type("subtract", other)
        return None

    def __mul__(self, other: Any) -> Vector2 | None:
        """
        Multiply the existing Vector2.

        :param other: The other Vector2.
        :return: the multiplied Vector2.
        """
        if type(other) in self.__NMB:
            return Vector2(super().__mul__(other))
        self._unsupported_type("multiply", other)
        return None

    def __xor__(self, other: Any) -> Any:
        """
        Calculate the cross-product.

        :param other: The other Vector2.
        :return: The cross-product.
        """
        if type(other) in self.__VCT:
            return self.cross(other)
        self._unsupported_type("XOR", other)
        return None

    def __or__(self, other: Any) -> Any:
        """
        Calculate the dot-product.

        :param other: The other Vector2.
        :return: The dot-product.
        """
        if type(other) in self.__VCT:
            return self.dot(other)
        self._unsupported_type("OR", other)
        return None

    def __ne__(self, other: object) -> bool:
        """
        Not equal to the existing Vector2.

        :param other: The other Vector2.
        :return: whether they are unequal.
        """
        if type(other) in self.__VCT:
            return bool(np.any(super().__ne__(other)))
        self._unsupported_type("NE", other)
        return False

    def __eq__(self, other: object) -> bool:
        """
        Equal to the existing Vector2.

        :param other: The other Vector2.
        :return: whether they are equal.
        """
        if type(other) in self.__VCT:
            return bool(np.all(super().__eq__(other)))
        self._unsupported_type("EQ", other)
        return False

    ########################
    # Methods and Properties
    @property
    def inverse(self) -> Vector2:
        """:return: the inverted Vector2."""
        return Vector2(-self)
