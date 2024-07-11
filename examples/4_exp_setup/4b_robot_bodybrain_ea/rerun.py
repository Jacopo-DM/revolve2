"""Rerun a robot with given body and parameters."""

import logging
import pickle
from pathlib import Path
from typing import TYPE_CHECKING

from evaluator import Evaluator
from revolve2.experimentation.logging import setup_logging

if TYPE_CHECKING:
    from individual import Individual


def main() -> None:
    """Perform the rerun.


    :rtype: None

    """
    setup_logging()

    with Path("best_robot.pkl").open("rb") as f:
        individual: Individual = pickle.load(f, encoding="latin1")

    logging.info(f"Fitness from pickle: {individual.fitness}")

    evaluator = Evaluator(
        headless=False,
        num_simulators=1,
    )
    fitness = evaluator.evaluate([individual.genotype])[0]
    logging.info(f"Rerun fitness: {fitness}")


if __name__ == "__main__":
    main()
