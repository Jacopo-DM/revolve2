"""Genotype class."""

from __future__ import annotations

from dataclasses import dataclass

import config
import numpy as np
import numpy.typing as npt


@dataclass
class Genotype:
    """A genotype that is a list of parameters."""

    parameters: npt.NDArray[np.float64]

    @classmethod
    def random(
        cls,
        rng: np.random.Generator,
    ) -> Genotype:
        """Create a random genotype.

        :param rng: Random number generator.
        :type rng: np.random.Generator
        :returns: The created genotype.
        :rtype: Genotype

        """
        return Genotype(rng.random(size=config.NUM_PARAMETERS) * 2 - 1)

    def mutate(
        self,
        rng: np.random.Generator,
    ) -> Genotype:
        """Mutate this genotype.

        This genotype will not be changed; a mutated copy will be
        returned.

        :param rng: Random number generator.
        :type rng: np.random.Generator
        :returns: A mutated copy of the provided genotype.
        :rtype: Genotype

        """
        return Genotype(
            rng.normal(scale=config.MUTATE_STD, size=config.NUM_PARAMETERS)
            + self.parameters
        )

    @classmethod
    def crossover(
        cls,
        parent1: Genotype,
        parent2: Genotype,
        rng: np.random.Generator,
    ) -> Genotype:
        """Perform uniform crossover between two genotypes.

        :param parent1: The first genotype.
        :type parent1: Genotype
        :param parent2: The second genotype.
        :type parent2: Genotype
        :param rng: Random number generator.
        :type rng: np.random.Generator
        :returns: A newly created genotype.
        :rtype: Genotype

        """
        mask = rng.random(config.NUM_PARAMETERS)
        return Genotype(np.where(mask, parent1.parameters, parent2.parameters))
