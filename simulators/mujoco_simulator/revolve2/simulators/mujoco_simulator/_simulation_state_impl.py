import mujoco
import numpy as np
import numpy.typing as npt
from pyrr import Quaternion, Vector3
from revolve2.simulation.scene import (
    JointHinge,
    MultiBodySystem,
    Pose,
    RigidBody,
    SimulationState,
    UUIDKey,
)
from revolve2.simulation.scene.sensors import CameraSensor, IMUSensor

from ._abstraction_to_mujoco_mapping import (
    AbstractionToMujocoMapping,
    MultiBodySystemMujoco,
)


class SimulationStateImpl(SimulationState):
    """Implementation of the simulation state interface for MuJoCo."""

    _xpos: npt.NDArray[np.float64]
    _xquat: npt.NDArray[np.float64]
    _qpos: npt.NDArray[np.float64]
    _sensordata: npt.NDArray[np.float64]
    _abstraction_to_mujoco_mapping: AbstractionToMujocoMapping
    _camera_views: dict[int, npt.NDArray[np.uint8]]

    def __init__(
        self,
        data: mujoco.MjData,
        abstraction_to_mujoco_mapping: AbstractionToMujocoMapping,
        camera_views: dict[int, npt.NDArray[np.uint8]],
    ) -> None:
        """Initialize this object.

        The copies required information from the provided data. As such
        the data can be modified after this constructor without causing
        problems.

        :param data: The data to copy from.
        :param abstraction_to_mujoco_mapping: A mapping between
            simulation abstraction and mujoco.
        :param camera_views: The camera views.
        """
        self._xpos = data.xpos.copy()
        self._xquat = data.xquat.copy()
        self._qpos = data.qpos.copy()
        self._sensordata = data.sensordata.copy()
        self._abstraction_to_mujoco_mapping = abstraction_to_mujoco_mapping
        self._camera_views = camera_views

    def xpos(self) -> npt.NDArray[np.float64]:
        """Get the position of all bodies.

        :returns: The positions.
        :rtype: npt.NDArray[np.float64]

        """
        return self._xpos

    def xquat(self) -> npt.NDArray[np.float64]:
        """Get the orientation of all bodies.

        :returns: The orientations.
        :rtype: npt.NDArray[np.float64]

        """
        return self._xquat

    def get_rigid_body_relative_pose(self, rigid_body: RigidBody) -> Pose:
        """Get the pose of a rigid body, relative to its parent multi-body
        system's reference frame.

        :param rigid_body: The rigid body to get the pose for.
        :type rigid_body: RigidBody
        :returns: The relative pose.
        :rtype: Pose
        :raises NotImplementedError: Always.

        """
        raise NotImplementedError

    def get_rigid_body_absolute_pose(self, rigid_body: RigidBody) -> Pose:
        """Get the pose of a rigid body, relative the global reference frame.

        :param rigid_body: The rigid body to get the pose for.
        :type rigid_body: RigidBody
        :returns: The absolute pose.
        :rtype: Pose
        :raises NotImplementedError: Always.

        """
        raise NotImplementedError

    def get_full_body(
        self, multi_body_system: MultiBodySystem
    ) -> MultiBodySystemMujoco:
        """Get the multi-body system a rigid body is part of.

        :param rigid_body: The rigid body to get the multi-body system for.
        :type rigid_body: RigidBody
        :returns: The multi-body system.
        :rtype: MultiBodySystem

        """
        return self._abstraction_to_mujoco_mapping.multi_body_system[
            UUIDKey(multi_body_system)
        ]

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
        body_mujoco = self._abstraction_to_mujoco_mapping.multi_body_system[
            UUIDKey(multi_body_system)
        ]
        return Pose(
            Vector3(self._xpos[body_mujoco.id]),
            Quaternion(self._xquat[body_mujoco.id]),
        )

    def get_hinge_joint_position(self, joint: JointHinge) -> float:
        """Get the rotational position of a hinge joint.

        :param joint: The joint to get the rotational position for.
        :type joint: JointHinge
        :returns: The rotational position.
        :rtype: float

        """
        joint_mujoco = self._abstraction_to_mujoco_mapping.hinge_joint[
            UUIDKey(joint)
        ]
        return float(self._qpos[joint_mujoco.id])

    def get_imu_specific_force(self, imu_sensor: IMUSensor) -> Vector3:
        """Get the specific force measured an IMU.

        :param imu_sensor: The IMU.
        :type imu_sensor: IMUSensor
        :returns: The specific force.
        :rtype: Vector3

        """
        accelerometer_id = self._abstraction_to_mujoco_mapping.imu_sensor[
            UUIDKey(imu_sensor)
        ].accelerometer_id
        specific_force = self._sensordata[
            accelerometer_id : accelerometer_id + 3
        ]
        return Vector3(specific_force)

    def get_imu_angular_rate(self, imu_sensor: IMUSensor) -> Vector3:
        """Get the angular rate measured by am IMU.

        :param imu_sensor: The IMU.
        :type imu_sensor: IMUSensor
        :returns: The angular rate.
        :rtype: Vector3

        """
        gyro_id = self._abstraction_to_mujoco_mapping.imu_sensor[
            UUIDKey(imu_sensor)
        ].gyro_id
        angular_rate = self._sensordata[gyro_id : gyro_id + 3]
        return Vector3(angular_rate)

    def get_camera_view(
        self, camera_sensor: CameraSensor
    ) -> npt.NDArray[np.uint8]:
        """Get the current view of the camera.

        :param camera_sensor: The camera.
        :type camera_sensor: CameraSensor
        :returns: The image (RGB).
        :rtype: npt.NDArray[np.uint8]

        """
        camera_id = self._abstraction_to_mujoco_mapping.camera_sensor[
            UUIDKey(camera_sensor)
        ].camera_id
        return self._camera_views[camera_id]
