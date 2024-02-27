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
        0.64095736,
        0.73656541,
        -0.73142523,
        0.32122525,
        0.99339834,
        0.28400446,
        -0.60034754,
        0.68629471,
        -0.4320507,
        0.32869863,
        0.79764717,
        0.99172804,
        0.63612167,
        -0.96939572,
        -0.71606361,
        0.99628936,
        0.57843282,
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
        start_paused=True,
    )

    # Show the robot.
    evaluator.evaluate([PARAMS])


if __name__ == "__main__":
    main()
