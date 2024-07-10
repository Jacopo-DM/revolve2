"""Standard fitness functions for modular robots."""

from itertools import pairwise, starmap

import numpy as np
from pyrr import Vector3
from revolve2.modular_robot_simulation import ModularRobotSimulationState


def l1_dist(a: Vector3, b: Vector3) -> float:
    """Calculate the L1 distance between two points."""
    return np.sum(np.abs(a - b))


def l2_dist(a: Vector3, b: Vector3) -> float:
    """Calculate the L2 distance between two points."""
    return np.sqrt(np.sum((a - b) ** 2))


def l2_squared_dist(a: Vector3, b: Vector3) -> float:
    """Calculate the squared L2 distance between two points."""
    return np.sum((a - b) ** 2)


def l1_area(states: list[ModularRobotSimulationState]) -> float:
    """Calculate the L1 area traveled on the xy-plane by a single modular."""
    return np.sum([l1_dist(states[0], state_i) for state_i in states])


def l2_area(states: list[ModularRobotSimulationState]) -> float:
    """Calculate the L1 area traveled on the xy-plane by a single modular."""
    return np.sum([l2_dist(states[0], state_i) for state_i in states])


def l2_squared_area(states: list[ModularRobotSimulationState]) -> float:
    """Calculate the L1 area traveled on the xy-plane by a single modular."""
    return np.sum([l2_dist(states[0], state_i) for state_i in states])


def l1_displacement(states: list[ModularRobotSimulationState]) -> float:
    """Calculate the L1 distance traveled on the xy-plane by a single modular."""
    return l1_dist(states[0], states[-1])


DISTANCE_FUNCTIONS = {
    "l1": l1_dist,
    "l2": l2_dist,
    "l2_squared": l2_squared_dist,
    "l1_area": l1_area,
    "l2_area": l2_area,
    "l2_squared_area": l2_squared_area,
}


def xy_displacement(
    states: list[ModularRobotSimulationState],
    mode: str = "l1_area",
) -> float:
    """Calculate the distance traveled on the xy-plane by a single modular."""
    if mode not in DISTANCE_FUNCTIONS:
        msg = f"Invalid mode '{mode}', must be one of {list(DISTANCE_FUNCTIONS.keys())}."
        raise ValueError(msg)
    return DISTANCE_FUNCTIONS[mode](states)
