from ..._modular_robot_control_interface import (
    ModularRobotControlInterface,
)
from ...brain._brain_instance import BrainInstance
from ...sensor_state import ModularRobotSensorState


class BrainDummyInstance(BrainInstance):
    """A brain that does nothing."""

    def control(
        self,
        dt: float,
        sensor_state: ModularRobotSensorState,
        control_interface: ModularRobotControlInterface,
    ) -> None:
        """Control nothing.

        This brain does not do anything for control, as it is an empty
        box.

        :param dt: Elapsed seconds since last call to this function.
        :type dt: float
        :param sensor_state: Interface for reading the current sensor
            state.
        :type sensor_state: ModularRobotSensorState
        :param control_interface: Interface for controlling the robot.
        :rtype: None
        :type control_interface: ModularRobotControlInterface
        :rtype: None

        """
