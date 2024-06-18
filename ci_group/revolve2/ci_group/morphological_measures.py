"""MorphologicalMeasures class."""

from itertools import product
from typing import Generic, TypeVar

import numpy as np
from numpy.typing import NDArray
from pyrr import Vector3
from revolve2.modular_robot.body import Module
from revolve2.modular_robot.body.base import ActiveHinge, Body, Brick, Core

TModule = TypeVar("TModule", bound=np.generic)


class MorphologicalMeasures(Generic[TModule]):
    """
    Modular robot morphological measures.

    Only works for robot with only right angle module rotations (90 degrees).
    Some measures only work for 2d robots, which is noted in their docstring.

    The measures are based on the following paper:
    Miras, K., Haasdijk, E., Glette, K., Eiben, A.E. (2018).
    Search Space Analysis of Evolvable Robot Morphologies.
    In: Sim, K., Kaufmann, P. (eds) Applications of Evolutionary Computation.
    EvoApplications 2018. Lecture Notes in Computer Science(), vol 10784. Springer, Cham.
    https://doi.org/10.1007/978-3-319-77538-8_47
    """

    """Represents the modules of a body in a 3D tensor."""
    grid: NDArray[TModule]
    symmetry_grid: NDArray[TModule]
    """Position of the core in 'body_as_grid'."""
    core_grid_position: Vector3[np.int_]

    """If the robot is two dimensional, i.e. all module rotations are 0 degrees."""
    is_2d: bool

    core: Core
    modules: list[Module]
    bricks: list[Brick]
    active_hinges: list[ActiveHinge]

    """If all slots of the core are filled with other modules."""
    core_is_filled: bool

    """Bricks which have all slots filled with other modules."""
    filled_bricks: list[Brick]

    """Active hinges which have all slots filled with other modules."""
    filled_active_hinges: list[ActiveHinge]

    """
    Modules that only connect to one other module.

    This includes children and parents.
    """
    single_neighbour_modules: list[Module]

    """
    Bricks that are only connected to one other module.

    Both children and parent are counted.
    """
    single_neighbour_bricks: list[Brick]

    """
    Bricks that are connected to exactly two other modules.

    Both children and parent are counted.
    """
    double_neighbour_bricks: list[Brick]

    """
    Active hinges that are connected to exactly two other modules.

    Both children and parent are counted.
    """
    double_neighbour_active_hinges: list[ActiveHinge]

    """
    X/Y-plane symmetry according to the paper but in 3D.

    X-axis is defined as forward/backward for the core module
    Y-axis is defined as left/right for the core module.
    """
    xy_symmetry: float

    """
    X/Z-plane symmetry according to the paper but in 3D.

    X-axis is defined as forward/backward for the core module
    Z-axis is defined as up/down for the core module.
    """
    xz_symmetry: float

    """
    Y/Z-plane symmetry according to the paper but in 3D.

    Y-axis is defined as left/right for the core module.
    Z-axis is defined as up/down for the core module.
    """
    yz_symmetry: float

    def __init__(self, body: Body) -> None:
        """
        Initialize this object.

        :param body: The body to measure.
        """
        self.grid, self.core_grid_position = body.to_grid()
        self.core = body.core
        self.is_2d = self.__calculate_is_2d_recur(self.core)
        self.modules = body.find_modules_of_type(Module, exclude=[Core])
        self.bricks = body.find_modules_of_type(Brick)
        self.active_hinges = body.find_modules_of_type(ActiveHinge)
        self.core_is_filled = self.__calculate_core_is_filled()
        self.filled_bricks = self.__calculate_filled_bricks()
        self.filled_active_hinges = self.__calculate_filled_active_hinges()
        self.single_neighbour_bricks = (
            self.__calculate_single_neighbour_bricks()
        )
        self.single_neighbour_modules = (
            self.__calculate_single_neighbour_modules()
        )
        self.double_neighbour_bricks = (
            self.__calculate_double_neighbour_bricks()
        )
        self.double_neighbour_active_hinges = (
            self.__calculate_double_neighbour_active_hinges()
        )

        self.__pad_grid()
        self.xy_symmetry = self.__calculate_xy_symmetry()
        self.xz_symmetry = self.__calculate_xz_symmetry()
        self.yz_symmetry = self.__calculate_yz_symmetry()

    @classmethod
    def __calculate_is_2d_recur(cls, module: Module) -> bool:
        return all(
            [np.isclose(module.orientation.angle, 0.0)]
            + [
                cls.__calculate_is_2d_recur(child)
                for child in module.children.values()
            ]
        )

    def __calculate_core_is_filled(self) -> bool:
        return all(
            self.core.children.get(child_index) is not None
            for child_index in self.core.attachment_points
        )

    def __calculate_filled_bricks(self) -> list[Brick]:
        return [
            brick
            for brick in self.bricks
            if all(
                brick.children.get(child_index) is not None
                for child_index in brick.attachment_points
            )
        ]

    def __calculate_filled_active_hinges(self) -> list[ActiveHinge]:
        return [
            active_hinge
            for active_hinge in self.active_hinges
            if all(
                active_hinge.children.get(child_index) is not None
                for child_index in active_hinge.attachment_points
            )
        ]

    def __calculate_single_neighbour_bricks(self) -> list[Brick]:
        return [
            brick
            for brick in self.bricks
            if all(
                brick.children.get(child_index) is None
                for child_index in brick.attachment_points
            )
        ]

    def __calculate_single_neighbour_modules(self) -> list[Module]:
        return [
            module
            for module in self.modules
            if all(
                module.children.get(child_index) is None
                for child_index in module.attachment_points
            )
        ]

    def __calculate_double_neighbour_bricks(self) -> list[Brick]:
        return [
            brick
            for brick in self.bricks
            if sum(
                0 if brick.children.get(child_index) is None else 1
                for child_index in brick.attachment_points
            )
            == 1
        ]

    def __calculate_double_neighbour_active_hinges(self) -> list[ActiveHinge]:
        return [
            active_hinge
            for active_hinge in self.active_hinges
            if sum(
                0 if active_hinge.children.get(child_index) is None else 1
                for child_index in active_hinge.attachment_points
            )
            == 1
        ]

    def __pad_grid(self) -> None:
        x, y, z = self.grid.shape
        xoffs, yoffs, zoffs = self.core_grid_position
        self.symmetry_grid = np.empty(
            shape=(x + xoffs, y + yoffs, z + zoffs), dtype=Module
        )
        self.symmetry_grid.fill(None)
        self.symmetry_grid[:x, :y, :z] = self.grid

    def __calculate_xy_symmetry(self) -> float:
        num_along_plane = 0
        num_symmetrical = 0
        for x, y, z in product(
            range(self.bounding_box_depth),
            range(self.bounding_box_width),
            range(1, (self.bounding_box_height - 1) // 2),
        ):
            if self.symmetry_grid[x, y, self.core_grid_position[2]] is not None:
                num_along_plane += 1
            if self.symmetry_grid[
                x, y, self.core_grid_position[2] + z
            ] is not None and isinstance(
                self.symmetry_grid[x, y, self.core_grid_position[2] + z],
                type(self.symmetry_grid[x, y, self.core_grid_position[2] - z]),
            ):
                num_symmetrical += 2

        difference = self.num_modules - num_along_plane
        return num_symmetrical / difference if difference > 0.0 else difference

    def __calculate_xz_symmetry(self) -> float:
        num_along_plane = 0
        num_symmetrical = 0
        for x, y, z in product(
            range(self.bounding_box_depth),
            range(1, (self.bounding_box_width - 1) // 2),
            range(self.bounding_box_height),
        ):
            if self.symmetry_grid[x, self.core_grid_position[1], z] is not None:
                num_along_plane += 1
            if self.symmetry_grid[
                x, self.core_grid_position[1] + y, z
            ] is not None and isinstance(
                self.symmetry_grid[x, self.core_grid_position[1] + y, z],
                type(self.symmetry_grid[x, self.core_grid_position[1] - y, z]),
            ):
                num_symmetrical += 2
        difference = self.num_modules - num_along_plane
        return num_symmetrical / difference if difference > 0.0 else difference

    def __calculate_yz_symmetry(self) -> float:
        num_along_plane = 0
        num_symmetrical = 0
        for x, y, z in product(
            range(1, (self.bounding_box_depth - 1) // 2),
            range(self.bounding_box_width),
            range(self.bounding_box_height),
        ):
            if self.symmetry_grid[self.core_grid_position[0], y, z] is not None:
                num_along_plane += 1
            if self.symmetry_grid[
                self.core_grid_position[0] + x, y, z
            ] is not None and isinstance(
                self.symmetry_grid[self.core_grid_position[0] + x, y, z],
                type(self.symmetry_grid[self.core_grid_position[0] - x, y, z]),
            ):
                num_symmetrical += 2
        difference = self.num_modules - num_along_plane
        return num_symmetrical / difference if difference > 0.0 else difference

    @property
    def bounding_box_depth(self) -> int:
        """
        Get the depth of the bounding box around the body.

        Forward/backward axis for the core module.

        :returns: The depth.
        """
        return self.grid.shape[0]

    @property
    def bounding_box_width(self) -> int:
        """
        Get the width of the bounding box around the body.

        Right/left axis for the core module.

        :returns: The width.
        """
        return self.grid.shape[1]

    @property
    def bounding_box_height(self) -> int:
        """
        Get the height of the bounding box around the body.

        Up/down axis for the core module.

        :returns: The height.
        """
        return self.grid.shape[2]

    @property
    def num_modules(self) -> int:
        """
        Get the number of modules.

        :returns: The number of modules.
        """
        return 1 + len(self.modules)

    @property
    def num_bricks(self) -> int:
        """
        Get the number of bricks.

        :returns: The number of bricks.
        """
        return len(self.bricks)

    @property
    def num_active_hinges(self) -> int:
        """
        Get the number of active hinges.

        :returns: The number of active hinges.
        """
        return len(self.active_hinges)

    @property
    def num_filled_bricks(self) -> int:
        """
        Get the number of bricks which have all slots filled with other modules.

        :returns: The number of bricks.
        """
        return len(self.filled_bricks)

    @property
    def num_filled_active_hinges(self) -> int:
        """
        Get the number of bricks which have all slots filled with other modules.

        :returns: The number of bricks.
        """
        return len(self.filled_active_hinges)

    @property
    def num_filled_modules(self) -> int:
        """
        Get the number of modules which have all slots filled with other modules, including the core.

        :returns: The number of modules.
        """
        return (
            self.num_filled_bricks
            + self.num_active_hinges
            + (1 if self.core_is_filled else 0)
        )

    @property
    def max_potentionally_filled_core_and_bricks(self) -> int:
        """
        Get the maximum number of core and bricks that could potentially be filled with this set of modules if rearranged in an optimal way.

        This calculates 'b_max' from the paper.

        :returns: The calculated number.
        """
        # Snake-like is an optimal arrangement.
        #
        #   H H H H
        #   | | | |
        # H-C-B-B-B-H
        #   | | | |
        #   H H H H
        #
        # Every extra brick(B) requires 3 modules:
        # The bricks itself and two other modules for its sides(here displayed as H).
        # However, the core and final brick require three each to fill, which is cheaper than another brick.
        #
        # Expected sequence:
        # | num modules | 1 2 3 4 5 6 7 8 9 10 11 12 14
        # | return val  | 0 0 0 0 1 1 1 2 2 2  3  3  3

        pot_max_filled = max(0, (self.num_modules - 2) // 3)

        return min(pot_max_filled, 1 + self.num_bricks)

    @property
    def filled_core_and_bricks_proportion(self) -> float:
        """
        Get the ratio between filled cores and bricks and how many that potentially could have been if this set of modules was rearranged in an optimal way.

        This calculates 'branching' from the paper.

        :returns: The proportion.
        """
        if self.max_potentionally_filled_core_and_bricks == 0:
            return 0.0

        return (
            len(self.filled_bricks) + (1 if self.core_is_filled else 0)
        ) / self.max_potentionally_filled_core_and_bricks

    @property
    def num_single_neighbour_modules(self) -> int:
        """
        Get the number of bricks that are only connected to one other module.

        Both children and parent are counted.

        :returns: The number of bricks.
        """
        return len(self.single_neighbour_modules)

    @property
    def max_potential_single_neighbour_modules(self) -> int:
        """
        Get the maximum number of bricks that could potentially have only one neighbour if this set of modules was rearranged in an optimal way.

        This calculates "l_max" from the paper.

        :returns: The calculated number.
        """
        # Snake-like is an optimal arrangement.
        #
        #   B B B B B
        #   | | | | |
        # B-C-B-B-B-B-B
        #   | | | | |
        #   B B B B B
        #
        # Expected sequence:
        # | num bricks | 0 1 2 3 4 5 6 7 8 9
        # | return val | 0 1 2 3 4 4 5 6 6 7

        return self.num_modules - 1 - max(0, (self.num_modules - 3) // 3)

    @property
    def num_double_neighbour_bricks(self) -> int:
        """
        Get the number of bricks that are connected to exactly two other modules.

        Both children and parent are counted.

        :returns: The number of bricks.
        """
        return len(self.double_neighbour_bricks)

    @property
    def num_double_neighbour_active_hinges(self) -> int:
        """
        Get the number of active hinges that are connected to exactly two other modules.

        Both children and parent are counted.

        :returns: The number of active hinges.
        """
        return len(self.double_neighbour_active_hinges)

    @property
    def potential_double_neighbour_bricks_and_active_hinges(self) -> int:
        """
        Get the maximum number of bricks and active hinges that could potentially have exactly two neighbours if this set of modules was rearranged in an optimal way.

        This calculates e_max from the paper.

        :returns: The calculated number.
        """
        #
        # C-M-M-M-M-M
        #
        # Snake in direction is optimal, no matter whether modules are bricks or active hinges.
        #
        # Simply add up the number of bricks and active hinges and subtract 1 for the final module.

        return max(0, self.num_bricks + self.num_active_hinges - 1)

    @property
    def double_neighbour_brick_and_active_hinge_proportion(self) -> float:
        """
        Get the ratio between the number of bricks and active hinges with exactly two neighbours and how many that could potentially have been if this set of modules was rearranged in an optimal way.

        This calculate length of limbs proportion(extensiveness) from the paper.

        :returns: The proportion.
        """
        if self.potential_double_neighbour_bricks_and_active_hinges == 0:
            return 0.0

        return (
            self.num_double_neighbour_bricks
            + self.num_double_neighbour_active_hinges
        ) / self.potential_double_neighbour_bricks_and_active_hinges

    @property
    def bounding_box_volume(self) -> int:
        """
        Get the volume of the bounding box.

        This calculates m_area from the paper.

        :returns: The volume.
        """
        return (
            self.bounding_box_width
            * self.bounding_box_height
            * self.bounding_box_depth
        )

    @property
    def bounding_box_volume_coverage(self) -> float:
        """
        Get the proportion of the bounding box that is filled with modules.

        This calculates 'coverage' from the paper.

        :returns: The proportion.
        """
        return self.num_modules / self.bounding_box_volume

    @property
    def branching(self) -> float:
        """
        Get the 'branching' measurement from the paper.

        Alias for filled_core_and_bricks_proportion.

        :returns: Branching measurement.
        """
        return self.filled_core_and_bricks_proportion

    @property
    def limbs(self) -> float:
        """
        Get the 'limbs' measurement from the paper.

        Alias for single_neighbour_brick_proportion.

        :returns: Limbs measurement.
        """
        if self.max_potential_single_neighbour_modules == 0:
            return 0.0
        return (
            self.num_single_neighbour_modules
            / self.max_potential_single_neighbour_modules
        )

    @property
    def length_of_limbs(self) -> float:
        """
        Get the 'length of limbs' measurement from the paper.

        Alias for double_neighbour_brick_and_active_hinge_proportion.

        :returns: Length of limbs measurement.
        """
        return self.double_neighbour_brick_and_active_hinge_proportion

    @property
    def coverage(self) -> float:
        """
        Get the 'coverage' measurement from the paper.

        Alias for bounding_box_volume_coverage.

        :returns: Coverage measurement.
        """
        return self.bounding_box_volume_coverage

    @property
    def proportion_2d(self) -> float:
        """
        Get the 'proportion' measurement from the paper.

        Only for 2d robots.

        :returns: Proportion measurement.
        """
        # assert self.is_2d
        if not self.is_2d:
            msg = "Proportion is only defined for 2D robots."
            raise ValueError(msg)

        return min(self.bounding_box_depth, self.bounding_box_width) / max(
            self.bounding_box_depth, self.bounding_box_width
        )

    @property
    def symmetry(self) -> float:
        """
        Get the 'symmetry' measurement from the paper, but extended to 3d.

        :returns: Symmetry measurement.
        """
        return max(self.xy_symmetry, self.xz_symmetry, self.yz_symmetry)
