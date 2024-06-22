"""Population class."""

from revolve2.experimentation.optimization.ea import (
    Population as GenericPopulation,
)

from ._base import Base
from ._individual import Individual


class Population(Base, GenericPopulation[Individual], kw_only=True):  # type: ignore[misc]
    # TODO(jmdm): Fix type error"↑"
    """A population of individuals."""

    __tablename__ = "population"
