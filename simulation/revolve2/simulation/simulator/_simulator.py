from abc import ABC, abstractmethod

from ..scene._simulation_state import SimulationState
from ._batch import Batch


class Simulator(ABC):
    """Interface for a simulator."""

    @abstractmethod
    def simulate_batch(self, batch: Batch) -> list[list[SimulationState]]:
        """Simulate the provided batch by simulating each contained scene.

        :param batch: The batch to run.
        :type batch: Batch
        :returns: List of simulation states in ascending order of time.
        :rtype: list[list[SimulationState]]

        """
