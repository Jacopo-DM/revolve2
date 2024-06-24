from abc import ABC, abstractmethod
from typing import Any

from ._evaluator import Evaluator

TPopulation = Any  # An alias for Any signifying that a population can vary depending on use-case.


class Learner(ABC):
    """A Learner object that enables learning for individuals in an
    evolutionary process.

    TODO: use link for explanation


    """

    _reward_function: Evaluator

    @abstractmethod
    def learn(self, population: TPopulation) -> TPopulation:
        """Make Individuals from a population learn.

        :param population: The population.
        :type population: TPopulation
        :returns: The learned population.
        :rtype: TPopulation

        """
