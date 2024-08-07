"""Main script for the example."""

import logging
import pickle
from pathlib import Path

import cma
import config
from evaluator import Evaluator
from individual import Individual
from revolve2.experimentation.logging import setup_logging
from revolve2.experimentation.rng import seed_from_time
from revolve2.modular_robot.brain.cpg import (
    active_hinges_to_cpg_network_structure_neighbor,
)


def get_genotype() -> Individual:
    """Load the best robot genotype from the previous experiment."""
    with Path("best_robot.pkl").open("rb") as f:
        individual: Individual = pickle.load(f, encoding="latin1")
    return individual


def main() -> None:
    """Run the experiment.


    :rtype: None

    """
    setup_logging(file_name="log.txt")

    # Find all active hinges in the body
    robot = get_genotype().genotype.develop()
    body = robot.body
    active_hinges = body.find_modules_of_any_type()

    # Create a structure for the CPG network from these hinges.
    # This also returns a mapping between active hinges and the index of there corresponding cpg in the network.
    (
        cpg_network_structure,
        output_mapping,
    ) = active_hinges_to_cpg_network_structure_neighbor(active_hinges)

    # Initialize the evaluator that will be used to evaluate robots.
    evaluator = Evaluator(
        headless=True,
        num_simulators=config.NUM_SIMULATORS,
        cpg_network_structure=cpg_network_structure,
        body=body,
        output_mapping=output_mapping,
    )

    # Initial parameter values for the brain.
    initial_mean = cpg_network_structure.num_connections * [0.5]

    # We use the CMA-ES optimizer from the cma python package.
    # Initialize the cma optimizer.
    options = cma.CMAOptions()
    options.set("bounds", [-3.0, 3.0])

    # The cma package uses its own internal rng.
    # Instead of creating our own numpy rng, we use our seed to initialize cma.
    rng_seed = seed_from_time() % 2**32  # Cma seed must be smaller than 2**32.
    options.set("seed", rng_seed)
    opt = cma.CMAEvolutionStrategy(initial_mean, config.INITIAL_STD, options)

    generation_index = 0

    # Run cma for the defined number of generations.
    logging.info("Start optimization process.")
    while generation_index < config.NUM_GENERATIONS:
        logging.info(
            f"Generation {generation_index + 1} / {config.NUM_GENERATIONS}."
        )

        # Get the sampled solutions(parameters) from cma.
        solutions = opt.ask()

        # Evaluate them. Invert because fitness maximizes, but cma minimizes.
        fitnesses = -evaluator.evaluate(solutions)

        # Tell cma the fitnesses.
        opt.tell(solutions, fitnesses)

        logging.info(f"{opt.result.xbest=} {opt.result.fbest=}")

        with Path("best_robot_brain.pkl").open("wb") as f:
            pickle.dump(opt.result.xbest, f)

        # Increase the generation index counter.
        generation_index += 1


if __name__ == "__main__":
    main()
