from abc import ABC, abstractmethod

from modular_robot._modular_robot_control_interface import (
    ModularRobotControlInterface,
)
from modular_robot.sensor_state import ModularRobotSensorState


class BrainInstance(ABC):
    """An instance of a brain that perform the control of a robot.

    Instances of this class can be stateful.
    """

    @abstractmethod
    def control(
        self,
        dt: float,
        sensor_state: ModularRobotSensorState,
        control_interface: ModularRobotControlInterface,
    ) -> None:
        """Control the modular robot.

        :param dt: Elapsed seconds since last call to this function.
        :param sensor_state: Interface for reading the current sensor state.
        :param control_interface: Interface for controlling the robot.
        """
