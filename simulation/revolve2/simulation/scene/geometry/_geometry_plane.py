from dataclasses import dataclass, field

from revolve2.simulation.scene._color import Color
from revolve2.simulation.scene.geometry.textures import MapType, Texture
from revolve2.simulation.scene.vector2 import Vector2

from ._geometry import Geometry


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
