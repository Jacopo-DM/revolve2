import mujoco
import numpy as np
from revolve2.simulation.scene import ControlInterface, JointHinge, UUIDKey

from ._abstraction_to_mujoco_mapping import (
    AbstractionToMujocoMapping,
)


class ControlInterfaceImpl(ControlInterface):
    """Implementation of the control interface for MuJoCo."""

    _data: mujoco.MjData
    _abstraction_to_mujoco_mapping: AbstractionToMujocoMapping

    def __init__(
        self,
        data: mujoco.MjData,
        abstraction_to_mujoco_mapping: AbstractionToMujocoMapping,
    ) -> None:
        """Initialize this object.

        :param data: The MuJoCo data to alter during control.
        :param abstraction_to_mujoco_mapping: A mapping between
            simulation abstraction and mujoco.
        """
        self._data = data
        self._abstraction_to_mujoco_mapping = abstraction_to_mujoco_mapping

    def set_joint_hinge_position_target(
        self,
        joint_hinge: JointHinge,
        update: float,
        *,
        as_delta: bool = True,
    ) -> None:
        """Set the position target of a hinge joint.

        :param joint_hinge: The hinge to set the position target for.
        :type joint_hinge: JointHinge
        :param position_delta:
        :type position_delta: float
        :rtype: None
        """
        maybe_hinge_joint_mujoco = (
            self._abstraction_to_mujoco_mapping.hinge_joint.get(
                UUIDKey(joint_hinge)
            )
        )
        assert (
            maybe_hinge_joint_mujoco is not None
        ), "Hinge joint does not exist in this scene."

        # Set position target
        idx_pos = maybe_hinge_joint_mujoco.ctrl_index_position

        # TODO(jmdm) should be position be added (+=) or set (=) ?
        ctrl_data = self._data.ctrl[idx_pos] + update if as_delta else update

        self._data.ctrl[idx_pos] = np.clip(
            ctrl_data,
            -joint_hinge.range,
            joint_hinge.range,
        )

        # Set velocity target
        idx_vel = maybe_hinge_joint_mujoco.ctrl_index_velocity
        self._data.ctrl[idx_vel] = 0.0
