import math
from abc import abstractmethod

import numpy as np
import numpy.typing as npt

from ...body.base import ActiveHinge, Body
from .._brain import Brain
from .._brain_instance import BrainInstance
from ._brain_cpg_instance import BrainCpgInstance
from ._make_cpg_network_structure_neighbor import (
    active_hinges_to_cpg_network_structure_neighbor,
)


class BrainCpgNetworkNeighbor(Brain):
    """A CPG brain with active hinges that are connected if they are within 2
    jumps in the modular robot tree structure.

    That means, NOT grid coordinates, but tree distance.


    """

    _initial_state: npt.NDArray[np.float64]
    # nxn matrix matching number of neurons
    _weight_matrix: npt.NDArray[np.float64]
    _output_mapping: list[tuple[int, ActiveHinge]]

    def __init__(self, body: Body) -> None:
        """Initialize this object.

        :param body: The body to create the cpg network and brain for.
        """
        active_hinges = body.find_modules_of_type(ActiveHinge)
        (
            cpg_network_structure,
            self._output_mapping,
        ) = active_hinges_to_cpg_network_structure_neighbor(active_hinges)
        connections = [
            (
                active_hinges[pair.cpg_index_lowest.index],
                active_hinges[pair.cpg_index_highest.index],
            )
            for pair in cpg_network_structure.connections
        ]
        (internal_weights, external_weights) = self._make_weights(
            active_hinges, connections, body
        )
        self._weight_matrix = (
            cpg_network_structure.make_connection_weights_matrix(
                dict(
                    zip(
                        cpg_network_structure.cpgs,
                        internal_weights,
                        strict=False,
                    )
                ),
                dict(
                    zip(
                        cpg_network_structure.connections,
                        external_weights,
                        strict=False,
                    )
                ),
            )
        )
        # TODO(jmdm) value??
        value = 0.5 * math.sqrt(2)
        # value = 1
        self._initial_state = cpg_network_structure.make_uniform_state(
            value=value
        )

    def make_instance(self) -> BrainInstance:
        """Create an instance of this brain.

        :returns: The created instance.

        :rtype: BrainInstance

        """
        return BrainCpgInstance(
            initial_state=self._initial_state,
            weight_matrix=self._weight_matrix,
            output_mapping=self._output_mapping,
        )

    @abstractmethod
    def _make_weights(
        self,
        active_hinges: list[ActiveHinge],
        connections: list[tuple[ActiveHinge, ActiveHinge]],
        body: Body,
    ) -> tuple[list[float], list[float]]:
        """Define the weights between neurons.

        :param active_hinges: The active hinges corresponding to each
            cpg.
        :type active_hinges: list[ActiveHinge]
        :param connections: Pairs of active hinges corresponding to
            pairs of cpgs that are connected. Connection is from hinge 0
            to hinge 1. Opposite connection is not provided as weights
            are assumed to be negative.
        :type connections: list[tuple[ActiveHinge, ActiveHinge]]
        :param body: The body that matches this brain.
        :type body: Body
        :returns: Two lists. The first list contains the internal
            weights in cpgs, corresponding to `active_hinges` The second
            list contains the weights between connected cpgs,
            corresponding to `connections` The lists should match the
            order of the input parameters.
        :rtype: tuple[list[float],list[float]]

        """
