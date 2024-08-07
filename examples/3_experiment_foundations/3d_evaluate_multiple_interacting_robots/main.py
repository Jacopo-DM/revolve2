"""Main script for the example."""

import logging
from itertools import starmap

from pyrr import Vector3
from revolve2.ci_group import fitness_functions, modular_robots_v2, terrains
from revolve2.ci_group.simulation_parameters import (
    make_standard_batch_parameters,
)
from revolve2.experimentation.logging import setup_logging
from revolve2.experimentation.rng import make_rng_time_seed
from revolve2.modular_robot import ModularRobot
from revolve2.modular_robot.brain.cpg import BrainCpgNetworkNeighborRandom
from revolve2.modular_robot_simulation import ModularRobotScene, simulate_scenes
from revolve2.simulation.scene import Pose
from revolve2.simulators.mujoco_simulator import LocalSimulator


def main() -> None:
    """Run the simulation.


    :rtype: None

    """
    # Set up logging.
    setup_logging()

    # Set up the random number generator.
    rng = make_rng_time_seed()

    # Create the robots.
    bodies = [
        modular_robots_v2.gecko_v2(),
        modular_robots_v2.ant_v2(),
        modular_robots_v2.snake_v2(),
        modular_robots_v2.spider_v2(),
    ]
    brains = [BrainCpgNetworkNeighborRandom(body, rng) for body in bodies]
    robots = list(starmap(ModularRobot, zip(bodies, brains, strict=False)))
    """Contrary to the previous examples, we now create a single scene and put
    all robots in it.

    We place the robots at separate locations in the terrain so they do
    not overlap at the start of the simulation.
    """
    scene = ModularRobotScene(terrain=terrains.flat())
    poses = [
        Pose(Vector3([1.0, 0.0, 0.0])),
        Pose(Vector3([-1.0, 0.0, 0.0])),
        Pose(Vector3([0.0, 1.0, 0.0])),
        Pose(Vector3([0.0, -1.0, 0.0])),
    ]
    for robot, pose in zip(robots, poses, strict=False):
        scene.add_robot(robot, pose=pose)

    # Create the simulator.
    simulator = LocalSimulator(headless=False, num_simulators=1)

    # Simulate all scenes.
    scene_states = simulate_scenes(
        simulator=simulator,
        batch_parameters=make_standard_batch_parameters(),
        scenes=scene,
    )

    # Calculate the xy displacements.
    xy_displacements = []
    for robot in robots:
        robot_satates = [
            state.get_modular_robot_simulation_state(robot)
            .get_pose()
            .position.xyz
            for state in scene_states
        ]
        xy_displacements.append(
            fitness_functions.xy_displacement(robot_satates)
        )

    logging.info(xy_displacements)


if __name__ == "__main__":
    main()
