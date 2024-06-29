from revolve2.modular_robot.body.sensors import ActiveHingeSensor
from revolve2.simulation.scene import (
    Joint,
    JointHinge,
    MultiBodySystem,
    RigidBody,
    UUIDKey,
)

from .._body_to_multi_body_system_mapping import (
    BodyToMultiBodySystemMapping,
)
from .._unbuilt_child import (
    UnbuiltChild,
)
from ._builder import (
    Builder,
)


class ActiveHingeSensorBuilder(Builder):
    """A Builder for Cores."""

    _sensor: ActiveHingeSensor

    def __init__(
        self, sensor: ActiveHingeSensor, rigid_body: RigidBody
    ) -> None:
        """Initialize the Active Hinge Sensor Builder.

        :param sensor: The sensor to be built.
        :param rigid_body: The rigid body for the module to be built on.
        """
        self._sensor = sensor
        self._rigid_body = rigid_body

    def build(
        self,
        multi_body_system: MultiBodySystem,
        body_to_multi_body_system_mapping: BodyToMultiBodySystemMapping,
    ) -> list[UnbuiltChild]:
        """Build a module onto the Robot.

        :param multi_body_system: The multi body system of the robot.
        :type multi_body_system: MultiBodySystem
        :param body_to_multi_body_system_mapping: A mapping from body to
            multi-body system
            BodyToMultiBodySystemMapping
        :type body_to_multi_body_system_mapping: BodyToMultiBodySystemMapping
        :returns: The next children to be built.
        :rtype: list[UnbuiltChild]

        """
        target: Joint | JointHinge = (
            multi_body_system.get_joints_for_rigid_body(self._rigid_body)
        )[0]

        # Check if the target is a hinge
        if not isinstance(target, JointHinge):
            msg = f"Active Hinge Sensor must be attached to a hinge. Found type: {target.__class__.__name__}"
            raise TypeError(msg)

        joint: JointHinge = target

        body_to_multi_body_system_mapping.active_hinge_sensor_to_joint_hinge[
            UUIDKey(self._sensor)
        ] = joint
        return []
