from dataclasses import dataclass

import numpy as np
import numpy.typing as npt


@dataclass(frozen=True)
class Cpg:
    """Identifies a cpg to be used in a cpg network structure."""

    index: int


@dataclass(frozen=True, init=False)
class CpgPair:
    """A pair of CPGs that assures that the first cpg always has the lowest
    index.


    """

    # lowest is automatically set to be the lowest state index of the two
    cpg_index_lowest: Cpg
    cpg_index_highest: Cpg

    def __init__(self, cpg_1: Cpg, cpg_2: Cpg) -> None:
        """Initialize this object.

        The order of the provided CPGs is irrelevant.

        :param cpg_1: One of the CPGs part of the pair.
        :param cpg_2: The other CPG part of the pair.
        """
        # hacky but normal variable setting not possible with frozen enabled
        # https://stackoverflow.com/questions/57893902/how-can-i-set-an-attribute-in-a-frozen-dataclass-custom-init-method
        if cpg_1.index < cpg_2.index:
            object.__setattr__(self, "cpg_index_lowest", cpg_1)
            object.__setattr__(self, "cpg_index_highest", cpg_2)
        else:
            object.__setattr__(self, "cpg_index_lowest", cpg_2)
            object.__setattr__(self, "cpg_index_highest", cpg_1)


class CpgNetworkStructure:
    """Describes the structure of a CPG network.

    Can generate parameters for a CPG network, such as the initial state
    and connection weights matrix.


    """

    cpgs: list[Cpg]
    connections: set[CpgPair]

    def __init__(self, cpgs: list[Cpg], connections: set[CpgPair]) -> None:
        """Initialize this object.

        :param cpgs: The CPGs used in the structure.
        :param connections: The connections between CPGs.
        """
        assert isinstance(connections, set)

        self.cpgs = cpgs
        self.connections = connections

    @staticmethod
    def make_cpgs(num_cpgs: int) -> list[Cpg]:
        """Create a list of CPGs.

        :param num_cpgs: The number of CPGs to create.
        :type num_cpgs: int
        :returns: The created list of CPGs.
        :rtype: list[Cpg]

        """
        return [Cpg(index) for index in range(num_cpgs)]

    def make_connection_weights_matrix(
        self,
        internal_connection_weights: dict[Cpg, float],
        external_connection_weights: dict[CpgPair, float],
    ) -> npt.NDArray[np.float64]:
        """Create a weight matrix from internal and external weights.

        :param internal_connection_weights: The internal weights.
        :type internal_connection_weights: dict[Cpg, float]
        :param external_connection_weights: The external weights.
        :type external_connection_weights: dict[CpgPair, float]
        :returns: The created matrix.
        :rtype: npt.NDArray[np.float64]

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
        """Get the number of connections in the structure.


        :returns: The number of connections.

        :rtype: int

        """
        return len(self.cpgs) + len(self.connections)

    def make_connection_weights_matrix_from_params(
        self, params: list[float]
    ) -> npt.NDArray[np.float64]:
        """Create a connection weights matrix from a list if connections.

        :param params: The connections to create the matrix from.
        :type params: list[float]
        :returns: The created matrix.
        :rtype: npt.NDArray[np.float64]

        """
        assert len(params) == self.num_connections, (
            f"Expected {self.num_connections} parameters, "
            f"got {len(params)} instead."
        )

        internal_connection_weights = dict(
            zip(self.cpgs, params[: self.num_cpgs], strict=False)
        )

        external_connection_weights = dict(
            zip(self.connections, params[self.num_cpgs :], strict=False)
        )

        return self.make_connection_weights_matrix(
            internal_connection_weights, external_connection_weights
        )

    @property
    def num_states(self) -> int:
        """Get the number of states in a cpg network of this structure.

        This would be twice the number of CPGs.


        :returns: The number of states.

        :rtype: int

        """
        return len(self.cpgs) * 2

    def make_uniform_state(
        self, value: float, balanced: bool = True
    ) -> npt.NDArray[np.float64]:
        """Make a state array by repeating the same value.

        Will match the required number of states in this structure.

        :param value: The value to use for all states
        :type value: float
        :param balanced: (Default value = True)
        :type balanced: bool
        :returns: The array of states.
        :rtype: npt.NDArray[np.float64]

        """
        if not balanced:
            return np.full(self.num_states, value)
        # The first half of the state array is positive, the second half is negative.
        #   this makes the CPGs oscillate in opposite directions:
        #   producing a more stable gait.
        first_half = np.full(self.num_states // 2, value)
        second_half = np.full(self.num_states // 2, -value)
        return np.concatenate((first_half, second_half))

    @property
    def num_cpgs(self) -> int:
        """Get the number of CPGs in the structure.


        :returns: The number of CPGs.

        :rtype: int

        """
        return len(self.cpgs)

    @property
    def output_indices(self) -> list[int]:
        """Get the index in the state array for each cpg, matching the order
        the CPGs were provided in.


        :returns: The indices.

        :rtype: list[int]

        """
        return list(range(self.num_cpgs))
