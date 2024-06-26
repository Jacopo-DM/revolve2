from abc import ABC, abstractmethod

from ._control_interface import ControlInterface
from ._simulation_state import SimulationState


class SimulationHandler(ABC):
    """Base class for handling a simulation, which includes, for example,
    controlling robots.


    """

    @abstractmethod
    def handle(
        self, state: SimulationState, control: ControlInterface, dt: float
    ) -> None:
        """Handle a simulation frame.

        :param state: The current state of the simulation.
        :type state: SimulationState
        :param control: Interface for setting control targets.
        :type control: ControlInterface
        :param dt: The time since the last call to this function.
        :rtype: None
        :type dt: float
        :rtype: None

        """
