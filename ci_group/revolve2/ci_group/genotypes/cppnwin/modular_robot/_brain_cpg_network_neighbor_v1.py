from typing import cast

import multineat

from revolve2.modular_robot.body.base import ActiveHinge, Body
from revolve2.modular_robot.brain.cpg import (
    BrainCpgNetworkNeighbor as ModularRobotBrainCpgNetworkNeighbor,
)


class BrainCpgNetworkNeighborV1(ModularRobotBrainCpgNetworkNeighbor):
    """A CPG brain based on `ModularRobotBrainCpgNetworkNeighbor` that creates weights from a CPPNWIN network.

    Weights are determined by querying the CPPN network with inputs:
    (hinge1_posx, hinge1_posy, hinge1_posz, hinge2_posx, hinge2_posy, hinge3_posz)
    If the weight in internal, hinge1 and hinge2 position will be the same.
    """

    _genotype: multineat.Genome

    def __init__(self, genotype: multineat.Genome, body: Body) -> None:
        """Initialize this object.

        :param genotype: A multineat genome used for determining weights.
        :param body: The body of the robot.
        """
        self._genotype = genotype
        super().__init__(body)

    def _make_weights(
        self,
        active_hinges: list[ActiveHinge],
        connections: list[tuple[ActiveHinge, ActiveHinge]],
        body: Body,
    ) -> tuple[list[float], list[float]]:
        # [ ] Understand this code and check for bugs
        brain_net = multineat.NeuralNetwork()
        self._genotype.BuildPhenotype(brain_net)

        # Create a list of grid positions for each active hinge
        hinge_grid_positions = [
            body.grid_position(active_hinge) for active_hinge in active_hinges
        ]

        # Initialize an empty list for the internal weights
        internal_weights = []

        # Iterate over each grid position
        for pos in hinge_grid_positions:
            # Create the input list for the network
            network_input = [
                1.0,
                float(pos.x),
                float(pos.y),
                float(pos.z),
                float(pos.x),
                float(pos.y),
                float(pos.z),
            ]
            # Evaluate the network with the current input and append the result to the internal weights
            internal_weights.append(
                self._evaluate_network(brain_net, network_input)
            )

        # Create a list of tuples with the grid positions of each pair of connected hinges
        hinge_positions = [
            (
                body.grid_position(active_hinge1),
                body.grid_position(active_hinge2),
            )
            for (active_hinge1, active_hinge2) in connections
        ]

        # Initialize an empty list for the external weights
        external_weights = []

        # Iterate over each pair of hinge positions
        for pos1, pos2 in hinge_positions:
            # Create the input list for the network
            network_input = [
                1.0,
                float(pos1.x),
                float(pos1.y),
                float(pos1.z),
                float(pos2.x),
                float(pos2.y),
                float(pos2.z),
            ]

            # Evaluate the network with the current input and append the result to the external weights
            external_weights.append(
                self._evaluate_network(brain_net, network_input)
            )
        return (internal_weights, external_weights)

    @staticmethod
    def _evaluate_network(
        network: multineat.NeuralNetwork, inputs: list[float]
    ) -> float:
        network.Input(inputs)
        network.ActivateAllLayers()
        return cast(float, network.Output()[0])
