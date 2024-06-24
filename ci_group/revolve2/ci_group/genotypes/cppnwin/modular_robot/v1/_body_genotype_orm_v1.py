from __future__ import annotations

from typing import TYPE_CHECKING, Self

import multineat
from sqlalchemy import event, orm

from ..._multineat_rng_from_random import multineat_rng_from_random
from ..._random_multineat_genotype import random_multineat_genotype
from .._multineat_params import get_multineat_params
from ._body_develop import develop as develop_body_v1

if TYPE_CHECKING:
    import numpy as np
    from revolve2.modular_robot.body.v1 import BodyV1


class BodyGenotypeOrmV1(orm.MappedAsDataclass, kw_only=True):
    """SQLAlchemy model for a CPPNWIN body genotype."""

    _NUM_INITIAL_MUTATIONS = 5
    _MULTINEAT_PARAMS = get_multineat_params()

    body: multineat.Genome

    serialized_body: orm.Mapped[str] = orm.mapped_column(
        "serialized_body", init=False, nullable=False
    )

    @classmethod
    def random_body(
        cls,
        innov_db: multineat.InnovationDatabase,
        rng: np.random.Generator,
    ) -> BodyGenotypeOrmV1:
        """Create a random genotype.

        :param innov_db: Multineat innovation database. See Multineat library.
        :param rng: Random number generator.
        :returns: The created genotype.
        """
        multineat_rng = multineat_rng_from_random(rng)

        body = random_multineat_genotype(
            innov_db=innov_db,
            rng=multineat_rng,
            multineat_params=cls._MULTINEAT_PARAMS,
            output_activation_func=multineat.ActivationFunction.TANH,
            num_inputs=5,  # bias(always 1), pos_x, pos_y, pos_z, chain_length
            num_outputs=5,  # empty, brick, activehinge, rot0, rot90
            num_initial_mutations=cls._NUM_INITIAL_MUTATIONS,
        )

        return BodyGenotypeOrmV1(body=body)

    def mutate_body(
        self,
        innov_db: multineat.InnovationDatabase,
        rng: np.random.Generator,
    ) -> BodyGenotypeOrmV1:
        """Mutate this genotype.

        This genotype will not be changed; a mutated copy will be returned.

        :param innov_db: Multineat innovation database. See Multineat library.
        :param rng: Random number generator.
        :returns: A mutated copy of the provided genotype.
        """
        multineat_rng = multineat_rng_from_random(rng)

        return BodyGenotypeOrmV1(
            body=self.body.MutateWithConstraints(
                False,
                multineat.SearchMode.BLENDED,
                innov_db,
                self._MULTINEAT_PARAMS,
                multineat_rng,
            )
        )

    @classmethod
    def crossover_body(
        cls,
        parent1: Self,
        parent2: Self,
        rng: np.random.Generator,
    ) -> BodyGenotypeOrmV1:
        """Perform crossover between two genotypes.

        :param parent1: The first genotype.
        :param parent2: The second genotype.
        :param rng: Random number generator.
        :returns: A newly created genotype.
        """
        multineat_rng = multineat_rng_from_random(rng)

        return BodyGenotypeOrmV1(
            body=parent1.body.MateWithConstraints(
                parent2.body,
                False,
                False,
                multineat_rng,
                cls._MULTINEAT_PARAMS,
            )
        )

    def develop_body(self) -> BodyV1:
        """Develop the genotype into a modular robot.

        :returns: The created robot.
        """
        return develop_body_v1(self.body)


@event.listens_for(BodyGenotypeOrmV1, "before_update", propagate=True)
@event.listens_for(BodyGenotypeOrmV1, "before_insert", propagate=True)
def _update_serialized_body(
    target: BodyGenotypeOrmV1,
) -> None:
    target.serialized_body = target.body.Serialize()


@event.listens_for(BodyGenotypeOrmV1, "load", propagate=True)
def _deserialize_body(target: BodyGenotypeOrmV1) -> None:
    body = multineat.Genome()
    body.Deserialize(target.serialized_body)
    target.body = body
