"""Functions for combining populations in EA algorithms."""

from experimentation.optimization.ea.population_management._generational import (
    generational,
)
from experimentation.optimization.ea.population_management._steady_state import (
    steady_state,
)

__all__ = [
    "generational",
    "steady_state",
]
