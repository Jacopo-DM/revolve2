"""Experiment class."""

from revolve2.experimentation.database import HasId
from sqlalchemy import orm

from ._base import Base


class Experiment(Base, HasId):  # type: ignore[misc]
    # TODO(jmdm): Fix type error"↑"
    """Experiment description."""

    __tablename__ = "experiment"

    # The seed for the rng.
    rng_seed: orm.Mapped[int] = orm.mapped_column(nullable=False)
