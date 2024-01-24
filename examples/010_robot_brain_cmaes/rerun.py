"""Rerun a robot with given body and parameters."""

import config
import numpy as np
from evaluator import Evaluator

from revolve2.experimentation.logging import setup_logging
from revolve2.modular_robot.body.base import ActiveHinge
from revolve2.modular_robot.brain.cpg import (
    active_hinges_to_cpg_network_structure_neighbor,
)

# These are set of parameters that we optimized using CMA-ES.
# You can copy your own parameters from the optimization output log.
PARAMS = np.array(
    [
        0.28582455,
        0.3037231,
        -0.6800551,
        0.04504218,
        0.70664006,
        -0.87443432,
        -0.89959569,
        0.97630598,
        -0.99991301,
    ]
)


def main() -> None:
    """Perform the rerun."""
    setup_logging()

    # Find all active hinges in the body
    active_hinges = config.BODY.find_modules_of_type(ActiveHinge)

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
        body=config.BODY,
        output_mapping=output_mapping,
    )

    # Show the robot.
    evaluator.evaluate([PARAMS])


if __name__ == "__main__":
    main()
