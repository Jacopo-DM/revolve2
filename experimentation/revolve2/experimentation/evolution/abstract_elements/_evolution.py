from abc import ABC, abstractmethod
from typing import Any

TPopulation = Any  # An alias for Any signifying that a population can vary depending on use-case.


class Evolution(ABC):
    """An abstract object to encapsulate an evolutionary process."""

    @abstractmethod
    def step(self, population: TPopulation, **kwargs: Any) -> TPopulation:
        """Step the current evolution by one iteration..

        :param population: The current population.
        :type population: TPopulation
        :param **kwargs:
        :type **kwargs: Any
        :returns: The population resulting from the step
        :rtype: TPopulation

        """
