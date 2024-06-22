"""Abstract Base Modules for Robots."""

from modular_robot.body.base._active_hinge import ActiveHinge
from modular_robot.body.base._attachment_face import AttachmentFace
from modular_robot.body.base._body import Body
from modular_robot.body.base._brick import Brick
from modular_robot.body.base._core import Core

__all__ = [
    "ActiveHinge",
    "AttachmentFace",
    "Body",
    "Brick",
    "Core",
]
