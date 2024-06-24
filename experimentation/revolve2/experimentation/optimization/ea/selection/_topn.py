from typing import TypeVar

from ._argsort import argsort
from ._supports_lt import SupportsLt

Genotype = TypeVar("Genotype")
Fitness = TypeVar("Fitness", bound=SupportsLt)


def topn(
    n: int, genotypes: list[Genotype], fitnesses: list[Fitness]
) -> list[int]:
    """Get indices of the top n genotypes sorted by their fitness.

    :param n: The number of genotypes to select.
    :type n: int
    :param genotypes: The genotypes. Ignored, but argument kept for
        function signature compatibility with other selection functions/
    :type genotypes: list[Genotype]
    :param fitnesses: Fitnesses of the genotypes.
    :type fitnesses: list[Fitness]
    :returns: Indices of the selected genotypes.
    :rtype: list[int]

    """
    assert len(fitnesses) >= n

    return argsort(fitnesses)[::-1][:n]
