from abc import ABC, abstractmethod

from simulation.scene import SimulationState
from simulation.simulator._batch import Batch


class Simulator(ABC):
    """Interface for a simulator."""

    @abstractmethod
    def simulate_batch(self, batch: Batch) -> list[list[SimulationState]]:
        """
        Simulate the provided batch by simulating each contained scene.

        :param batch: The batch to run.
        :returns: List of simulation states in ascending order of time.
        """
