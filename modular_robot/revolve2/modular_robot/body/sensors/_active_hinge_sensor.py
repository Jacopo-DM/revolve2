from pyrr import Quaternion, Vector3

from modular_robot.body.sensors._sensor import Sensor


class ActiveHingeSensor(Sensor):
    """A sensors for an active hinge that measures its angle."""

    def __init__(self) -> None:
        """Initialize the ActiveHinge sensor."""
        super().__init__(Quaternion(), Vector3())
