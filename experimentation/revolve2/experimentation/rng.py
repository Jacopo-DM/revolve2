"""Functions for standardized number generation."""

import hashlib
import logging
from datetime import datetime

import numpy as np


def seed_from_time(log_seed: bool = True) -> int:
    """Create a seed from the current time in microseconds.

    :param log_seed: If the seed should be logged. It probably should.
        (Default value = True)
    :type log_seed: bool
    :returns: The created seed.
    :rtype: int

    """
    seed = int(datetime.now().timestamp() * 1e6)
    if log_seed:
        logging.info(f"Rng seed: {seed}")
    return seed


def seed_from_string(text: str) -> int:
    """Convert a string seed to an integer seed.

    :param text: The seed as string.
    :type text: str
    :returns: The seed as integer.
    :rtype: int

    """
    return int(
        hashlib.sha256(text.encode()).hexdigest(),
        16,
    )


def make_rng(seed: int) -> np.random.Generator:
    """Create a numpy random number generator from a seed.

    :param seed: The seed to use.
    :type seed: int
    :returns: The random number generator.
    :rtype: np.random.Generator

    """
    return np.random.Generator(np.random.PCG64(seed))


def make_rng_time_seed(log_seed: bool = True) -> np.random.Generator:
    """Create a numpy random number generator from a seed.

    :param log_seed: If the automatically created seed should be logged.
        It probably should. (Default value = True)
    :type log_seed: bool
    :returns: The random number generator.
    :rtype: np.random.Generator

    """
    return np.random.Generator(np.random.PCG64(seed_from_time(log_seed)))
