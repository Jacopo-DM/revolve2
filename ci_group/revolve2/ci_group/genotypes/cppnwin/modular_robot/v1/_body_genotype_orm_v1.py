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

    body: multineat.Genome

    _BODY_MULTINEAT_PARAMS = get_multineat_params()
    _BODY_SEARCH_MODE = multineat.SearchMode.BLENDED

    # SOFTPLUS RELU TANH SIGNED_SIGMOID
    _BODY_OUTPUT_ACT_FUNC = multineat.ActivationFunction.SOFTPLUS
    # SOFTPLUS, RELU, SIGNED_STEP, TANH, TANH_CUBIC, SIGNED_SIGMOID
    _BODY_HIDDEN_ACT_FUNC = multineat.ActivationFunction.SOFTPLUS

    _BODY_NUM_INITIAL_MUTATIONS = 5
    # bias(always 1), pos_x, pos_y, pos_z, chain_length
    _BODY_NUM_INPUTS = 5
    # empty, brick, activehinge, rotation
    _BODY_NUM_OUTPUTS = 4

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

        :param innov_db: Multineat innovation database. See Multineat
            library.
        :type innov_db: multineat.InnovationDatabase
        :param rng: Random number generator.
        :type rng: np.random.Generator
        :returns: The created genotype.
        :rtype: BodyGenotypeOrmV1
        """
        multineat_rng = multineat_rng_from_random(rng)

        body = random_multineat_genotype(
            innov_db=innov_db,
            rng=multineat_rng,
            multineat_params=cls._BODY_MULTINEAT_PARAMS,
            output_activation_func=cls._BODY_OUTPUT_ACT_FUNC,
            num_inputs=cls._BODY_NUM_INPUTS,
            num_outputs=cls._BODY_NUM_OUTPUTS,
            num_initial_mutations=cls._BODY_NUM_INITIAL_MUTATIONS,
            hidden_act_f=cls._BODY_HIDDEN_ACT_FUNC,
            search_mode=cls._BODY_SEARCH_MODE,
        )

        return BodyGenotypeOrmV1(body=body)

    def mutate_body(
        self,
        innov_db: multineat.InnovationDatabase,
        rng: np.random.Generator,
    ) -> BodyGenotypeOrmV1:
        """Mutate this genotype.

        This genotype will not be changed; a mutated copy will be
        returned.

        :param innov_db: Multineat innovation database. See Multineat
            library.
        :type innov_db: multineat.InnovationDatabase
        :param rng: Random number generator.
        :type rng: np.random.Generator
        :returns: A mutated copy of the provided genotype.
        :rtype: BodyGenotypeOrmV1
        """
        multineat_rng = multineat_rng_from_random(rng)

        return BodyGenotypeOrmV1(
            body=self.body.MutateWithConstraints(
                False,
                self._BODY_SEARCH_MODE,
                innov_db,
                self._BODY_MULTINEAT_PARAMS,
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
        :type parent1: Self
        :param parent2: The second genotype.
        :type parent2: Self
        :param rng: Random number generator.
        :type rng: np.random.Generator
        :returns: A newly created genotype.
        :rtype: BodyGenotypeOrmV1
        """
        multineat_rng = multineat_rng_from_random(rng)

        return BodyGenotypeOrmV1(
            body=parent1.body.MateWithConstraints(
                parent2.body,
                False,
                False,
                multineat_rng,
                cls._BODY_MULTINEAT_PARAMS,
            )
        )

    def develop_body(self) -> BodyV1:
        """Develop the genotype into a modular robot.

        :returns: The created robot.
        :rtype: BodyV1
        """
        return develop_body_v1(self.body)


@event.listens_for(BodyGenotypeOrmV1, "before_update", propagate=True)
@event.listens_for(BodyGenotypeOrmV1, "before_insert", propagate=True)
def _update_serialized_body(
    target: BodyGenotypeOrmV1,
) -> None:
    """:param target:
    :type target: BodyGenotypeOrmV1
    :rtype: None
    """
    target.serialized_body = target.body.Serialize()


@event.listens_for(BodyGenotypeOrmV1, "load", propagate=True)
def _deserialize_body(target: BodyGenotypeOrmV1) -> None:
    """:param target:
    :type target: BodyGenotypeOrmV1
    :rtype: None
    """
    body = multineat.Genome()
    body.Deserialize(target.serialized_body)
    target.body = body
