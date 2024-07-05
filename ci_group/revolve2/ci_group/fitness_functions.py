"""Standard fitness functions for modular robots."""

import numpy as np
from pyrr import Vector3
from revolve2.modular_robot_simulation import ModularRobotSimulationState


def xy_displacement(
    begin_state: ModularRobotSimulationState,
    end_state: ModularRobotSimulationState,
) -> float:
    """Calculate the distance traveled on the xy-plane by a single modular
    robot.

    :param begin_state: Begin state of the robot.
    :type begin_state: ModularRobotSimulationState
    :param end_state: End state of the robot.
    :type end_state: ModularRobotSimulationState
    :returns: The calculated fitness.
    :rtype: float

    """
    end_position = end_state.get_pose().position

    xyz_n = end_position.xyz
    xyz_0 = Vector3([0.0, 0.0, 0.0])
    return np.sum((xyz_n - xyz_0) ** 2)
