"""Evaluator class."""

from genotype import Genotype
from revolve2.ci_group import fitness_functions, terrains
from revolve2.ci_group.simulation_parameters import (
    make_standard_batch_parameters,
)
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
    ) -> None:
        """Initialize this object.

        :param headless: `headless` parameter for the physics simulator.
        :param num_simulators: `num_simulators` parameter for the
            physics simulator.
        """
        self._simulator = LocalSimulator(
            headless=headless,
            num_simulators=num_simulators,
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

        # Simulate all scenes.
        scene_states = simulate_scenes(
            simulator=self._simulator,
            batch_parameters=make_standard_batch_parameters(),
            scenes=scenes,
        )

        # Calculate the xy displacements.
        fitnesses = []
        for robot, states in zip(robots, scene_states, strict=False):
            robot_states = [
                state.get_modular_robot_simulation_state(robot)
                .get_pose()
                .position.xyz
                for state in states
            ]
            fitnesses.append(fitness_functions.xy_displacement(robot_states))

        return fitnesses
