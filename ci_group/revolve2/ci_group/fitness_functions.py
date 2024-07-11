"""Standard fitness functions for modular robots."""

import numpy as np
from pyrr import Vector3
from revolve2.modular_robot_simulation import ModularRobotSimulationState

BIAS = Vector3((1, 1, 0))
ABS = Vector3((0, 0, 0))
MEASURE = "absolute"  # "absolute" or "relative"


def _l1_dist_(a: Vector3, b: Vector3, bias: Vector3 = BIAS) -> float:
    """Calculate the L1 distance between two points."""
    return np.sum(np.abs((a * bias) - (b * bias)))


def _l2_dist_(a: Vector3, b: Vector3, bias: Vector3 = BIAS) -> float:
    """Calculate the L2 distance between two points."""
    return np.sqrt(np.sum(((a * bias) - (b * bias)) ** 2))


def _l2_squared_dist_(a: Vector3, b: Vector3, bias: Vector3 = BIAS) -> float:
    """Calculate the squared L2 distance between two points."""
    return np.sum(((a * bias) - (b * bias)) ** 2)


def l1_area(
    states: list[ModularRobotSimulationState], *, absolute: bool = True
) -> float:
    """Calculate the L1 area traveled on the xy-plane by a single modular."""
    reference = ABS if absolute else states[0]
    return np.sum([_l1_dist_(reference, state_i) for state_i in states])


def l2_area(
    states: list[ModularRobotSimulationState], *, absolute: bool = True
) -> float:
    """Calculate the L1 area traveled on the xy-plane by a single modular."""
    reference = ABS if absolute else states[0]
    return np.sum([_l2_dist_(reference, state_i) for state_i in states])


def l2_squared_area(
    states: list[ModularRobotSimulationState], *, absolute: bool = True
) -> float:
    """Calculate the L1 area traveled on the xy-plane by a single modular."""
    reference = ABS if absolute else states[0]
    return np.sum([_l2_squared_dist_(reference, state_i) for state_i in states])


def l1_displacement(
    states: list[ModularRobotSimulationState], *, absolute: bool = True
) -> float:
    """Calculate the L1 distance traveled on the xy-plane by a single modular."""
    reference = ABS if absolute else states[0]
    return _l1_dist_(reference, states[-1])


def l2_displacement(
    states: list[ModularRobotSimulationState], *, absolute: bool = True
) -> float:
    """Calculate the L1 distance traveled on the xy-plane by a single modular."""
    reference = ABS if absolute else states[0]
    return _l2_dist_(reference, states[-1])


DISTANCE_FUNCTIONS = {
    "l1_displacement": l1_displacement,
    "l2_displacement": l2_displacement,
    "l1_area": l1_area,
    "l2_area": l2_area,
    "l2_squared_area": l2_squared_area,
}


def xy_displacement(
    states: list[ModularRobotSimulationState],
    mode: str = "l2_squared_area",
) -> float:
    """Calculate the distance traveled on the xy-plane by a single modular."""
    if mode not in DISTANCE_FUNCTIONS:
        msg = f"Invalid mode '{mode}', must be one of {list(DISTANCE_FUNCTIONS.keys())}."
        raise ValueError(msg)
    return DISTANCE_FUNCTIONS[mode](states)
