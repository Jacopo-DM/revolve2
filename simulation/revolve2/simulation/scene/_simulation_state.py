from abc import ABC, abstractmethod

import numpy as np
from numpy.typing import NDArray
from pyrr import Vector3

from ._joint_hinge import JointHinge
from ._multi_body_system import MultiBodySystem
from ._pose import Pose
from ._rigid_body import RigidBody
from .sensors import CameraSensor, IMUSensor


class SimulationState(ABC):
    """Interface for the state of a simulation at certain point."""

    @abstractmethod
    def get_rigid_body_relative_pose(self, rigid_body: RigidBody) -> Pose:
        """Get the pose of a rigid body, relative to its parent multi-body
        system's reference frame.

        :param rigid_body: The rigid body to get the pose for.
        :type rigid_body: RigidBody
        :returns: The relative pose.
        :rtype: Pose

        """

    @abstractmethod
    def get_rigid_body_absolute_pose(self, rigid_body: RigidBody) -> Pose:
        """Get the pose of a rigid body, relative the global reference frame.

        :param rigid_body: The rigid body to get the pose for.
        :type rigid_body: RigidBody
        :returns: The absolute pose.
        :rtype: Pose

        """

    @abstractmethod
    def get_multi_body_system_pose(
        self, multi_body_system: MultiBodySystem
    ) -> Pose:
        """Get the pose of a multi-body system, relative to the global
        reference frame.

        :param multi_body_system: The multi-body system to get the pose
            for.
        :type multi_body_system: MultiBodySystem
        :returns: The relative pose.
        :rtype: Pose

        """

    @abstractmethod
    def get_hinge_joint_position(self, joint: JointHinge) -> float:
        """Get the rotational position of a hinge joint.

        :param joint: The joint to get the rotational position for.
        :type joint: JointHinge
        :returns: The rotational position.
        :rtype: float

        """

    @abstractmethod
    def get_imu_specific_force(self, imu_sensor: IMUSensor) -> Vector3:
        """Get the specific force measured an IMU.

        :param imu_sensor: The IMU.
        :type imu_sensor: IMUSensor
        :returns: The specific force.
        :rtype: Vector3

        """

    @abstractmethod
    def get_imu_angular_rate(self, imu_sensor: IMUSensor) -> Vector3:
        """Get the angular rate measured by am IMU.

        :param imu_sensor: The IMU.
        :type imu_sensor: IMUSensor
        :returns: The angular rate.
        :rtype: Vector3

        """

    @abstractmethod
    def get_camera_view(self, camera_sensor: CameraSensor) -> NDArray[np.uint8]:
        """Get the camera view.

        :param camera_sensor: The camera.
        :type camera_sensor: CameraSensor
        :returns: The view.
        :rtype: NDArray[np.uint8]

        """
