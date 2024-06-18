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
PARAMS = np.array([
    0.67338874,
    -0.32043631,
    -0.09329818,
    0.14104069,
    0.2078359,
    0.09654036,
    0.57177192,
    0.09843656,
    0.99727493,
    -0.11738952,
    0.39712527,
    0.41593478,
    -0.16532369,
    -0.92198934,
    -0.77732104,
    0.34631912,
    0.6039283,
])


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
