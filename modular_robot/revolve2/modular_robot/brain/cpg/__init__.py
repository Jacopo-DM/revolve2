"""CPG brains for modular robots."""

from modular_robot.brain.cpg._brain_cpg_instance import BrainCpgInstance
from modular_robot.brain.cpg._brain_cpg_network_neighbor import (
    BrainCpgNetworkNeighbor,
)
from modular_robot.brain.cpg._brain_cpg_network_neighbor_random import (
    BrainCpgNetworkNeighborRandom,
)
from modular_robot.brain.cpg._brain_cpg_network_static import (
    BrainCpgNetworkStatic,
)
from modular_robot.brain.cpg._cpg_network_structure import CpgNetworkStructure
from modular_robot.brain.cpg._make_cpg_network_structure_neighbor import (
    active_hinges_to_cpg_network_structure_neighbor,
)

__all__ = [
    "BrainCpgInstance",
    "BrainCpgNetworkNeighbor",
    "BrainCpgNetworkNeighborRandom",
    "BrainCpgNetworkStatic",
    "CpgNetworkStructure",
    "active_hinges_to_cpg_network_structure_neighbor",
]
