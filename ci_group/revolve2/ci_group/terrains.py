"""Standard terrains."""

import math

import numpy as np
import numpy.typing as npt
from noise import pnoise2
from pyrr import Vector3
from revolve2.modular_robot_simulation import Terrain
from revolve2.simulation.scene import Color, Pose
from revolve2.simulation.scene.geometry import GeometryHeightmap, GeometryPlane
from revolve2.simulation.scene.geometry.textures import MapType
from revolve2.simulation.scene.vector2 import Vector2
from revolve2.simulators.mujoco_simulator.textures import Checker


def flat(size: Vector2 = Vector2([20.0, 20.0])) -> Terrain:
    """Create a flat plane terrain.

    :param size: Size of the plane. (Default value = None)
    :type size: Vector2
    :returns: The created terrain.
    :rtype: Terrain

    """
    return Terrain(
        static_geometry=[
            GeometryPlane(
                pose=Pose(),
                mass=0.0,
                size=size,
                texture=Checker(
                    primary_color=Color(25, 51, 76, 255),
                    secondary_color=Color(51, 76, 102, 255),
                    map_type=MapType.MAP2D,
                ),
            ),
        ]
    )


def crater(
    size: tuple[float, float],
    ruggedness: float,
    curviness: float,
    granularity_multiplier: float = 1.0,
) -> Terrain:
    r"""Create a crater-like terrain with rugged floor using a heightmap.

    It will look like::

        |            |
         \_        .'
           '.,^_..'

    A combination of the rugged and bowl heightmaps.

    :param size: Size of the crater.
    :type size: tuple[float, float]
    :param ruggedness: How coarse the ground is.
    :type ruggedness: float
    :param curviness: Height of the edges of the crater.
    :type curviness: float
    :param granularity_multiplier: Multiplier for how many edges are
        used in the heightmap. (Default value = 1.0)
    :type granularity_multiplier: float
    :returns: The created terrain.
    :rtype: Terrain

    """
    # arbitrary constant to get a nice number of edges
    num_edges_int = 100

    num_edges = (
        int(num_edges_int * size[0] * granularity_multiplier),
        int(num_edges_int * size[1] * granularity_multiplier),
    )

    rugged = rugged_heightmap(
        size=size,
        num_edges=num_edges,
        density=1.5,
    )
    bowl = bowl_heightmap(num_edges=num_edges)

    max_height = ruggedness + curviness
    if max_height == 0.0:
        heightmap = np.zeros(num_edges)
        max_height = 1.0
    else:
        heightmap = (ruggedness * rugged + curviness * bowl) / (
            ruggedness + curviness
        )

    return Terrain(
        static_geometry=[
            GeometryHeightmap(
                pose=Pose(),
                mass=0.0,
                size=Vector3([size[0], size[1], max_height]),
                base_thickness=0.1 + ruggedness,
                heights=heightmap,
            )
        ]
    )


def rugged_heightmap(
    size: tuple[float, float],
    num_edges: tuple[int, int],
    density: float = 1.0,
) -> npt.NDArray[np.float64]:
    r"""Create a rugged terrain heightmap.

    It will look like::

        ..^.__,^._.-.

    Be aware: the maximum height of the heightmap is not actually 1.
    It is around [-1,1] but not exactly.

    :param size: Size of the heightmap.
    :type size: tuple[float, float]
    :param num_edges: How many edges to use for the heightmap.
    :type num_edges: tuple[int, int]
    :param density: How coarse the ruggedness is. (Default value = 1.0)
    :type density: float
    :returns: The created heightmap as a 2 dimensional array.
    :rtype: npt.NDArray[np.float64]

    """
    octave = 10
    c1 = 4.0  # arbitrary constant to get nice noise

    return np.fromfunction(
        np.vectorize(
            lambda y, x: pnoise2(
                x / num_edges[0] * c1 * size[0] * density,
                y / num_edges[1] * c1 * size[1] * density,
                octave,
            ),
            otypes=[float],
        ),
        num_edges,
        dtype=float,
    )


def bowl_heightmap(
    num_edges: tuple[int, int],
) -> npt.NDArray[np.float64]:
    r"""Create a terrain heightmap in the shape of a bowl.

    It will look like::

        |         |
         \       /
          '.___.'

    The height of the edges of the bowl is 1.0 and the center is 0.0.

    :param num_edges: How many edges to use for the heightmap.
    :type num_edges: tuple[int, int]
    :returns: The created heightmap as a 2 dimensional array.
    :rtype: npt.NDArray[np.float64]

    """
    return np.fromfunction(
        np.vectorize(
            lambda y, x: (
                (x / num_edges[0] * 2.0 - 1.0) ** 2
                + (y / num_edges[1] * 2.0 - 1.0) ** 2
                if math.sqrt(
                    (x / num_edges[0] * 2.0 - 1.0) ** 2
                    + (y / num_edges[1] * 2.0 - 1.0) ** 2
                )
                <= 1.0
                else 0.0
            ),
            otypes=[float],
        ),
        num_edges,
        dtype=float,
    )
