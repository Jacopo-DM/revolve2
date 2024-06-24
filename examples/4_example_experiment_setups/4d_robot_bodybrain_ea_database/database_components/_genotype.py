"""Genotype class."""

from __future__ import annotations

from typing import TYPE_CHECKING

from revolve2.ci_group.genotypes.cppnwin.modular_robot import (
    BrainGenotypeCpgOrm,
)
from revolve2.ci_group.genotypes.cppnwin.modular_robot.v2 import (
    BodyGenotypeOrmV2,
)
from revolve2.experimentation.database import HasId
from revolve2.modular_robot import ModularRobot

from ._base import Base

if TYPE_CHECKING:
    import multineat
    import numpy as np


class Genotype(Base, HasId, BodyGenotypeOrmV2, BrainGenotypeCpgOrm):
    """SQLAlchemy model for a genotype for a modular robot body and brain."""

    __tablename__ = "genotype"

    @classmethod
    def random(
        cls,
        innov_db_body: multineat.InnovationDatabase,
        innov_db_brain: multineat.InnovationDatabase,
        rng: np.random.Generator,
    ) -> Genotype:
        """Create a random genotype.

        :param innov_db_body: Multineat innovation database for the
            body. See Multineat library.
        :type innov_db_body: multineat.InnovationDatabase
        :param innov_db_brain: Multineat innovation database for the
            brain. See Multineat library.
        :type innov_db_brain: multineat.InnovationDatabase
        :param rng: Random number generator.
        :type rng: np.random.Generator
        :returns: The created genotype.
        :rtype: Genotype

        """
        body = cls.random_body(innov_db_body, rng)
        brain = cls.random_brain(innov_db_brain, rng)

        return Genotype(body=body.body, brain=brain.brain)

    def mutate(
        self,
        innov_db_body: multineat.InnovationDatabase,
        innov_db_brain: multineat.InnovationDatabase,
        rng: np.random.Generator,
    ) -> Genotype:
        """Mutate this genotype.
        
        This genotype will not be changed; a mutated copy will be
        returned.

        :param innov_db_body: Multineat innovation database for the
            body. See Multineat library.
        :type innov_db_body: multineat.InnovationDatabase
        :param innov_db_brain: Multineat innovation database for the
            brain. See Multineat library.
        :type innov_db_brain: multineat.InnovationDatabase
        :param rng: Random number generator.
        :type rng: np.random.Generator
        :returns: A mutated copy of the provided genotype.
        :rtype: Genotype

        """
        body = self.mutate_body(innov_db_body, rng)
        brain = self.mutate_brain(innov_db_brain, rng)

        return Genotype(body=body.body, brain=brain.brain)

    @classmethod
    def crossover(
        cls,
        parent1: Genotype,
        parent2: Genotype,
        rng: np.random.Generator,
    ) -> Genotype:
        """Perform crossover between two genotypes.

        :param parent1: The first genotype.
        :type parent1: Genotype
        :param parent2: The second genotype.
        :type parent2: Genotype
        :param rng: Random number generator.
        :type rng: np.random.Generator
        :returns: A newly created genotype.
        :rtype: Genotype

        """
        body = cls.crossover_body(parent1, parent2, rng)
        brain = cls.crossover_brain(parent1, parent2, rng)

        return Genotype(body=body.body, brain=brain.brain)

    def develop(self) -> ModularRobot:
        """Develop the genotype into a modular robot.


        :returns: The created robot.

        :rtype: ModularRobot

        """
        body = self.develop_body()
        brain = self.develop_brain(body=body)
        return ModularRobot(body=body, brain=brain)
