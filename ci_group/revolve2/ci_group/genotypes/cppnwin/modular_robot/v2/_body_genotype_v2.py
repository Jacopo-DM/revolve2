from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Self

import multineat

from ... import (
    MultineatGenotypePickleWrapper,
    multineat_rng_from_random,
    random_multineat_genotype,
)
from ...modular_robot import (
    get_multineat_params,
)
from ._body_develop import (
    develop as develop_body_v2,
)

if TYPE_CHECKING:
    import numpy as np
    from revolve2.modular_robot.body.v2 import BodyV2

MULTINEAT_PARAMS = get_multineat_params("NoveltySearch")
SEARCH_MODE = multineat.SearchMode.BLENDED

# SOFTPLUS RELU TANH SIGNED_SIGMOID
OUTPUT_ACT_F = multineat.ActivationFunction.TANH
# SOFTPLUS, RELU, SIGNED_STEP, TANH, TANH_CUBIC, SIGNED_SIGMOID
HIDDEN_ACT_F = multineat.ActivationFunction.TANH

NUM_INITIAL_MUTATIONS = 5
# bias(always 1), pos_x, pos_y, pos_z, chain_length
NUM_BODY_INPUTS = 1 + 3 + 1
# 'empty, brick, activehinge' + 'rot1, rot2, rot3, rot4' + 'bias'
NUM_BODY_OUTPUTS = 3 + 4 + 1


@dataclass
class BodyGenotypeV2:
    """CPPNWIN body genotype."""

    body: MultineatGenotypePickleWrapper

    @classmethod
    def random_body(
        cls,
        innov_db: multineat.InnovationDatabase,
        rng: np.random.Generator,
    ) -> BodyGenotypeV2:
        """Create a random genotype.

        :param innov_db: Multineat innovation database. See Multineat
            library.
        :type innov_db: multineat.InnovationDatabase
        :param rng: Random number generator.
        :type rng: np.random.Generator
        :returns: The created genotype.
        :rtype: BodyGenotypeV2

        """
        multineat_rng = multineat_rng_from_random(rng)

        body = MultineatGenotypePickleWrapper(
            random_multineat_genotype(
                innov_db=innov_db,
                rng=multineat_rng,
                multineat_params=MULTINEAT_PARAMS,
                output_activation_func=OUTPUT_ACT_F,
                num_inputs=NUM_BODY_INPUTS,
                num_outputs=NUM_BODY_OUTPUTS,
                num_initial_mutations=NUM_INITIAL_MUTATIONS,
                hidden_act_f=HIDDEN_ACT_F,
                search_mode=SEARCH_MODE,
            )
        )

        return BodyGenotypeV2(body)

    def mutate_body(
        self,
        innov_db: multineat.InnovationDatabase,
        rng: np.random.Generator,
    ) -> BodyGenotypeV2:
        """Mutate this genotype.

        This genotype will not be changed; a mutated copy will be
        returned.

        :param innov_db: Multineat innovation database. See Multineat
            library.
        :type innov_db: multineat.InnovationDatabase
        :param rng: Random number generator.
        :type rng: np.random.Generator
        :returns: A mutated copy of the provided genotype.
        :rtype: BodyGenotypeV2

        """
        multineat_rng = multineat_rng_from_random(rng)

        return BodyGenotypeV2(
            MultineatGenotypePickleWrapper(
                self.body.genotype.MutateWithConstraints(
                    False,
                    SEARCH_MODE,
                    innov_db,
                    MULTINEAT_PARAMS,
                    multineat_rng,
                )
            )
        )

    @classmethod
    def crossover_body(
        cls,
        parent1: Self,
        parent2: Self,
        rng: np.random.Generator,
    ) -> BodyGenotypeV2:
        """Perform crossover between two genotypes.

        :param parent1: The first genotype.
        :type parent1: Self
        :param parent2: The second genotype.
        :type parent2: Self
        :param rng: Random number generator.
        :type rng: np.random.Generator
        :returns: A newly created genotype.
        :rtype: BodyGenotypeV2

        """
        multineat_rng = multineat_rng_from_random(rng)

        return BodyGenotypeV2(
            MultineatGenotypePickleWrapper(
                parent1.body.genotype.MateWithConstraints(
                    parent2.body.genotype,
                    False,
                    False,
                    multineat_rng,
                    MULTINEAT_PARAMS,
                )
            )
        )

    def develop_body(self) -> BodyV2:
        """Develop the genotype into a modular robot.


        :returns: The created robot.

        :rtype: BodyV2

        """
        return develop_body_v2(self.body.genotype)
