"""
This module defines the Cpg, CpgPair, and CpgNetworkStructure classes, which are used to represent the structure of a central pattern generator (CPG) network.
"""

from dataclasses import dataclass

import numpy as np
import numpy.typing as npt


@dataclass(frozen=True)
class Cpg:
    """Identifies a CPG to be used in a CPG network structure."""

    index: int


@dataclass(frozen=True, init=False)
class CpgPair:
    """A pair of CPGs that assures that the first CPG always has the lowest index."""

    cpg_index_lowest: Cpg
    cpg_index_highest: Cpg

    def __init__(self, cpg_1: Cpg, cpg_2: Cpg) -> None:
        """
        Initialize this object.

        The order of the provided CPGs is irrelevant.

        :param cpg_1: One of the CPGs part of the pair.
        :param cpg_2: The other CPG part of the pair.
        """
        if cpg_1.index < cpg_2.index:
            object.__setattr__(self, "cpg_index_lowest", cpg_1)
            object.__setattr__(self, "cpg_index_highest", cpg_2)
        else:
            object.__setattr__(self, "cpg_index_lowest", cpg_2)
            object.__setattr__(self, "cpg_index_highest", cpg_1)


class CpgNetworkStructure:
    """
    Describes the structure of a CPG network.

    Can generate parameters for a CPG network, such as the initial state and connection weights matrix.
    """

    cpgs: list[Cpg]
    connections: set[CpgPair]

    def __init__(self, cpgs: list[Cpg], connections: set[CpgPair]) -> None:
        """
        Initialize this object.

        :param cpgs: The CPGs used in the structure.
        :param connections: The connections between CPGs.
        """
        assert isinstance(connections, set)

        self.cpgs = cpgs
        self.connections = connections

    @staticmethod
    def make_cpgs(num_cpgs: int) -> list[Cpg]:
        """
        Create a list of CPGs.

        :param num_cpgs: The number of CPGs to create.
        :returns: The created list of CPGs.
        """
        return [Cpg(index) for index in range(num_cpgs)]

    def make_connection_weights_matrix(
        self,
        internal_connection_weights: dict[Cpg, float],
        external_connection_weights: dict[CpgPair, float],
    ) -> npt.NDArray[np.float_]:
        """
        Create a weight matrix from internal and external weights.

        :param internal_connection_weights: The internal weights.
        :param external_connection_weights: The external weights.
        :returns: The created matrix.
        """
        state_size = self.num_cpgs * 2

        assert set(internal_connection_weights.keys()) == set(self.cpgs)
        assert set(external_connection_weights.keys()) == self.connections

        weight_matrix = np.zeros((state_size, state_size))

        for cpg, weight in internal_connection_weights.items():
            weight_matrix[cpg.index][self.num_cpgs + cpg.index] = weight
            weight_matrix[self.num_cpgs + cpg.index][cpg.index] = -weight

        for cpg_pair, weight in external_connection_weights.items():
            weight_matrix[cpg_pair.cpg_index_lowest.index][
                cpg_pair.cpg_index_highest.index
            ] = weight
            weight_matrix[cpg_pair.cpg_index_highest.index][
                cpg_pair.cpg_index_lowest.index
            ] = -weight

        return weight_matrix

    @property
    def num_connections(self) -> int:
        """
        Get the number of connections in the structure.

        :returns: The number of connections.
        """
        return len(self.cpgs) + len(self.connections)

    def make_connection_weights_matrix_from_params(
        self, params: list[float]
    ) -> npt.NDArray[np.float_]:
        """
        Create a connection weights matrix from a list if connections.

        :param params: The connections to create the matrix from.
        :returns: The created matrix.
        """
        assert len(params) == self.num_connections, (
            f"Expected {self.num_connections} parameters, "
            f"got {len(params)} instead."
        )

        internal_connection_weights = dict(zip(self.cpgs, params[: self.num_cpgs]))

        external_connection_weights = dict(
            zip(self.connections, params[self.num_cpgs :])
        )

        return self.make_connection_weights_matrix(
            internal_connection_weights, external_connection_weights
        )

    @property
    def num_states(self) -> int:
        """
        Get the number of states in a CPG network of this structure.

        This would be twice the number of CPGs.

        :returns: The number of states.
        """
        return len(self.cpgs) * 2

    def make_uniform_state(self, value: float) -> npt.NDArray[np.float_]:
        """
        Make a state array by repeating the same value.

        Will match the required number of states in this structure.

        :param value: The value to use for all states.
        :returns: The array of states.
        """
        return np.full(self.num_states, value)

    @property
    def num_cpgs(self) -> int:
        """
        Get the number of CPGs in the structure.

        :returns: The number of CPGs.
        """
        return len(self.cpgs)

    @property
    def output_indices(self) -> list[int]:
        """
        Get the index in the state array for each CPG, matching the order the CPGs were provided in.

        :returns: The indices.
        """
        return list(range(self.num_cpgs))
