import uuid
import warnings

import defusedxml
import scipy.spatial.transform
from defusedxml import ElementTree as xmlTree
from pyrr import Quaternion, Vector3

from simulation.scene import JointHinge, MultiBodySystem, Pose, RigidBody
from simulation.scene.geometry import (
    Geometry,
    GeometryBox,
    GeometryHeightmap,
    GeometryPlane,
    GeometrySphere,
)


def multi_body_system_to_urdf(
    multi_body_system: MultiBodySystem, name: str
) -> tuple[
    str,
    list[GeometryPlane],
    list[GeometryHeightmap],
    list[tuple[JointHinge, str]],
    list[tuple[Geometry, str]],
    list[tuple[RigidBody, str]],
]:
    """
    Convert a multi-body system to URDF.

    It must be acyclic and the root body must also be the tree root.
    Furthermore, for each joint, the first body will be considered the parent, and as such must be the parent in the tree.

    Plane and heightmap cannot be represented in URDF and will be returned as in lists.
    It is checked they only exist as part of the root rigid body and for static multi-body systems.

    :param multi_body_system: The multi-body system to convert.
    :param name: The name to using in the URDF. It will be a prefix for every name in the model.
    :returns: A urdf string, plane geometries, heightmap geometries, joints and their names in the urdf, geometries and their names in the urdf, rigid bodies and their names in the urdf.
    :raises ValueError: In case the graph is cyclic.

    # noqa: DAR402 ValueError
    """
    return _URDFConverter().build(multi_body_system, name)


class _URDFConverter:
    base_name: str
    multi_body_system: MultiBodySystem
    visited_rigid_bodies: set[uuid.UUID]  # their indices
    joints_and_names: list[tuple[JointHinge, str]]
    geometries_and_names: list[tuple[Geometry, str]]
    rigid_bodies_and_names: list[tuple[RigidBody, str]]
    planes: list[GeometryPlane]
    heightmaps: list[GeometryHeightmap]

    def build(
        self, multi_body_system: MultiBodySystem, name: str
    ) -> tuple[
        str,
        list[GeometryPlane],
        list[GeometryHeightmap],
        list[tuple[JointHinge, str]],
        list[tuple[Geometry, str]],
        list[tuple[RigidBody, str]],
    ]:
        if not multi_body_system.has_root():
            msg = "Multi-body system has no root."
            raise ValueError(msg)

        self.multi_body_system = multi_body_system
        self.visited_rigid_bodies = set()
        self.joints_and_names = []
        self.geometries_and_names = []
        self.rigid_bodies_and_names = []
        self.planes = []
        self.heightmaps = []

        urdf = xmlTree.Element("robot", {"name": name})

        for element in self._make_links_xml_elements(
            multi_body_system.root,
            multi_body_system.root.initial_pose,
            f"{name}",
            parent_rigid_body=None,
        ):
            urdf.append(element)

        return (
            defusedxml.minidom.parseString(
                defusedxml.xmlTree.tostring(
                    urdf, encoding="unicode", method="xml"
                )
            ).toprettyxml(indent="    "),
            self.planes,
            self.heightmaps,
            self.joints_and_names,
            self.geometries_and_names,
            self.rigid_bodies_and_names,
        )

    def _make_links_xml_elements(
        self,
        rigid_body: RigidBody,
        link_pose: Pose,
        rigid_body_name: str,
        parent_rigid_body: RigidBody | None,
    ) -> list[xmlTree.Element]:
        if rigid_body.uuid in self.visited_rigid_bodies:
            msg = "Multi-body system is cyclic."
            raise ValueError(msg)
        self.visited_rigid_bodies.add(rigid_body.uuid)

        link = xmlTree.Element("link", {"name": rigid_body_name})
        elements = [link]
        self.rigid_bodies_and_names.append((rigid_body, rigid_body_name))

        com_xyz = link_pose.orientation.inverse * (
            rigid_body.initial_pose.position
            - link_pose.position
            + rigid_body.initial_pose.orientation * rigid_body.center_of_mass()
        )
        com_rpy = _quaternion_to_euler(
            link_pose.orientation.inverse * rigid_body.initial_pose.orientation
        )
        if rigid_body.mass() != 0.0:
            inertia = rigid_body.inertia_tensor()

            inertial = xmlTree.SubElement(link, "inertial")
            xmlTree.SubElement(
                inertial,
                "origin",
                {
                    "rpy": f"{com_rpy[0]} {com_rpy[1]} {com_rpy[2]}",
                    "xyz": f"{com_xyz[0]} {com_xyz[1]} {com_xyz[2]}",
                },
            )
            xmlTree.SubElement(
                inertial, "mass", {"value": f"{rigid_body.mass():e}"}
            )
            xmlTree.SubElement(
                inertial,
                "inertia",
                {
                    "ixx": f"{inertia[0][0]:e}",
                    "ixy": f"{inertia[0][1]:e}",
                    "ixz": f"{inertia[0][2]:e}",
                    "iyy": f"{inertia[1][1]:e}",
                    "iyz": f"{inertia[1][2]:e}",
                    "izz": f"{inertia[2][2]:e}",
                },
            )

        for geometry_index, geometry in enumerate(rigid_body.geometries):
            name = f"{rigid_body_name}_geom{geometry_index}"

            match geometry:
                case GeometryBox():
                    self.geometries_and_names.append((geometry, name))
                    self._add_geometry_box(
                        link=link,
                        name=name,
                        geometry=geometry,
                        link_pose=link_pose,
                        rigid_body=rigid_body,
                    )
                case GeometryPlane():
                    if parent_rigid_body is not None:
                        msg = "Plane geometry can only be included in the root rigid body."
                        raise ValueError(msg)
                    if not self.multi_body_system.is_static:
                        msg = "Plane geometry can only be included in static multi-body systems."
                        raise ValueError(msg)
                    self.planes.append(geometry)
                case GeometryHeightmap():
                    if parent_rigid_body is not None:
                        msg = "Heightmap geometry can only be included in the root rigid body."
                        raise ValueError(msg)
                    if not self.multi_body_system.is_static:
                        msg = "Heightmap geometry can only be included in static multi-body systems."
                        raise ValueError(msg)
                    self.heightmaps.append(geometry)
                case GeometrySphere():
                    self.geometries_and_names.append((geometry, name))
                    self._add_geometry_sphere(
                        link=link,
                        name=name,
                        geometry=geometry,
                        link_pose=link_pose,
                        rigid_body=rigid_body,
                    )
                case _:
                    msg = "Geometry not yet supported."
                    raise ValueError(msg)

        for joint_index, joint in enumerate(
            self.multi_body_system.get_joints_for_rigid_body(rigid_body)
        ):
            # Make sure we don't go back up the joint we came from.
            if parent_rigid_body is not None and (
                parent_rigid_body.uuid
                in {joint.rigid_body1.uuid, joint.rigid_body2.uuid}
            ):
                continue

            if not isinstance(joint, JointHinge):
                msg = "Joints other that hinge joints are not yet supported."
                raise TypeError(msg)

            child_name = f"{rigid_body_name}_link{joint_index}"

            joint_name = f"{rigid_body_name}_joint{joint_index}"
            self.joints_and_names.append((joint, joint_name))
            el = xmlTree.Element("joint", type="revolute", name=joint_name)
            xmlTree.SubElement(
                el,
                "parent",
                {
                    "link": (
                        rigid_body_name
                        if joint.rigid_body1.uuid == rigid_body.uuid
                        else child_name
                    )
                },
            )
            xmlTree.SubElement(
                el,
                "child",
                {
                    "link": (
                        rigid_body_name
                        if joint.rigid_body1.uuid != rigid_body.uuid
                        else child_name
                    )
                },
            )
            xyz = link_pose.orientation.inverse * (
                joint.pose.position - link_pose.position
            )
            rpy = _quaternion_to_euler(
                link_pose.orientation.inverse * joint.pose.orientation
            )
            xmlTree.SubElement(
                el,
                "origin",
                {
                    "rpy": f"{rpy[0]} {rpy[1]} {rpy[2]}",
                    "xyz": f"{xyz[0]} {xyz[1]} {xyz[2]}",
                },
            )
            xmlTree.SubElement(el, "axis", {"xyz": "0 1 0"})
            xmlTree.SubElement(
                el,
                "limit",
                {
                    "lower": f"{-joint.range}",
                    "upper": f"{joint.range}",
                    "effort": f"{joint.effort}",
                    "velocity": f"{joint.velocity}",
                },
            )
            elements.append(el)
            elements += self._make_links_xml_elements(
                joint.rigid_body2,
                joint.pose,
                child_name,
                parent_rigid_body=rigid_body,
            )

        return elements

    @staticmethod
    def _add_geometry_box(
        link: xmlTree.Element,
        name: str,
        geometry: GeometryBox,
        link_pose: Pose,
        rigid_body: RigidBody,
    ) -> None:
        el = xmlTree.SubElement(link, "collision", {"name": name})
        geometry_xml = xmlTree.SubElement(el, "geometry")
        xmlTree.SubElement(
            geometry_xml,
            "box",
            {
                "size": f"{geometry.aabb.size.x} {geometry.aabb.size.y} {geometry.aabb.size.z}"
            },
        )
        xyz = link_pose.orientation.inverse * (
            rigid_body.initial_pose.position
            - link_pose.position
            + rigid_body.initial_pose.orientation * geometry.pose.position
        )
        rpy = _quaternion_to_euler(
            link_pose.orientation.inverse
            * rigid_body.initial_pose.orientation
            * geometry.pose.orientation
        )
        xmlTree.SubElement(
            el,
            "origin",
            {
                "rpy": f"{rpy[0]} {rpy[1]} {rpy[2]}",
                "xyz": f"{xyz[0]} {xyz[1]} {xyz[2]}",
            },
        )

    @staticmethod
    def _add_geometry_sphere(
        link: xmlTree.Element,
        name: str,
        geometry: GeometrySphere,
        link_pose: Pose,
        rigid_body: RigidBody,
    ) -> None:
        el = xmlTree.SubElement(link, "collision", {"name": name})
        geometry_xml = xmlTree.SubElement(el, "geometry")
        xmlTree.SubElement(
            geometry_xml,
            "sphere",
            {"radius": str(geometry.radius)},
        )
        xyz = link_pose.orientation.inverse * (
            rigid_body.initial_pose.position
            - link_pose.position
            + rigid_body.initial_pose.orientation * geometry.pose.position
        )
        rpy = _quaternion_to_euler(
            link_pose.orientation.inverse
            * rigid_body.initial_pose.orientation
            * geometry.pose.orientation
        )
        xmlTree.SubElement(
            el,
            "origin",
            {
                "rpy": f"{rpy[0]} {rpy[1]} {rpy[2]}",
                "xyz": f"{xyz[0]} {xyz[1]} {xyz[2]}",
            },
        )

    @staticmethod
    def _add_geometry_plane(
        link: xmlTree.Element,
        name: str,
        geometry: GeometryPlane,
        link_pose: Pose,
        rigid_body: RigidBody,
    ) -> None:
        _plane_box_height = 0.1

        el = xmlTree.SubElement(link, "collision", {"name": name})
        geometry_xml = xmlTree.SubElement(el, "geometry")
        xmlTree.SubElement(
            geometry_xml,
            "box",
            {
                "size": f"{geometry.size.x} {geometry.size.y} {_plane_box_height}"
            },
        )
        xyz = link_pose.orientation.inverse * (
            rigid_body.initial_pose.position
            - link_pose.position
            + rigid_body.initial_pose.orientation
            * (
                geometry.pose.position
                + Vector3([0.0, 0.0, -_plane_box_height / 2.0])
            )
        )
        rpy = _quaternion_to_euler(
            link_pose.orientation.inverse
            * rigid_body.initial_pose.orientation
            * geometry.pose.orientation
        )
        xmlTree.SubElement(
            el,
            "origin",
            {
                "rpy": f"{rpy[0]} {rpy[1]} {rpy[2]}",
                "xyz": f"{xyz[0]} {xyz[1]} {xyz[2]}",
            },
        )


def _quaternion_to_euler(quaternion: Quaternion) -> Vector3:
    with warnings.catch_warnings():
        # ignore gimbal lock warning. it is irrelevant for us.
        warnings.simplefilter("ignore", UserWarning)
        euler = scipy.spatial.transform.Rotation.from_quat([
            quaternion.x,
            quaternion.y,
            quaternion.z,
            quaternion.w,
        ]).as_euler("xyz")

    return Vector3(euler)
