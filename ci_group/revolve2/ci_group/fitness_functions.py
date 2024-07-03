"""Standard fitness functions for modular robots."""


import numpy as np
from pyrr import Quaternion, Vector3
from revolve2.modular_robot_simulation import ModularRobotSimulationState
from revolve2.simulation.scene import (
    Pose,
)


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
    body_st = begin_state.get_body()
    st_xpos = begin_state.get_simulation_state().xpos().copy()
    st_xquat = begin_state.get_simulation_state().xquat().copy()

    body_ed = end_state.get_body()
    ed_xpos = end_state.get_simulation_state().xpos().copy()
    ed_xquat = end_state.get_simulation_state().xquat().copy()

    pose_st = Pose(
        Vector3(st_xpos[body_st.id]),
        Quaternion(st_xquat[body_st.id]),
    )
    pose_ed = Pose(
        Vector3(ed_xpos[body_ed.id]),
        Quaternion(ed_xquat[body_ed.id]),
    )
    return float(np.linalg.norm(pose_ed.position.xyz - pose_st.position.xyz))
