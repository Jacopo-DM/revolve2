from pyrr import Vector3
from revolve2.modular_robot.body._right_angles import RightAngles
from revolve2.modular_robot.body.base import Core


class CoreV1(Core):
    """The core module of a v1 modular robot."""

    def __init__(self, rotation: float | RightAngles) -> None:
        """
        Initialize this object.

        :param rotation: The modules' rotation.
        """
        super().__init__(
            rotation=rotation,
            bounding_box=Vector3([0.089, 0.089, 0.0603]),
            mass=0.250,
            child_offset=0.089 / 2.0,
            sensors=[],
        )
