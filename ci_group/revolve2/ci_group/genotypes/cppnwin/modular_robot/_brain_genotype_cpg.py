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

MULTINEAT_PARAMS = get_multineat_params("NoveltySearch")
SEARCH_MODE = multineat.SearchMode.BLENDED

# UNSIGNED_GAUSS, LINEAR
OUTPUT_ACT_F = multineat.ActivationFunction.SIGNED_SIGMOID
# SOFTPLUS, RELU, SIGNED_STEP, TANH, TANH_CUBIC, SIGNED_SIGMOID
HIDDEN_ACT_F = multineat.ActivationFunction.SIGNED_SIGMOID

NUM_INITIAL_MUTATIONS = 5
# bias(always 1), x1, y1, z1, x2, y2, z2
NUM_BRAIN_INPUTS = 7
# weight
NUM_BRAIN_OUTPUTS = 1


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

        :param innov_db: Multineat innovation database. See Multineat
            library.
        :type innov_db: multineat.InnovationDatabase
        :param rng: Random number generator.
        :type rng: np.random.Generator
        :returns: The created genotype.
        :rtype: BrainGenotypeCpg

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
                hidden_act_f=HIDDEN_ACT_F,
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

        This genotype will not be changed; a mutated copy will be
        returned.

        :param innov_db: Multineat innovation database. See Multineat
            library.
        :type innov_db: multineat.InnovationDatabase
        :param rng: Random number generator.
        :type rng: np.random.Generator
        :returns: A mutated copy of the provided genotype.
        :rtype: BrainGenotypeCpg

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
        :type parent1: Self
        :param parent2: The second genotype.
        :type parent2: Self
        :param rng: Random number generator.
        :type rng: np.random.Generator
        :returns: A newly created genotype.
        :rtype: BrainGenotypeCpg

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
        :type body: Body
        :returns: The created robot.
        :rtype: BrainCpgNetworkNeighbor

        """
        return BrainCpgNetworkNeighbor(genotype=self.brain.genotype, body=body)
