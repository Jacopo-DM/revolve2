"""Draw 2D representations of Modular Robots.

Based on Karine Miras` Method.
"""

import logging
import time
from pathlib import Path
from typing import TYPE_CHECKING, Any

import cairo
import numpy as np
from numpy.typing import NDArray
from revolve2.modular_robot import ModularRobot
from revolve2.modular_robot.body import Module
from revolve2.modular_robot.body.base import ActiveHinge, Body, Brick, Core

if TYPE_CHECKING:
    from pyrr import Vector3


def __mk_path() -> str:
    path = f"planar_robot_representations_{time.time()}"
    logging.info("Saving images to: %s", path)
    file_path = Path(path)
    if not file_path.exists():
        Path.mkdir(file_path)
    return path


def draw_robots(
    robots: list[ModularRobot] | list[Body],
    scale: int = 100,
    path: str | None = None,
) -> None:
    """Draw multiple robots at once.

    How to use:

    :param robots: The robots.
    :type robots: list[ModularRobot] | list[Body]
    :param scale: The scale for the robots to be drawn. (Default value =
        100)
    :type scale: int
    :param path: The path for the output files. (Default value = None)
    :type path: str | None
    :rtype: None

    >>> robots: (
    ...     list[revolve2.modular_robot.ModularRobot]
    ...     | list[revolve2.modular_robot.body.base.Body]
    ... )
    >>> draw_robots(robots, path="<your desired path to save the image to>")
    """
    if not path:
        path = __mk_path()

    for robot in robots:
        draw_robot(robot, scale, path)


def draw_robot(
    robot: ModularRobot | Body, scale: int = 100, path: str | None = None
) -> None:
    """Draw a 2D representation for a modular robots body.

    How to use:

    :param robot: Supply the robot as a ModularRobot object, or the body
        directly as a Body object.
    :type robot: ModularRobot | Body
    :param scale: Allows to set the size of the drawing. (Default value
        = 100)
    :type scale: int
    :param path: The path to save images to. (Default value = None)
    :type path: str | None
    :rtype: None

    >>> robot: (
    ...     revolve2.modular_robot.ModularRobot | revolve2.modular_robot.body.base.Body
    ... )
    >>> draw_robot(robot, path="<your desired path to save the image to>")
    """
    if not path:
        path = __mk_path()

    body = robot if isinstance(robot, Body) else robot.body
    tpl: tuple[NDArray[Any], Vector3[np.int_]] = body.to_grid()
    body_grid, core_position = tpl
    x, y, _ = body_grid.shape

    image = cairo.ImageSurface(cairo.FORMAT_ARGB32, x * scale, y * scale)
    context = cairo.Context(image)
    context.scale(scale, scale)

    cx, cy, _ = tuple(core_position)
    _draw_module(
        module=body.core,
        position=(cx, cy),
        previous_position=(cx, cy),
        orientation=_make_rot_mat(0),
        context=context,
    )
    _save_png(image, path)


def _draw_module(
    module: Module,
    position: tuple[int, int],
    previous_position: tuple[int, int],
    orientation: NDArray[np.int_],
    context: "cairo.Context[cairo.ImageSurface]",
    *,
    print_id: bool = False,
) -> None:
    """Draw a module onto the canvas.

    :param module: The module.
    :type module: Module
    :param position: The position on the canvas.
    :type position: tuple[int, int]
    :param previous_position: The position of the previous module.
    :type previous_position: tuple[int, int]
    :param orientation: The orientation to draw in.
    :type orientation: NDArray[np.int_]
    :param context: The context to draw it on.
    :type context: "cairo.Context[cairo.ImageSurface]"
    :param print_id: If the modules id should be drawn as well. (Default
        value = False)
    :type print_id: bool
    :param :
    :rtype: None
    :raises Exception: If the module cant be drawn.
    """
    x, y = position
    context.rectangle(x, y, 1, 1)  # draw module object

    match module:
        case Core():
            context.set_source_rgb(255, 255, 0)  # Yellow
        case ActiveHinge():
            context.set_source_rgb(red=255, green=0, blue=0)  # Red
            if np.isclose(module.orientation.angle, 0.0):
                context.set_source_rgb(1.0, 0.4, 0.4)  # Flesh Color
        case Brick():
            context.set_source_rgb(0, 0, 255)  # Blue
        case _:
            msg = f"Module of type {type(module)} has no defined structure for drawing."
            raise ValueError(msg)

    # default operation for every module
    context.fill_preserve()
    context.set_line_width(0.01)
    context.stroke()
    context.set_source_rgb(0, 0, 0)

    if module.parent is not None:
        # draw the connection to the parent module
        x_offset, y_offset = (
            previous_position[0] - position[0],
            previous_position[1] - position[1],
        )

        circ_x = (
            x + 0.5
            if x_offset == 0
            else x + (x_offset if x_offset > 0 else abs(x_offset) - 1)
        )
        circ_y = (
            y + 0.5
            if y_offset == 0
            else y + (y_offset if y_offset > 0 else abs(y_offset) - 1)
        )

        context.arc(circ_x, circ_y, 0.1, 0, np.pi * 2)
        context.fill_preserve()
        context.stroke()

    if print_id:
        # print module id onto canvas
        context.set_font_size(0.3)
        context.move_to(x, y + 0.4)
        context.show_text(str(module.uuid))
        context.stroke()

    for key, child in module.children.items():
        angle = module.attachment_points[key].orientation.angle
        mapo = _make_rot_mat(angle)
        target_orientation = orientation @ mapo

        x, y = target_orientation.dot(np.array([1, 0]))

        new_pos = position[0] + x, position[1] + y
        _draw_module(
            module=child,
            position=new_pos,
            previous_position=position,
            context=context,
            orientation=target_orientation,
        )


def _make_rot_mat(theta: float) -> NDArray[np.int_]:
    """Make a rotation matrix from angle in 2D.

    This function casts angles to iterations of 90°, since we plot on a
    grid.

    :param theta: The angle.
    :type theta: float
    :returns: The matrix.
    :rtype: NDArray[np.int_]
    """
    c, s = int(round(np.cos(theta))), int(round(np.sin(theta)))
    return np.array(((c, -s), (s, c)))


def _save_png(image: cairo.ImageSurface, path: str) -> None:
    """Save the image representation of a robot as png.

    :param image: The image.
    :type image: cairo.ImageSurface
    :param path: The path to save the image to.
    :type path: str
    :rtype: None
    """
    image.write_to_png(f"{path}/robot_2d_{hash(image)}.png")
