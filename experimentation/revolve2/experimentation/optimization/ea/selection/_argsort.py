from collections.abc import Sequence
from typing import TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from ._supports_lt import (
        SupportsLt,
    )

Item = TypeVar("Item", bound="SupportsLt")


def argsort(seq: Sequence[Item]) -> list[int]:
    """Get the indices of the sequence sorted by value.

    :param seq: The sequence.
    :type seq: Sequence[Item]
    :returns: The indices.
    :rtype: list[int]

    """
    # http://stackoverflow.com/questions/3071415/efficient-method-to-calculate-the-rank-vector-of-a-list-in-python
    return sorted(range(len(seq)), key=seq.__getitem__)
