"""CPPNWIN genotypes for modular robots."""

from ._brain_cpg_network_neighbor import BrainCpgNetworkNeighbor
from ._brain_cpg_network_neighbor_v1 import BrainCpgNetworkNeighborV1
from ._brain_genotype_cpg import BrainGenotypeCpg
from ._brain_genotype_cpg_orm import BrainGenotypeCpgOrm
from ._multineat_params import get_multineat_params
from ._multineat_reference import DefaultGenome

__all__ = [
    "BrainCpgNetworkNeighbor",
    "BrainCpgNetworkNeighborV1",
    "BrainGenotypeCpg",
    "BrainGenotypeCpgOrm",
    "get_multineat_params",
    "DefaultGenome",
]
