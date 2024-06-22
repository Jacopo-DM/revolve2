from typing import TypeVar

import numpy as np

Fitness = TypeVar("Fitness")


def tournament(
    rng: np.random.Generator, fitnesses: list[Fitness], k: int
) -> int:
    """
    Perform tournament selection and return the index of the best individual.

    :param rng: Random number generator.
    :param fitnesses: List of finesses of individuals that joint the tournament.
    :param k: Amount of individuals to participate in tournament.
    :returns: The index of te individual that won the tournament.
    """
    if len(fitnesses) < k:
        msg = f"Expected at least {k} fitnesses, got {len(fitnesses)}."
        raise ValueError(msg)

    participant_indices = rng.choice(range(len(fitnesses)), size=k)
    return int(max(participant_indices, key=lambda i: fitnesses[i]))
