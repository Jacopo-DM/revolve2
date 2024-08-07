"""Evaluator class."""

import logging

import numpy as np
import numpy.typing as npt
from readable_number import ReadableNumber
from revolve2.ci_group import fitness_functions, terrains
from revolve2.ci_group.simulation_parameters import (
    make_standard_batch_parameters,
)
from revolve2.modular_robot import ModularRobot
from revolve2.modular_robot.body.base import ActiveHinge, Body
from revolve2.modular_robot.brain.cpg import (
    BrainCpgNetworkStatic,
    CpgNetworkStructure,
)
from revolve2.modular_robot_simulation import (
    ModularRobotScene,
    Terrain,
    simulate_scenes,
)
from revolve2.simulators.mujoco_simulator import LocalSimulator


class Evaluator:
    """Provides evaluation of robots."""

    _simulator: LocalSimulator
    _terrain: Terrain
    _cpg_network_structure: CpgNetworkStructure
    _body: Body
    _output_mapping: list[tuple[int, ActiveHinge]]

    def __init__(
        self,
        headless: bool,
        num_simulators: int,
        cpg_network_structure: CpgNetworkStructure,
        body: Body,
        output_mapping: list[tuple[int, ActiveHinge]],
    ) -> None:
        """Initialize this object.

        :param headless: `headless` parameter for the physics simulator.
        :param num_simulators: `num_simulators` parameter for the
            physics simulator.
        :param cpg_network_structure: Cpg structure for the brain.
        :param body: Modular body of the robot.
        :param output_mapping: A mapping between active hinges and the
            index of their corresponding cpg in the cpg network
            structure.
        """
        self._simulator = LocalSimulator(
            headless=headless, num_simulators=num_simulators
        )
        self._terrain = terrains.flat()
        self._cpg_network_structure = cpg_network_structure
        self._body = body
        self._output_mapping = output_mapping

    def evaluate(
        self,
        solutions: list[npt.NDArray[np.float64]],
    ) -> npt.NDArray[np.float64]:
        """Evaluate multiple robots.

        Fitness is the distance traveled on the xy plane.

        :param solutions: Solutions to evaluate.
        :type solutions: list[npt.NDArray[np.float64]]
        :returns: Fitnesses of the solutions.
        :rtype: npt.NDArray[np.float64]

        """
        # Create robots from the brain parameters.
        robots = [
            ModularRobot(
                body=self._body,
                brain=BrainCpgNetworkStatic.uniform_from_params(
                    params=params,
                    cpg_network_structure=self._cpg_network_structure,
                    initial_state_uniform=1.0,  # 2 / np.sqrt(2),
                    output_mapping=self._output_mapping,
                ),
            )
            for params in solutions
        ]

        # Create the scenes.
        scenes = []
        for robot in robots:
            scene = ModularRobotScene(terrain=self._terrain)
            scene.add_robot(robot)
            scenes.append(scene)

        # Simulate all scenes.
        scene_states = simulate_scenes(
            simulator=self._simulator,
            batch_parameters=make_standard_batch_parameters(),
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
        return np.array(fitness)
