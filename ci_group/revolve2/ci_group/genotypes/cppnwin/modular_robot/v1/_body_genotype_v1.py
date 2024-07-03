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
from ._body_develop import develop as develop_body_v1

if TYPE_CHECKING:
    import numpy as np
    from revolve2.modular_robot.body.v1 import BodyV1


@dataclass
class BodyGenotypeV1:
    """CPPNWIN body genotype."""

    _NUM_INITIAL_MUTATIONS = 5
    _MULTINEAT_PARAMS = get_multineat_params()
    body: MultineatGenotypePickleWrapper

    @classmethod
    def random_body(
        cls,
        innov_db: multineat.InnovationDatabase,
        rng: np.random.Generator,
    ) -> BodyGenotypeV1:
        """Create a random genotype.

        :param innov_db: Multineat innovation database. See Multineat
            library.
        :type innov_db: multineat.InnovationDatabase
        :param rng: Random number generator.
        :type rng: np.random.Generator
        :returns: The created genotype.
        :rtype: BodyGenotypeV1

        """
        multineat_rng = multineat_rng_from_random(rng)

        body = MultineatGenotypePickleWrapper(
            random_multineat_genotype(
                innov_db=innov_db,
                rng=multineat_rng,
                multineat_params=cls._MULTINEAT_PARAMS,
                output_activation_func=multineat.ActivationFunction.SOFTPLUS,
                # bias(always 1), pos_x, pos_y, pos_z, chain_length
                num_inputs=5,
                # empty, brick, activehinge, rotation
                num_outputs=4,
                num_initial_mutations=cls._NUM_INITIAL_MUTATIONS,
            )
        )

        return BodyGenotypeV1(body)

    def mutate_body(
        self,
        innov_db: multineat.InnovationDatabase,
        rng: np.random.Generator,
    ) -> BodyGenotypeV1:
        """Mutate this genotype.

        This genotype will not be changed; a mutated copy will be
        returned.

        :param innov_db: Multineat innovation database. See Multineat
            library.
        :type innov_db: multineat.InnovationDatabase
        :param rng: Random number generator.
        :type rng: np.random.Generator
        :returns: A mutated copy of the provided genotype.
        :rtype: BodyGenotypeV1

        """
        multineat_rng = multineat_rng_from_random(rng)

        return BodyGenotypeV1(
            MultineatGenotypePickleWrapper(
                self.body.genotype.MutateWithConstraints(
                    False,
                    multineat.SearchMode.BLENDED,
                    innov_db,
                    self._MULTINEAT_PARAMS,
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
    ) -> BodyGenotypeV1:
        """Perform crossover between two genotypes.

        :param parent1: The first genotype.
        :type parent1: Self
        :param parent2: The second genotype.
        :type parent2: Self
        :param rng: Random number generator.
        :type rng: np.random.Generator
        :returns: A newly created genotype.
        :rtype: BodyGenotypeV1

        """
        multineat_rng = multineat_rng_from_random(rng)

        return BodyGenotypeV1(
            MultineatGenotypePickleWrapper(
                parent1.body.genotype.MateWithConstraints(
                    parent2.body.genotype,
                    False,
                    False,
                    multineat_rng,
                    cls._MULTINEAT_PARAMS,
                )
            )
        )

    def develop_body(self) -> BodyV1:
        """Develop the genotype into a modular robot.


        :returns: The created robot.

        :rtype: BodyV1

        """
        return develop_body_v1(self.body.genotype)
