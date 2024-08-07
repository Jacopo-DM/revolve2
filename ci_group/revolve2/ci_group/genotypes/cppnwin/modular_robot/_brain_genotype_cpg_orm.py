from __future__ import annotations

from typing import TYPE_CHECKING, Self

import multineat
from sqlalchemy import event, orm

from ...cppnwin import (
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
    from sqlalchemy.engine import Connection


class BrainGenotypeCpgOrm(orm.MappedAsDataclass, kw_only=True):
    """An SQLAlchemy model for a CPPNWIN cpg brain genotype."""

    brain: multineat.Genome

    _BRAIN_MULTINEAT_PARAMS = get_multineat_params("NoveltySearch")
    _BRAIN_SEARCH_MODE = multineat.SearchMode.BLENDED

    # UNSIGNED_GAUSS, LINEAR
    _BRAIN_OUTPUT_ACT_FUNC = multineat.ActivationFunction.SIGNED_SIGMOID
    # SOFTPLUS, RELU, SIGNED_STEP, TANH, TANH_CUBIC, SIGNED_SIGMOID
    _BRAIN_HIDDEN_ACT_FUNC = multineat.ActivationFunction.SIGNED_SIGMOID

    _BRAIN_NUM_INITIAL_MUTATIONS = 5
    # bias(always 1), x1, y1, z1, x2, y2, z2
    _BRAIN_NUM_INPUTS = 7
    # weight
    _BRAIN_NUM_OUTPUTS = 1

    serialized_brain: orm.Mapped[str] = orm.mapped_column(
        "serialized_brain", init=False, nullable=False
    )

    @classmethod
    def random_brain(
        cls,
        innov_db: multineat.InnovationDatabase,
        rng: np.random.Generator,
    ) -> BrainGenotypeCpgOrm:
        """Create a random genotype.

        :param innov_db: Multineat innovation database. See Multineat
            library.
        :type innov_db: multineat.InnovationDatabase
        :param rng: Random number generator.
        :type rng: np.random.Generator
        :returns: The created genotype.
        :rtype: BrainGenotypeCpgOrm

        """
        multineat_rng = multineat_rng_from_random(rng)

        brain = random_multineat_genotype(
            innov_db=innov_db,
            rng=multineat_rng,
            multineat_params=cls._BRAIN_MULTINEAT_PARAMS,
            output_activation_func=cls._BRAIN_OUTPUT_ACT_FUNC,
            num_inputs=cls._BRAIN_NUM_INPUTS,
            num_outputs=cls._BRAIN_NUM_OUTPUTS,
            num_initial_mutations=cls._BRAIN_NUM_INITIAL_MUTATIONS,
            hidden_act_f=cls._BRAIN_HIDDEN_ACT_FUNC,
            search_mode=cls._BRAIN_SEARCH_MODE,
        )

        return BrainGenotypeCpgOrm(brain=brain)

    def mutate_brain(
        self,
        innov_db: multineat.InnovationDatabase,
        rng: np.random.Generator,
    ) -> BrainGenotypeCpgOrm:
        """Mutate this genotype.

        This genotype will not be changed; a mutated copy will be
        returned.

        :param innov_db: Multineat innovation database. See Multineat
            library.
        :type innov_db: multineat.InnovationDatabase
        :param rng: Random number generator.
        :type rng: np.random.Generator
        :returns: A mutated copy of the provided genotype.
        :rtype: BrainGenotypeCpgOrm

        """
        multineat_rng = multineat_rng_from_random(rng)

        return BrainGenotypeCpgOrm(
            brain=self.brain.MutateWithConstraints(
                False,
                self._BRAIN_SEARCH_MODE,
                innov_db,
                self._BRAIN_MULTINEAT_PARAMS,
                multineat_rng,
            )
        )

    @classmethod
    def crossover_brain(
        cls,
        parent1: Self,
        parent2: Self,
        rng: np.random.Generator,
    ) -> BrainGenotypeCpgOrm:
        """Perform crossover between two genotypes.

        :param parent1: The first genotype.
        :type parent1: Self
        :param parent2: The second genotype.
        :type parent2: Self
        :param rng: Random number generator.
        :type rng: np.random.Generator
        :returns: A newly created genotype.
        :rtype: BrainGenotypeCpgOrm

        """
        multineat_rng = multineat_rng_from_random(rng)

        return BrainGenotypeCpgOrm(
            brain=parent1.brain.MateWithConstraints(
                parent2.brain,
                False,
                False,
                multineat_rng,
                cls._BRAIN_MULTINEAT_PARAMS,
            )
        )

    def develop_brain(self, body: Body) -> BrainCpgNetworkNeighbor:
        """Develop the genotype into a modular robot.

        :param body: The body to develop the brain for.
        :type body: Body
        :returns: The created robot.
        :rtype: BrainCpgNetworkNeighbor

        """
        return BrainCpgNetworkNeighbor(genotype=self.brain, body=body)


@event.listens_for(BrainGenotypeCpgOrm, "before_update", propagate=True)
@event.listens_for(BrainGenotypeCpgOrm, "before_insert", propagate=True)
def _serialize_brain(
    mapper: orm.Mapper[BrainGenotypeCpgOrm],
    connection: Connection,
    target: BrainGenotypeCpgOrm,
) -> None:
    """:param mapper:
    :type mapper: orm.Mapper[BrainGenotypeCpgOrm]
    :param connection:
    :type connection: Connection
    :param target:
    :type target: BrainGenotypeCpgOrm
    :rtype: None

    """
    target.serialized_brain = target.brain.Serialize()


@event.listens_for(BrainGenotypeCpgOrm, "load", propagate=True)
def _deserialize_brain(
    target: BrainGenotypeCpgOrm, context: orm.QueryContext
) -> None:
    """:param target:
    :type target: BrainGenotypeCpgOrm
    :param context:
    :type context: orm.QueryContext
    :rtype: None

    """
    brain = multineat.Genome()
    brain.Deserialize(target.serialized_brain)
    target.brain = brain
