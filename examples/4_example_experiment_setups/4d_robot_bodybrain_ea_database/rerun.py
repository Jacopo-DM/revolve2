"""Rerun the best robot between all experiments."""

import logging
import pickle
from pathlib import Path

import config
from database_components import (
    Experiment,
    Generation,
    Genotype,
    Individual,
    Population,
)
from evaluator import Evaluator
from revolve2.experimentation.database import OpenMethod, open_database_sqlite
from revolve2.experimentation.logging import setup_logging
from sqlalchemy import select
from sqlalchemy.orm import Session


def main() -> None:
    """Perform the rerun.


    :rtype: None

    """
    setup_logging()

    # Load the best individual from the database.
    dbengine = open_database_sqlite(
        config.DATABASE_FILE, open_method=OpenMethod.OPEN_IF_EXISTS
    )

    with Session(dbengine) as ses:
        # Aliasing the tables
        row = ses.execute(
            select(
                Individual.fitness,
                Genotype,
            )
            .join_from(
                Experiment,
                Generation,
                Experiment.id == Generation.experiment_id,
            )
            .join_from(
                Generation,
                Population,
                Generation.population_id == Population.id,
            )
            .join_from(
                Population,
                Individual,
                Population.id == Individual.population_id,
            )
            .join(
                Genotype,
                Individual.genotype_id == Genotype.id,
            )
            # .where(Experiment.id == 1)
            .order_by(Individual.fitness.desc())
            .limit(1)
        ).one()
        fitness = row[0]
        genotype = row[1]

    logging.info(f"Best fitness: {fitness}")

    with Path("best_robot.pkl").open("wb") as f:
        pickle.dump(genotype, f)

    # Create the evaluator.
    evaluator = Evaluator(headless=False, num_simulators=1, start_paused=True)

    # Show the robot.
    evaluator.evaluate([genotype])


if __name__ == "__main__":
    main()
