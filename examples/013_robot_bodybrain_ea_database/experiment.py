"""Experiment class."""

from base import Base
from revolve2.experimentation.database import HasId
from sqlalchemy import orm


class Experiment(Base, HasId):
    """Experiment description."""

    __tablename__ = "experiment"

    # The seed for the rng.
    rng_seed: orm.Mapped[int] = orm.mapped_column(nullable=False)
