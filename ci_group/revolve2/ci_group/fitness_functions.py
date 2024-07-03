"""Standard fitness functions for modular robots."""

import numpy as np
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
    begin_position = begin_state.get_pose().position.xyz
    end_position = end_state.get_pose().position.xyz

    # body_st, core_st = begin_state.get_core_and_body_pose()
    # body_ed, core_ed = begin_state.get_core_and_body_pose()

    return float(np.linalg.norm(end_position - begin_position))
