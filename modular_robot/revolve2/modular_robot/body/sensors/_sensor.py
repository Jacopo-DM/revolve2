import uuid
from abc import ABC

from pyrr import Quaternion, Vector3


class Sensor(ABC):
    """An abstract Sensor Class."""

    _uuid: uuid.UUID
    _orientation: Quaternion
    _position: Vector3

    def __init__(self, orientation: Quaternion, position: Vector3) -> None:
        """Initialize the sensor.

        :param orientation: The rotation of the sensor.
        :param position: The position of the sensor.
        """
        self._orientation = orientation
        self._uuid = uuid.uuid1()
        self._position = position

    @property
    def uuid(self) -> uuid.UUID:
        """Get the uuid of the sensor.


        :returns: The uuid.

        :rtype: uuid.UUID

        """
        return self._uuid

    @property
    def orientation(self) -> Quaternion:
        """Return the orientation of the sensor.


        :returns: The orientation.

        :rtype: Quaternion

        """
        return self._orientation

    @property
    def position(self) -> Vector3:
        """Get the relative position of the sensor on a module.


        :returns: The position.

        :rtype: Vector3

        """
        return self._position
