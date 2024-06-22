from dataclasses import dataclass

from simulation.scene.geometry._geometry import Geometry


@dataclass(kw_only=True)
class GeometrySphere(Geometry):
    """Box geometry."""

    radius: float
    """The radius of the sphere."""
