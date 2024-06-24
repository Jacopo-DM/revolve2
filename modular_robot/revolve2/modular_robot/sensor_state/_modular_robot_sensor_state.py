from abc import ABC, abstractmethod

from ..body.sensors import (
    ActiveHingeSensor,
    CameraSensor,
    IMUSensor,
)
from ._active_hinge_sensor_state import (
    ActiveHingeSensorState,
)
from ._camera_sensor_state import CameraSensorState
from ._imu_sensor_state import IMUSensorState


class ModularRobotSensorState(ABC):
    """The state of modular robot's sensors."""

    @abstractmethod
    def get_active_hinge_sensor_state(
        self, sensor: ActiveHingeSensor
    ) -> ActiveHingeSensorState:
        """Get the state of the provided active hinge sensor.

        :param sensor: The sensor.
        :type sensor: ActiveHingeSensor
        :returns: The state.
        :rtype: ActiveHingeSensorState

        """

    @abstractmethod
    def get_imu_sensor_state(self, sensor: IMUSensor) -> IMUSensorState:
        """Get the state of the provided IMU sensor.

        :param sensor: The sensor.
        :type sensor: IMUSensor
        :returns: The state.
        :rtype: IMUSensorState

        """

    @abstractmethod
    def get_camera_sensor_state(
        self, sensor: CameraSensor
    ) -> CameraSensorState:
        """Get the state of the provided camera sensor.

        :param sensor: The sensor.
        :type sensor: CameraSensor
        :returns: The state.
        :rtype: CameraSensorState

        """
