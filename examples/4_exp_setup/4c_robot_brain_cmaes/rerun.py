"""Rerun a robot with given body and parameters."""

import pickle
from pathlib import Path

import config
from evaluator import Evaluator
from revolve2.experimentation.logging import setup_logging
from revolve2.experimentation.optimization.ea._individual import Individual
from revolve2.modular_robot.body.base import ActiveHinge
from revolve2.modular_robot.brain.cpg import (
    active_hinges_to_cpg_network_structure_neighbor,
)


def get_brain():
    """Get the best brain from the CMA-ES optimization."""
    with Path("best_robot_brain.pkl").open("rb") as f:
        return pickle.load(f)


def main() -> None:
    """Perform the rerun.


    :rtype: None

    """
    setup_logging()

    body = config.BODY
    active_hinges = body.find_modules_of_type(ActiveHinge)

    prams = get_brain()

    # Create a structure for the CPG network from these hinges.
    # This also returns a mapping between active hinges and the index of there corresponding cpg in the network.
    (
        cpg_network_structure,
        output_mapping,
    ) = active_hinges_to_cpg_network_structure_neighbor(active_hinges)

    # Create the evaluator.
    evaluator = Evaluator(
        headless=False,
        num_simulators=1,
        cpg_network_structure=cpg_network_structure,
        body=body,
        output_mapping=output_mapping,
    )

    # Show the robot.
    evaluator.evaluate([prams])


if __name__ == "__main__":
    main()
