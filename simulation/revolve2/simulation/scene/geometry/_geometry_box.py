from dataclasses import dataclass

from revolve2.simulation.scene._aabb import AABB

from ._geometry import Geometry


@dataclass(kw_only=True)
class GeometryBox(Geometry):
    """Box geometry."""

    aabb: AABB
    """AABB describing the box's bounding box."""
