"""
Calculate Morphological Novelty across a Population.

Using the MorphologicalNoveltyMetric for evaluating a population of robots can be done as shown in the code below.

    >>> robots: list[revolve2.modular_robot.ModularRobot]
    >>> novelties = get_novelty_from_population(robots)
"""

from ci_group.morphological_novelty_metric._morphological_novelty_metric import (
    get_novelty_from_population,
)

__all__ = ["get_novelty_from_population"]
