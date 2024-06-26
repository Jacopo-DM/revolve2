import uuid
from dataclasses import dataclass, field

from pyrr import Matrix33, Quaternion, Vector3

from ._pose import Pose
from .geometry import (
    Geometry,
    GeometryBox,
    GeometrySphere,
)
from .sensors import CameraSensor, IMUSensor, Sensor


@dataclass
class _AttachedSensors:
    """"""

    imu_sensors: list[IMUSensor] = field(default_factory=list)
    camera_sensors: list[CameraSensor] = field(default_factory=list)

    def add_sensor(self, sensor: Sensor) -> None:
        """Add sensor to the AttachedSensors object.

        :param sensor: The sensor
        :type sensor: Sensor
        :rtype: None
        :raises ValueError: If the sensor type is unknown.
        """
        match sensor:
            case IMUSensor():
                self.imu_sensors.append(sensor)
            case CameraSensor():
                self.camera_sensors.append(sensor)
            case _:
                msg = f"Sensor of type: {type(sensor)} is not defined for _rigid_body._AttachedSensors"
                raise ValueError(msg)


class RigidBody:
    """A collection of geometries and physics parameters."""

    _uuid: uuid.UUID
    initial_pose: Pose
    static_friction: float
    dynamic_friction: float
    geometries: list[Geometry]
    sensors: _AttachedSensors

    def __init__(
        self,
        initial_pose: Pose,
        static_friction: float,
        dynamic_friction: float,
        geometries: list[Geometry],
    ) -> None:
        """Initialize the rigid body object.

        :param initial_pose: The Initial pose of the rigid body.
            Relative to its parent multi-body system.
        :param static_friction: Static friction of the body.
        :param dynamic_friction: Dynamic friction of the body.
        :param geometries: Geometries describing the shape of the body.
        """
        self._uuid = uuid.uuid1()
        self.initial_pose = initial_pose
        self.static_friction = static_friction
        self.dynamic_friction = dynamic_friction
        self.geometries = geometries
        self.sensors = _AttachedSensors()

    @property
    def uuid(self) -> uuid.UUID:
        """Get the uuid.

        :returns: The uuid.
        :rtype: uuid.UUID
        """
        return self._uuid

    def mass(self) -> float:
        """Get mass of the rigid body.

        :returns: The mass.
        :rtype: float
        """
        return sum(geometry.mass for geometry in self.geometries)

    def center_of_mass(self) -> Vector3:
        """Calculate the center of mass in the local reference frame of this
        rigid body.

        If no geometry has mass, the average position of all geometries
        is returned, unweighted.

        :returns: The center of mass.
        :rtype: Vector3
        """
        if self.mass() == 0:
            return sum(
                geometry.mass * geometry.pose.position
                for geometry in self.geometries
            ) / len(self.geometries)
        return (
            sum(
                geometry.mass * geometry.pose.position
                for geometry in self.geometries
            )
            / self.mass()
        )

    def inertia_tensor(self) -> Matrix33:
        """Calculate the inertia tensor in the local reference frame of this
        rigid body.

        For more details on the inertia calculations, see
        https://en.wikipedia.org/wiki/List_of_moments_of_inertia.

        :returns: The inertia tensor.
        :rtype: Matrix33
        :raises ValueError: If one of the geometries is not a box.
        """
        com = self.center_of_mass()
        inertia = Matrix33()

        for geometry in self.geometries:
            if geometry.mass == 0:
                continue

            match geometry:
                case GeometryBox():
                    local_inertia = self._calculate_box_inertia(geometry)
                case GeometrySphere():
                    local_inertia = self._calculate_sphere_inertia(geometry)
                case _:
                    msg = f"Geometries with non-zero mass of type {type(geometry)} are not supported yet."
                    raise ValueError(msg)

            translation = Matrix33()
            translation[0, 0] += geometry.mass * (
                (geometry.pose.position.y - com.y) ** 2
                + (geometry.pose.position.z - com.z) ** 2
            )
            translation[1, 1] += geometry.mass * (
                (geometry.pose.position.x - com.x) ** 2
                + (geometry.pose.position.z - com.z) ** 2
            )
            translation[2, 2] += geometry.mass * (
                (geometry.pose.position.x - com.x) ** 2
                + (geometry.pose.position.y - com.y) ** 2
            )

            ori_as_mat = self._quaternion_to_rotation_matrix(
                geometry.pose.orientation
            )
            global_inertia = (
                ori_as_mat * local_inertia * ori_as_mat.transpose()
                + translation
            )
            inertia += global_inertia
        return inertia

    @staticmethod
    def _calculate_box_inertia(geometry: GeometryBox) -> Matrix33:
        """Calculate the moment of inertia for a box geometry.

        :param geometry: The geometry.
        :type geometry: GeometryBox
        :returns: The local inertia.
        :rtype: Matrix33
        """
        # calculate inertia in local coordinates
        local_inertia = Matrix33()
        local_inertia[0, 0] += (
            geometry.mass
            * (geometry.aabb.size.y**2 + geometry.aabb.size.z**2)
            / 12.0
        )
        local_inertia[1, 1] += (
            geometry.mass
            * (geometry.aabb.size.x**2 + geometry.aabb.size.z**2)
            / 12.0
        )
        local_inertia[2, 2] += (
            geometry.mass
            * (geometry.aabb.size.x**2 + geometry.aabb.size.y**2)
            / 12.0
        )
        return local_inertia

    @staticmethod
    def _calculate_sphere_inertia(geometry: GeometrySphere) -> Matrix33:
        """Calculate the moment of inertia for a sphere geometry.

        :param geometry: The geometry.
        :type geometry: GeometrySphere
        :returns: The local inertia.
        :rtype: Matrix33
        """
        # calculate inertia in local coordinates
        local_inertia = Matrix33()
        local_inertia[0, 0] += 2 * geometry.mass * (geometry.radius**2) / 5
        local_inertia[1, 1] += 2 * geometry.mass * (geometry.radius**2) / 5
        local_inertia[2, 2] += 2 * geometry.mass * (geometry.radius**2) / 5
        return local_inertia

    @staticmethod
    def _quaternion_to_rotation_matrix(quat: Quaternion) -> Matrix33:
        """:param quat:
        :type quat: Quaternion
        :rtype: Matrix33
        """
        # https://automaticaddison.com/how-to-convert-a-quaternion-to-a-rotation-matrix/

        q0, q1, q2, q3 = quat

        # First row of the rotation matrix
        r00 = 2 * (q0 * q0 + q1 * q1) - 1
        r01 = 2 * (q1 * q2 - q0 * q3)
        r02 = 2 * (q1 * q3 + q0 * q2)

        # Second row of the rotation matrix
        r10 = 2 * (q1 * q2 + q0 * q3)
        r11 = 2 * (q0 * q0 + q2 * q2) - 1
        r12 = 2 * (q2 * q3 - q0 * q1)

        # Third row of the rotation matrix
        r20 = 2 * (q1 * q3 - q0 * q2)
        r21 = 2 * (q2 * q3 + q0 * q1)
        r22 = 2 * (q0 * q0 + q3 * q3) - 1

        return Matrix33([[r00, r01, r02], [r10, r11, r12], [r20, r21, r22]])
