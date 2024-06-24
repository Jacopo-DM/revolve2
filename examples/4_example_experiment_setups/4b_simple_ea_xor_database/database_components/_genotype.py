"""Genotype class."""

from __future__ import annotations

import numpy as np
from revolve2.experimentation.database import HasId
from revolve2.experimentation.optimization.ea import (
    Parameters as GenericParameters,
)

from ._base import Base


class Genotype(Base, HasId, GenericParameters):
    """ORM definition for our genotype that is a list of parameters.

    In SQLAlchemy we can inherit from multiple classes that each define
    seperate table columns. Revolve2's 'GenericParameters' class defines
    our 'parameters' field. Take a short look at the class to see that
    it writes the parameters to the database as a string of semicolon
    concatenated floats.

    Besides the removed dataclass decorator(identical behavior is
    provided by SQLAlchemy), the rest of this class is exactly the same
    as the original example!


    """

    __tablename__ = "genotype"

    @classmethod
    def random(
        cls,
        rng: np.random.Generator,
        num_parameters: int,
    ) -> Genotype:
        """Create a random genotype.

        :param rng: Random number generator.
        :type rng: np.random.Generator
        :param num_parameters: Number of parameters for genotype.
        :type num_parameters: int
        :returns: The created genotype.
        :rtype: Genotype

        """
        return Genotype(parameters=(rng.random(size=num_parameters) * 2 - 1))

    def mutate(
        self,
        rng: np.random.Generator,
        mutate_std: float,
        num_parameters: int,
    ) -> Genotype:
        """Mutate this genotype.

        This genotype will not be changed; a mutated copy will be
        returned.

        :param rng: Random number generator.
        :type rng: np.random.Generator
        :param mutate_std: The mutation probability.
        :type mutate_std: float
        :param num_parameters: Number of parameters for genotype.
        :type num_parameters: int
        :returns: A mutated copy of the provided genotype.
        :rtype: Genotype

        """
        return Genotype(
            parameters=(
                rng.normal(scale=mutate_std, size=num_parameters)
                + self.parameters
            )
        )

    @classmethod
    def crossover(
        cls,
        parent1: Genotype,
        parent2: Genotype,
        rng: np.random.Generator,
        num_parameters: int,
    ) -> Genotype:
        """Perform uniform crossover between two genotypes.

        :param parent1: The first genotype.
        :type parent1: Genotype
        :param parent2: The second genotype.
        :type parent2: Genotype
        :param rng: Random number generator.
        :type rng: np.random.Generator
        :param num_parameters: The number of parameters for the
            genotype.
        :type num_parameters: int
        :returns: A newly created genotype.
        :rtype: Genotype

        """
        mask = rng.random(num_parameters)
        return Genotype(
            parameters=(np.where(mask, parent1.parameters, parent2.parameters))
        )
