"""Standard modular robots."""

import numpy as np
from revolve2.modular_robot.body.v2 import ActiveHingeV2, BodyV2, BrickV2


def all() -> list[BodyV2]:
    """Get a list of all standard module robots.

    :returns: The list of robots.

    :rtype: list[BodyV2]

    """
    return [gecko_v2(), ant_v2(), spider_v2(), snake_v2()]


def get(name: str) -> BodyV2:
    """Get a robot by name.

    :param name: The name of the robot to get.
    :type name: str
    :returns: The robot with that name.
    :rtype: BodyV2
    :raises ValueError: When a robot with that name does not exist.

    """
    match name:
        case "gecko":
            return gecko_v2()
        case "spider":
            return spider_v2()
        case "snake":
            return snake_v2()
        case "ant":
            return ant_v2()
        case "gecko_plus":
            return gecko_plus_v2()
        case "runner":
            return runner_v2()
        case _:
            msg = f"Robot does not exist: {name}"
            raise ValueError(msg)


def runner_v2() -> BodyV2:
    """Sample robot with new HW config.

    :returns: the robot

    :rtype: BodyV2

    """
    body = BodyV2()

    degs_90 = np.pi / 2.0
    body.core_v2.back_face.bottom = BrickV2(degs_90)

    body.core_v2.front_face.bottom = BrickV2(degs_90)
    body.core_v2.front_face.bottom.front = ActiveHingeV2(degs_90)
    body.core_v2.front_face.bottom.front.attachment = BrickV2(degs_90)

    body.core_v2.right_face.bottom = BrickV2(degs_90)
    body.core_v2.right_face.bottom.right = ActiveHingeV2(0.0)
    body.core_v2.right_face.bottom.right.attachment = ActiveHingeV2(0.0)
    body.core_v2.right_face.bottom.right.attachment.attachment = BrickV2(
        degs_90
    )
    body.core_v2.right_face.bottom.right.attachment.attachment.front = BrickV2(
        0.0
    )

    body.core_v2.left_face.bottom = BrickV2(0.0)
    body.core_v2.left_face.bottom.front = BrickV2(degs_90)
    body.core_v2.left_face.bottom.front.right = ActiveHingeV2(0.0)
    body.core_v2.left_face.bottom.front.right.attachment = BrickV2(0.0)
    body.core_v2.left_face.bottom.front.right.attachment.front = ActiveHingeV2(
        0.0
    )
    body.core_v2.left_face.bottom.front.right.attachment.front.attachment = (
        BrickV2(0.0)
    )

    return body


def gecko_v2() -> BodyV2:
    """Sample robot with new HW config.

    :returns: the robot

    :rtype: BodyV2

    """
    body = BodyV2()

    body.core_v2.right_face.bottom = ActiveHingeV2(0.0)
    body.core_v2.right_face.bottom.attachment = BrickV2(0.0)

    body.core_v2.left_face.bottom = ActiveHingeV2(0.0)
    body.core_v2.left_face.bottom.attachment = BrickV2(0.0)

    body.core_v2.back_face.bottom = ActiveHingeV2(np.pi / 2.0)
    body.core_v2.back_face.bottom.attachment = BrickV2(-np.pi / 2.0)
    body.core_v2.back_face.bottom.attachment.front = ActiveHingeV2(np.pi / 2.0)
    body.core_v2.back_face.bottom.attachment.front.attachment = BrickV2(
        -np.pi / 2.0
    )
    body.core_v2.back_face.bottom.attachment.front.attachment.left = (
        ActiveHingeV2(0.0)
    )
    body.core_v2.back_face.bottom.attachment.front.attachment.right = (
        ActiveHingeV2(0.0)
    )
    body.core_v2.back_face.bottom.attachment.front.attachment.left.attachment = BrickV2(
        0.0
    )
    body.core_v2.back_face.bottom.attachment.front.attachment.right.attachment = BrickV2(
        0.0
    )

    return body


def gecko_plus_v2() -> BodyV2:
    """Sample robot with new HW config.

    :returns: the robot

    :rtype: BodyV2

    """
    body = BodyV2()

    body.core_v2.right_face.bottom = ActiveHingeV2(0.0)
    body.core_v2.right_face.bottom.attachment = ActiveHingeV2(0.0)
    body.core_v2.right_face.bottom.attachment.attachment = BrickV2(0.0)

    body.core_v2.left_face.bottom = ActiveHingeV2(0.0)
    body.core_v2.left_face.bottom.attachment = ActiveHingeV2(0.0)
    body.core_v2.left_face.bottom.attachment.attachment = BrickV2(0.0)

    body.core_v2.back_face.bottom = ActiveHingeV2(np.pi / 2.0)
    body.core_v2.back_face.bottom.attachment = BrickV2(-np.pi / 2.0)
    body.core_v2.back_face.bottom.attachment.front = ActiveHingeV2(np.pi / 2.0)
    body.core_v2.back_face.bottom.attachment.front.attachment = BrickV2(
        -np.pi / 2.0
    )
    body.core_v2.back_face.bottom.attachment.front.attachment.left = (
        ActiveHingeV2(0.0)
    )
    body.core_v2.back_face.bottom.attachment.front.attachment.right = (
        ActiveHingeV2(0.0)
    )

    body.core_v2.back_face.bottom.attachment.front.attachment.left.attachment = ActiveHingeV2(
        0.0
    )
    body.core_v2.back_face.bottom.attachment.front.attachment.left.attachment.attachment = BrickV2(
        0.0
    )

    body.core_v2.back_face.bottom.attachment.front.attachment.right.attachment = ActiveHingeV2(
        0.0
    )
    body.core_v2.back_face.bottom.attachment.front.attachment.right.attachment.attachment = BrickV2(
        0.0
    )

    return body


def spider_v2() -> BodyV2:
    """Get the spider modular robot.

    :returns: the robot.

    :rtype: BodyV2

    """
    body = BodyV2()

    body.core_v2.left_face.bottom = ActiveHingeV2(np.pi / 2.0)
    body.core_v2.left_face.bottom.attachment = BrickV2(-np.pi / 2.0)
    body.core_v2.left_face.bottom.attachment.front = ActiveHingeV2(0.0)
    body.core_v2.left_face.bottom.attachment.front.attachment = BrickV2(0.0)

    body.core_v2.right_face.bottom = ActiveHingeV2(np.pi / 2.0)
    body.core_v2.right_face.bottom.attachment = BrickV2(-np.pi / 2.0)
    body.core_v2.right_face.bottom.attachment.front = ActiveHingeV2(0.0)
    body.core_v2.right_face.bottom.attachment.front.attachment = BrickV2(0.0)

    body.core_v2.front_face.bottom = ActiveHingeV2(np.pi / 2.0)
    body.core_v2.front_face.bottom.attachment = BrickV2(-np.pi / 2.0)
    body.core_v2.front_face.bottom.attachment.front = ActiveHingeV2(0.0)
    body.core_v2.front_face.bottom.attachment.front.attachment = BrickV2(0.0)

    body.core_v2.back_face.bottom = ActiveHingeV2(np.pi / 2.0)
    body.core_v2.back_face.bottom.attachment = BrickV2(-np.pi / 2.0)
    body.core_v2.back_face.bottom.attachment.front = ActiveHingeV2(0.0)
    body.core_v2.back_face.bottom.attachment.front.attachment = BrickV2(0.0)

    return body


def ant_v2() -> BodyV2:
    """Get the ant modular robot.

    :returns: the robot.

    :rtype: BodyV2

    """
    body = BodyV2()

    body.core_v2.left_face.bottom = ActiveHingeV2(0.0)
    body.core_v2.left_face.bottom.attachment = BrickV2(0.0)

    body.core_v2.right_face.bottom = ActiveHingeV2(0.0)
    body.core_v2.right_face.bottom.attachment = BrickV2(0.0)

    body.core_v2.back_face.bottom = ActiveHingeV2(np.pi / 2.0)
    body.core_v2.back_face.bottom.attachment = BrickV2(-np.pi / 2.0)
    body.core_v2.back_face.bottom.attachment.left = ActiveHingeV2(0.0)
    body.core_v2.back_face.bottom.attachment.left.attachment = BrickV2(0.0)
    body.core_v2.back_face.bottom.attachment.right = ActiveHingeV2(0.0)
    body.core_v2.back_face.bottom.attachment.right.attachment = BrickV2(0.0)

    body.core_v2.back_face.bottom.attachment.front = ActiveHingeV2(np.pi / 2.0)
    body.core_v2.back_face.bottom.attachment.front.attachment = BrickV2(
        -np.pi / 2.0
    )
    body.core_v2.back_face.bottom.attachment.front.attachment.left = (
        ActiveHingeV2(0.0)
    )
    body.core_v2.back_face.bottom.attachment.front.attachment.left.attachment = BrickV2(
        0.0
    )
    body.core_v2.back_face.bottom.attachment.front.attachment.right = (
        ActiveHingeV2(0.0)
    )
    body.core_v2.back_face.bottom.attachment.front.attachment.right.attachment = BrickV2(
        0.0
    )

    return body


def snake_v2() -> BodyV2:
    """Get the snake modular robot.

    :returns: the robot.

    :rtype: BodyV2

    """
    body = BodyV2()

    body.core_v2.left_face.bottom = ActiveHingeV2(0.0)
    body.core_v2.left_face.bottom.attachment = BrickV2(0.0)
    body.core_v2.left_face.bottom.attachment.front = ActiveHingeV2(np.pi / 2.0)
    body.core_v2.left_face.bottom.attachment.front.attachment = BrickV2(
        -np.pi / 2.0
    )
    body.core_v2.left_face.bottom.attachment.front.attachment.front = (
        ActiveHingeV2(0.0)
    )
    body.core_v2.left_face.bottom.attachment.front.attachment.front.attachment = BrickV2(
        0.0
    )
    body.core_v2.left_face.bottom.attachment.front.attachment.front.attachment.front = ActiveHingeV2(
        np.pi / 2.0
    )
    body.core_v2.left_face.bottom.attachment.front.attachment.front.attachment.front.attachment = BrickV2(
        -np.pi / 2.0
    )
    body.core_v2.left_face.bottom.attachment.front.attachment.front.attachment.front.attachment.front = ActiveHingeV2(
        0.0
    )
    body.core_v2.left_face.bottom.attachment.front.attachment.front.attachment.front.attachment.front.attachment = BrickV2(
        0.0
    )
    body.core_v2.left_face.bottom.attachment.front.attachment.front.attachment.front.attachment.front.attachment.front = ActiveHingeV2(
        np.pi / 2.0
    )
    body.core_v2.left_face.bottom.attachment.front.attachment.front.attachment.front.attachment.front.attachment.front.attachment = BrickV2(
        -np.pi / 2.0
    )
    body.core_v2.left_face.bottom.attachment.front.attachment.front.attachment.front.attachment.front.attachment.front.attachment.front = ActiveHingeV2(
        0.0
    )
    body.core_v2.left_face.bottom.attachment.front.attachment.front.attachment.front.attachment.front.attachment.front.attachment.front.attachment = BrickV2(
        0.0
    )
    body.core_v2.left_face.bottom.attachment.front.attachment.front.attachment.front.attachment.front.attachment.front.attachment.front.attachment.front = ActiveHingeV2(
        np.pi / 2.0
    )

    return body
