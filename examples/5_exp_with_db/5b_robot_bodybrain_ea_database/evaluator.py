"""Evaluator class."""

import logging

import numpy as np
import revolve2.ci_group.simulation_parameters as sim_p
from database_components import Genotype
from readable_number import ReadableNumber
from revolve2.ci_group import fitness_functions, terrains
from revolve2.experimentation.evolution.abstract_elements import (
    Evaluator as Eval,
)
from revolve2.modular_robot_simulation import (
    ModularRobotScene,
    Terrain,
    simulate_scenes,
)
from revolve2.simulators.mujoco_simulator import LocalSimulator


class Evaluator(Eval):
    """Provides evaluation of robots."""

    _simulator: LocalSimulator
    _terrain: Terrain

    def __init__(
        self,
        headless: bool,
        num_simulators: int,
        *,
        start_paused: bool = False,
    ) -> None:
        """Initialize this object.

        :param headless: `headless` parameter for the physics simulator.
        :param num_simulators: `num_simulators` parameter for the
            physics simulator.
        """
        self._simulator = LocalSimulator(
            headless=headless,
            num_simulators=num_simulators,
            start_paused=start_paused,
        )
        self._terrain = terrains.flat()

    def evaluate(
        self,
        population: list[Genotype],
    ) -> list[float]:
        """Evaluate multiple robots.

        Fitness is the distance traveled on the xy plane.

        :param population: The robots to simulate.
        :type population: list[Genotype]
        :returns: Fitnesses of the robots.
        :rtype: list[float]

        """
        robots = [genotype.develop() for genotype in population]
        # Create the scenes.
        scenes = []
        for robot in robots:
            scene = ModularRobotScene(terrain=self._terrain)
            scene.add_robot(robot)
            scenes.append(scene)

        scene_states = simulate_scenes(
            simulator=self._simulator,
            batch_parameters=sim_p.make_standard_batch_parameters(),
            scenes=scenes,
        )

        # Calculate the xy displacements.
        fitness = []
        for robot, states in zip(robots, scene_states, strict=False):
            _states = [
                state.get_modular_robot_simulation_state(robot)
                .get_pose()
                .position.xyz
                for state in states
            ]
            fitness.append(fitness_functions.xy_displacement(_states))

        logging.info(f"fit: {ReadableNumber(np.max(fitness))}")
        logging.info(f"fit: {ReadableNumber(np.mean(fitness))}")
        logging.info(f"fit: {ReadableNumber(np.min(fitness))}")
        return fitness
