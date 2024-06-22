from dataclasses import dataclass, field

from simulation.scene import Pose
from simulation.scene.sensors._sensor import Sensor


@dataclass
class CameraSensor(Sensor):
    """Camera sensor."""

    pose: Pose
    camera_size: tuple[int, int]
    """Pose of the geometry, relative to its parent rigid body."""
    type: str = field(
        default="camera"
    )  # The type attribute is used for the translation into XML formats.
