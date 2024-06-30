"""Rerun the best robot between all experiments."""

import logging

import config
from database_components import Generation, Genotype, Individual
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
        row = ses.execute(
            select(Genotype, Individual.fitness)
            .join_from(
                Genotype, Individual, Genotype.id == Individual.genotype_id
            )
            .order_by(Individual.fitness.desc())
            .filter(Genotype.id != 1)
            .filter(Generation.id == 1)
            .limit(1)
        ).fetchone()

        genotype = row[0]
        fitness = row[1]

    logging.info(f"Best fitness: {fitness}")

    # Create the evaluator.
    evaluator = Evaluator(headless=False, num_simulators=1, start_paused=True)

    # Show the robot.
    evaluator.evaluate([genotype])


if __name__ == "__main__":
    main()
