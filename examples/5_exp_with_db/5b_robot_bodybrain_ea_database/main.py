"""Main script for the example."""

import logging
from typing import Any

import config
import multineat
import numpy as np
import numpy.typing as npt
from database_components import (
    Base,
    Experiment,
    Generation,
    Genotype,
    Individual,
    Population,
)
from evaluator import Evaluator
from plot import main as plot_fig
from rerun import main as rerun_main
from revolve2.experimentation.database import OpenMethod, open_database_sqlite
from revolve2.experimentation.evolution import ModularRobotEvolution
from revolve2.experimentation.evolution.abstract_elements import (
    Reproducer,
    Selector,
)
from revolve2.experimentation.logging import setup_logging
from revolve2.experimentation.optimization.ea import (
    population_management,
    selection,
)
from revolve2.experimentation.rng import make_rng, seed_from_time
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session


class ParentSelector(Selector):
    """Selector class for parent selection."""

    rng: np.random.Generator
    offspring_size: int

    def __init__(self, offspring_size: int, rng: np.random.Generator) -> None:
        """Initialize the parent selector.

        :param offspring_size: The offspring size.
        :param rng: The rng generator.
        """
        self.offspring_size = offspring_size
        self.rng = rng

    def select(
        self, population: Population, **kwargs: Any
    ) -> tuple[npt.NDArray[np.int_], dict[str, Population]]:
        """Select the parents.

        :param population: The population of robots.
            Any
        :type population: Population
        :param **kwargs:
        :type **kwargs: Any
        :returns: The parent pairs.
        :rtype: tuple[npt.NDArray[np.int_],dict[str,Population]]

        """
        return np.array(
            [
                selection.multiple_unique(
                    selection_size=2,
                    population=[
                        individual.genotype
                        for individual in population.individuals
                    ],
                    fitnesses=[
                        individual.fitness
                        for individual in population.individuals
                    ],
                    selection_function=lambda _,
                    fitnesses: selection.tournament(
                        rng=self.rng, fitnesses=fitnesses, k=2
                    ),
                )
                for _ in range(self.offspring_size)
            ],
        ), {"parent_population": population}


class SurvivorSelector(Selector):
    """Selector class for survivor selection."""

    rng: np.random.Generator

    def __init__(self, rng: np.random.Generator) -> None:
        """Initialize the parent selector.

        :param rng: The rng generator.
        """
        self.rng = rng

    def select(
        self, population: Population, **kwargs: Any
    ) -> tuple[Population, dict[str, Any]]:
        """Select survivors using a tournament.

        :param population: The population the parents come from.
            Any
        :type population: Population
        :param **kwargs:
        :type **kwargs: Any
        :returns: A newly created population.
        :rtype: tuple[Population,dict[str,Any]]
        :raises ValueError: If the population is empty.

        """
        offspring = kwargs.get("children")
        offspring_fitness = kwargs.get("child_task_performance")
        if offspring is None or offspring_fitness is None:
            msg = "No offspring was passed with positional argument 'children' and / or 'child_task_performance'."
            raise ValueError(msg)

        original_survivors, offspring_survivors = (
            population_management.steady_state(
                old_genotypes=[i.genotype for i in population.individuals],
                old_fitnesses=[i.fitness for i in population.individuals],
                new_genotypes=offspring,
                new_fitnesses=offspring_fitness,
                selection_function=lambda n,
                genotypes,
                fitnesses: selection.multiple_unique(
                    selection_size=n,
                    population=genotypes,
                    fitnesses=fitnesses,
                    selection_function=lambda _,
                    fitnesses: selection.tournament(
                        rng=self.rng, fitnesses=fitnesses, k=2
                    ),
                ),
            )
        )

        return (
            Population(
                individuals=[
                    Individual(
                        genotype=population.individuals[i].genotype,
                        fitness=population.individuals[i].fitness,
                    )
                    for i in original_survivors
                ]
                + [
                    Individual(
                        genotype=offspring[i],
                        fitness=offspring_fitness[i],
                    )
                    for i in offspring_survivors
                ]
            ),
            {},
        )


class CrossoverReproducer(Reproducer):
    """A simple crossover reproducer using multineat."""

    rng: np.random.Generator
    innov_db_body: multineat.InnovationDatabase
    innov_db_brain: multineat.InnovationDatabase

    def __init__(
        self,
        rng: np.random.Generator,
        innov_db_body: multineat.InnovationDatabase,
        innov_db_brain: multineat.InnovationDatabase,
    ) -> None:
        """Initialize the reproducer.

        :param rng: The random generator.
        :param innov_db_body: The innovation database for the body.
        :param innov_db_brain: The innovation database for the brain.
        """
        self.rng = rng
        self.innov_db_body = innov_db_body
        self.innov_db_brain = innov_db_brain

    def reproduce(
        self, population: npt.NDArray[np.int_], **kwargs: Any
    ) -> list[Genotype]:
        """Reproduce the population by crossover.

        :param population: The parent pairs.
        :type population: npt.NDArray[np.int_]
        :param **kwargs:
        :type **kwargs: Any
        :returns: The genotypes of the children.
        :rtype: list[Genotype]
        :raises ValueError: If the parent population is not passed as a
            kwarg `parent_population`.

        """
        parent_population: Population | None = kwargs.get("parent_population")
        if parent_population is None:
            msg = "No parent population given."
            raise ValueError(msg)

        return [
            Genotype.crossover(
                parent_population.individuals[parent1_i].genotype,
                parent_population.individuals[parent2_i].genotype,
                self.rng,
            ).mutate(self.innov_db_body, self.innov_db_brain, self.rng)
            for parent1_i, parent2_i in population
        ]


def run_experiment(dbengine: Engine) -> None:
    """Run an experiment.

    :param dbengine: An openened database with matching initialize
        database structure.
    :rtype: None
    :type dbengine: Engine
    :rtype: None

    """
    logging.info("----------------")
    logging.info("Start experiment")

    # Set up the random number generator.
    rng_seed = seed_from_time()
    rng = make_rng(rng_seed)

    # Create and save the experiment instance.
    experiment = Experiment(rng_seed=rng_seed)
    logging.info("Saving experiment configuration.")
    with Session(dbengine) as session:
        session.add(experiment)
        session.commit()

    # CPPN innovation databases.
    innov_db_body = multineat.InnovationDatabase()
    innov_db_brain = multineat.InnovationDatabase()
    """Here we initialize the components used for the evolutionary process.

    - evaluator: Allows us to evaluate a population of modular robots.
    - parent_selector: Allows us to select parents from a population of modular robots.
    - survivor_selector: Allows us to select survivors from a population.
    - crossover_reproducer: Allows us to generate offspring from parents.
    - modular_robot_evolution: The evolutionary process as a object that can be iterated.
    """
    evaluator = Evaluator(
        headless=True,
        num_simulators=config.NUM_SIMULATORS,
    )
    parent_selector = ParentSelector(
        offspring_size=config.OFFSPRING_SIZE, rng=rng
    )
    survivor_selector = SurvivorSelector(rng=rng)
    crossover_reproducer = CrossoverReproducer(
        rng=rng, innov_db_body=innov_db_body, innov_db_brain=innov_db_brain
    )

    modular_robot_evolution = ModularRobotEvolution(
        parent_selection=parent_selector,
        survivor_selection=survivor_selector,
        evaluator=evaluator,
        reproducer=crossover_reproducer,
    )

    # Create an initial population, as we cant start from nothing.
    logging.info("Generating initial population.")
    initial_genotypes = [
        Genotype.random(
            innov_db_body=innov_db_body,
            innov_db_brain=innov_db_brain,
            rng=rng,
        )
        for _ in range(config.POPULATION_SIZE)
    ]

    # Evaluate the initial population.
    logging.info("Evaluating initial population.")
    initial_fitnesses = evaluator.evaluate(initial_genotypes)

    # Create a population of individuals, combining genotype with fitness.
    population = Population(
        individuals=[
            Individual(
                genotype=genotype,
                fitness=fitness,
            )
            for genotype, fitness in zip(
                initial_genotypes, initial_fitnesses, strict=True
            )
        ]
    )

    # Finish the zeroth generation and save it to the database.
    generation = Generation(
        experiment=experiment, generation_index=0, population=population
    )
    save_to_db(dbengine, generation)

    # Start the actual optimization process.
    logging.info("Start optimization process.")
    while generation.generation_index < config.NUM_GENERATIONS:
        logging.info(
            "Generation %d / %d.",
            generation.generation_index + 1,
            config.NUM_GENERATIONS,
        )

        # Here we iterate the evolutionary process using the step.
        population = modular_robot_evolution.step(population)

        # Make it all into a generation and save it to the database.
        generation = Generation(
            experiment=experiment,
            generation_index=generation.generation_index + 1,
            population=population,
        )
        save_to_db(dbengine, generation)
        plot_fig()


def main() -> None:
    """Run the program.


    :rtype: None

    """
    # Set up logging.
    setup_logging(file_name="log.txt")

    # Open the database, only if it does not already exists.
    dbengine = open_database_sqlite(
        db_file=config.DATABASE_FILE,
        open_method=OpenMethod.OVERWRITE_IF_EXISTS,
    )
    # Create the structure of the database.
    Base.metadata.create_all(dbengine)

    # Run the experiment several times.
    for id in range(config.NUM_REPETITIONS):
        run_experiment(dbengine)
        rerun_main(id + 1)


def save_to_db(dbengine: Engine, generation: Generation) -> None:
    """Save the current generation to the database.

    :param dbengine: The database engine.
    :type dbengine: Engine
    :param generation: The current generation.
    :rtype: None
    :type generation: Generation
    :rtype: None

    """
    logging.info("Saving generation.")
    with Session(dbengine, expire_on_commit=False) as session:
        session.add(generation)
        session.commit()


if __name__ == "__main__":
    main()
