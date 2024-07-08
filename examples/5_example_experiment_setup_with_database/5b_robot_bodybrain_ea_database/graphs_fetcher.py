"""Rerun the best robot between all experiments."""

import gc
import pickle
from copy import deepcopy

import config
import numpy as np
from database_components import (
    Experiment,
    Generation,
    Genotype,
    Individual,
    Population,
)
from revolve2.ci_group.morphological_measures import MorphologicalMeasures
from revolve2.experimentation.database import OpenMethod, open_database_sqlite
from revolve2.experimentation.logging import setup_logging
from sqlalchemy import select
from sqlalchemy.orm import Session
from tqdm import tqdm


def main() -> None:
    """Perform the rerun.


    :rtype: None

    """
    gc.disable()

    setup_logging()

    # Load the best individual from the database.
    dbengine = open_database_sqlite(
        config.DATABASE_FILE, open_method=OpenMethod.OPEN_IF_EXISTS
    )

    with Session(dbengine) as ses:
        # Aliasing the tables
        row = ses.execute(
            select(
                Experiment.id.label("experiment_id"),
                Generation.generation_index,
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
            .where(Experiment.id == 1)
            .order_by(Generation.generation_index.asc())
        ).fetchall()

    # id, generation_index, fitness, genotype
    row = np.array(row)
    generations = np.unique(row[:, 1])

    _template = {
        "nmod": [],
        "nhin": [],
        "ratio": [],
        "xy_symmetry": [],
        "xz_symmetry": [],
        "yz_symmetry": [],
    }

    _dict = {i: deepcopy(_template) for i in generations}

    iters = len(row)
    for idx, (_, gen_idx, _, genotype) in tqdm(enumerate(row), total=iters):
        gc.disable()

        robot = genotype.develop().body

        measures = MorphologicalMeasures(robot)
        nmod = len(measures.modules)
        nhin = len(measures.active_hinges)

        ratio = nhin / nmod

        xy_symmetry = measures.xy_symmetry
        xz_symmetry = measures.xz_symmetry
        yz_symmetry = measures.yz_symmetry

        _dict[gen_idx]["nmod"].append(nmod)
        _dict[gen_idx]["nhin"].append(nhin)
        _dict[gen_idx]["ratio"].append(ratio)
        _dict[gen_idx]["xy_symmetry"].append(xy_symmetry)
        _dict[gen_idx]["xz_symmetry"].append(xz_symmetry)
        _dict[gen_idx]["yz_symmetry"].append(yz_symmetry)

        del robot, measures

    # Save the dictionary on disk
    with open("dictionary.pkl", "wb") as file:
        pickle.dump(_dict, file)


if __name__ == "__main__":
    main()
