import multineat
import numpy as np


def multineat_rng_from_random(rng: np.random.Generator) -> multineat.RNG:
    """Create a multineat rng object from a numpy rng state.

    :param rng: The numpy rng.
    :type rng: np.random.Generator
    :returns: The multineat rng.
    :rtype: multineat.RNG

    """
    multineat_rng = multineat.RNG()
    multineat_rng.Seed(rng.integers(0, 2**31))
    return multineat_rng
