from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Self

import multineat

from ...cppnwin import (
    MultineatGenotypePickleWrapper,
    multineat_rng_from_random,
    random_multineat_genotype,
)
from ._brain_cpg_network_neighbor import (
    BrainCpgNetworkNeighbor,
)
from ._multineat_params import get_multineat_params

if TYPE_CHECKING:
    import numpy as np
    from revolve2.modular_robot.body.base import Body

MULTINEAT_PARAMS = get_multineat_params()
OUTPUT_ACT_F = multineat.ActivationFunction.SIGNED_SINE
SEARCH_MODE = multineat.SearchMode.BLENDED
NUM_INITIAL_MUTATIONS = 5
NUM_BRAIN_INPUTS = 7  # bias(always 1), x1, y1, z1, x2, y2, z2
NUM_BRAIN_OUTPUTS = 1  # weight


@dataclass
class BrainGenotypeCpg:
    """An SQLAlchemy model for a CPPNWIN cpg brain genotype."""

    brain: MultineatGenotypePickleWrapper

    @classmethod
    def random_brain(
        cls,
        innov_db: multineat.InnovationDatabase,
        rng: np.random.Generator,
    ) -> BrainGenotypeCpg:
        """Create a random genotype.

        :param innov_db: Multineat innovation database. See Multineat library.
        :param rng: Random number generator.
        :returns: The created genotype.
        """
        multineat_rng = multineat_rng_from_random(rng)

        brain = MultineatGenotypePickleWrapper(
            random_multineat_genotype(
                innov_db=innov_db,
                rng=multineat_rng,
                multineat_params=MULTINEAT_PARAMS,
                output_activation_func=OUTPUT_ACT_F,
                num_inputs=NUM_BRAIN_INPUTS,
                num_outputs=NUM_BRAIN_OUTPUTS,
                num_initial_mutations=NUM_INITIAL_MUTATIONS,
                search_mode=SEARCH_MODE,
            )
        )

        return BrainGenotypeCpg(brain)

    def mutate_brain(
        self,
        innov_db: multineat.InnovationDatabase,
        rng: np.random.Generator,
    ) -> BrainGenotypeCpg:
        """Mutate this genotype.

        This genotype will not be changed; a mutated copy will be returned.

        :param innov_db: Multineat innovation database. See Multineat library.
        :param rng: Random number generator.
        :returns: A mutated copy of the provided genotype.
        """
        multineat_rng = multineat_rng_from_random(rng)

        return BrainGenotypeCpg(
            MultineatGenotypePickleWrapper(
                self.brain.genotype.MutateWithConstraints(
                    False,
                    SEARCH_MODE,
                    innov_db,
                    MULTINEAT_PARAMS,
                    multineat_rng,
                )
            )
        )

    @classmethod
    def crossover_brain(
        cls,
        parent1: Self,
        parent2: Self,
        rng: np.random.Generator,
    ) -> BrainGenotypeCpg:
        """Perform crossover between two genotypes.

        :param parent1: The first genotype.
        :param parent2: The second genotype.
        :param rng: Random number generator.
        :returns: A newly created genotype.
        """
        multineat_rng = multineat_rng_from_random(rng)

        return BrainGenotypeCpg(
            MultineatGenotypePickleWrapper(
                parent1.brain.genotype.MateWithConstraints(
                    parent2.brain.genotype,
                    False,
                    False,
                    multineat_rng,
                    MULTINEAT_PARAMS,
                )
            )
        )

    def develop_brain(self, body: Body) -> BrainCpgNetworkNeighbor:
        """Develop the genotype into a modular robot.

        :param body: The body to develop the brain for.
        :returns: The created robot.
        """
        return BrainCpgNetworkNeighbor(genotype=self.brain.genotype, body=body)
