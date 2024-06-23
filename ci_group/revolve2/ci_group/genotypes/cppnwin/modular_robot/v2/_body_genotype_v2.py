from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Self

import multineat

from revolve2.ci_group.genotypes.cppnwin import (
    MultineatGenotypePickleWrapper,
    multineat_rng_from_random,
    random_multineat_genotype,
)
from revolve2.ci_group.genotypes.cppnwin.modular_robot import (
    get_multineat_params,
)

from ._body_develop import (
    develop as develop_body_v2,
)

if TYPE_CHECKING:
    import numpy as np

    from revolve2.modular_robot.body.v2 import BodyV2

MULTINEAT_PARAMS = get_multineat_params()
# TODO(jmdm): what act_f to use?
OUTPUT_ACT_F = multineat.ActivationFunction.UNSIGNED_SINE
SEARCH_MODE = multineat.SearchMode.BLENDED
NUM_INITIAL_MUTATIONS = 5
NUM_BODY_INPUTS = 5  # bias(always 1), pos_x, pos_y, pos_z, chain_length
NUM_BODY_OUTPUTS = 5  # empty, brick, activehinge, rot0, rot90


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

        :param innov_db: Multineat innovation database. See Multineat library.
        :param rng: Random number generator.
        :returns: The created genotype.
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

        This genotype will not be changed; a mutated copy will be returned.

        :param innov_db: Multineat innovation database. See Multineat library.
        :param rng: Random number generator.
        :returns: A mutated copy of the provided genotype.
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
        :param parent2: The second genotype.
        :param rng: Random number generator.
        :returns: A newly created genotype.
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
        """
        return develop_body_v2(self.body.genotype)
