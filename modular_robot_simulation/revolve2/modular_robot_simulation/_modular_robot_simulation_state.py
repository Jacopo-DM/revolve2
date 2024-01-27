from revolve2.modular_robot.body import Module
from revolve2.simulation.scene import MultiBodySystem, Pose, SimulationState


class ModularRobotSimulationState:
    """The state of a modular robot at some moment in a simulation."""

    _simulation_state: SimulationState
    _multi_body_system: MultiBodySystem
    """The multi-body system corresponding to the modular robot."""

    def __init__(
        self, simulation_state: SimulationState, multi_body_system: MultiBodySystem
    ) -> None:
        """
        Initialize this object.

        :param simulation_state: The simulation state corresponding to this modular robot state.
        :param multi_body_system: The multi-body system this modular robot corresponds to.
        """
        self._simulation_state = simulation_state
        self._multi_body_system = multi_body_system

    def get_pose(self) -> Pose:
        """
        Get the pose of the modular robot.

        :returns: The retrieved pose.
        """
        return self._simulation_state.get_multi_body_system_pose(
            self._multi_body_system
        )

    def get_module_relative_pose(self, module: Module) -> Pose:
        """
        Get the pose of a module, relative to its parent module's reference frame.

        In case there is no parent(the core), this is equal to getting the absolute pose.
        # TODO (returns) The relative pose.

        :param module: The module to get the pose for.
        :raises NotImplementedError: Always.
        """
        raise NotImplementedError()

    def get_module_absolute_pose(self, module: Module) -> Pose:
        """
        Get the pose of this module, relative the global reference frame.

        # TODO (returns) The absolute pose.

        :param module: The module to get the pose for.
        :raises NotImplementedError: Always.
        """
        raise NotImplementedError()