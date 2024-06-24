from revolve2.modular_robot.brain import BrainInstance
from revolve2.simulation.scene import (
    ControlInterface,
    SimulationHandler,
    SimulationState,
)

from ._build_multi_body_systems import (
    BodyToMultiBodySystemMapping,
)
from ._modular_robot_control_interface_impl import (
    ModularRobotControlInterfaceImpl,
)
from ._sensor_state_impl import (
    ModularRobotSensorStateImpl,
)


class ModularRobotSimulationHandler(SimulationHandler):
    """Implements the simulation handler for a modular robot scene."""

    _brains: list[tuple[BrainInstance, BodyToMultiBodySystemMapping]]

    def __init__(self) -> None:
        """Initialize this object."""
        self._brains = []

    def add_robot(
        self,
        brain_instance: BrainInstance,
        body_to_multi_body_system_mapping: BodyToMultiBodySystemMapping,
    ) -> None:
        """Add a brain that will control a robot during simulation.

        :param brain_instance: The brain.
        :type brain_instance: BrainInstance
        :param body_to_multi_body_system_mapping: A mapping from body to
            multi-body system
        :type body_to_multi_body_system_mapping: BodyToMultiBodySystemMapping
        :rtype: None

        """
        self._brains.append((brain_instance, body_to_multi_body_system_mapping))

    def handle(
        self,
        simulation_state: SimulationState,
        simulation_control: ControlInterface,
        dt: float,
    ) -> None:
        """Handle a simulation frame.

        :param simulation_state: The current state of the simulation.
        :type simulation_state: SimulationState
        :param simulation_control: Interface for setting control
            targets.
        :type simulation_control: ControlInterface
        :param dt: The time since the last call to this function.
        :type dt: float
        :rtype: None

        """
        for brain_instance, body_to_multi_body_system_mapping in self._brains:
            sensor_state = ModularRobotSensorStateImpl(
                simulation_state=simulation_state,
                body_to_multi_body_system_mapping=body_to_multi_body_system_mapping,
            )
            control = ModularRobotControlInterfaceImpl(
                simulation_control=simulation_control,
                body_to_multi_body_system_mapping=body_to_multi_body_system_mapping,
            )
            brain_instance.control(
                dt=dt, sensor_state=sensor_state, control_interface=control
            )
