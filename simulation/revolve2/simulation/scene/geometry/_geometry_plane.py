from dataclasses import dataclass, field

from simulation.scene._color import Color
from simulation.scene.geometry._geometry import Geometry
from simulation.scene.geometry.textures import MapType, Texture
from simulation.scene.vector2 import Vector2


@dataclass(kw_only=True)
class GeometryPlane(Geometry):
    """A flat plane geometry."""

    size: Vector2
    texture: Texture = field(
        default_factory=lambda: Texture(
            base_color=Color(100, 100, 100, 255),
            map_type=MapType.MAP2D,
        )
    )
