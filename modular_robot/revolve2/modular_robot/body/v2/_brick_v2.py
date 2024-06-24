from pyrr import Vector3

from revolve2.modular_robot.body._right_angles import RightAngles
from revolve2.modular_robot.body.base import Brick


class BrickV2(Brick):
    """A brick module for a modular robot."""

    def __init__(self, rotation: float | RightAngles) -> None:
        """Initialize this object.

        :param rotation: The modules' rotation.
        """
        super().__init__(
            rotation=rotation,
            bounding_box=Vector3([0.06288625, 0.06288625, 0.0603]),
            mass=0.06043,
            child_offset=0.06288625 / 2.0,
            sensors=[],
        )
