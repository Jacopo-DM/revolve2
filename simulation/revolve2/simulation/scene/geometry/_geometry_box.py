from dataclasses import dataclass

from simulation.scene._aabb import AABB
from simulation.scene.geometry._geometry import Geometry


@dataclass(kw_only=True)
class GeometryBox(Geometry):
    """Box geometry."""

    aabb: AABB
    """AABB describing the box's bounding box."""
