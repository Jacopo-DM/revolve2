from abc import ABC, abstractmethod

from revolve2.modular_robot_simulation._build_multi_body_systems._body_to_multi_body_system_mapping import (
    BodyToMultiBodySystemMapping,
)
from revolve2.modular_robot_simulation._build_multi_body_systems._unbuilt_child import (
    UnbuiltChild,
)
from revolve2.simulation.scene import MultiBodySystem


class Builder(ABC):
    """An abstract builder class."""

    @abstractmethod
    def build(
        self,
        multi_body_system: MultiBodySystem,
        body_to_multi_body_system_mapping: BodyToMultiBodySystemMapping,
    ) -> list[UnbuiltChild]:
        """Build a module onto the Robot.

        :param multi_body_system: The multi body system of the robot.
        :param body_to_multi_body_system_mapping: A mapping from body to multi-body system
        :return: The next children to be built.
        """
