from dataclasses import dataclass, field

import numpy as np
import numpy.typing as npt
from pyrr import Vector3

from .._color import Color
from ..geometry.textures import MapType, Texture
from ._geometry import Geometry


@dataclass(kw_only=True)
class GeometryHeightmap(Geometry):
    """A heightmap geometry.

    Similarly to the `Plane` geometry, x and y of `size` define the space the heightmap encompasses.
    The z-coordinate defines the height of a heightmap edge when it's value is maximum.
    `heights` defines the edge of the heightmap. Values much lie between 0.0 and 1.0, inclusive.
    `base_thickness` defines the thickness of the box below the heightmap, which is requires for proper collision detection in some simulators.
    """

    size: Vector3
    base_thickness: float
    # MxN matrix. outer list is x, inner list is y
    heights: npt.NDArray[np.float64]
    texture: Texture = field(
        default_factory=lambda: Texture(
            base_color=Color(100, 100, 100, 255), map_type=MapType.MAP2D
        )
    )
