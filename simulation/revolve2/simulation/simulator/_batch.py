"""Batch class."""

from dataclasses import dataclass, field

from simulation.scene import Scene
from simulation.simulator import BatchParameters, RecordSettings


@dataclass
class Batch:
    """A set of scenes and shared parameters for simulation."""

    parameters: BatchParameters

    scenes: list[Scene] = field(default_factory=list, init=False)
    """The scenes to simulate."""

    record_settings: RecordSettings | None = None
