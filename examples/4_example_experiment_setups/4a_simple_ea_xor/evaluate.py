"""Evaluation functions."""

import numpy as np
import numpy.typing as npt
from genotype import Genotype
from revolve2.experimentation.evolution.abstract_elements import (
    Evaluator as Eval,
)


class Evaluator(Eval):
    """Here we make an evaluator object, based on the abstract evaluator
    defined in Revolve2.


    """

    @staticmethod
    def evaluate_network(
        params: npt.NDArray[np.float64], inputs: npt.NDArray[np.float64]
    ) -> np.float64:
        """Pass two inputs through a fully connected relu network.

        :param params: The parameters to evaluate.
        :type params: npt.NDArray[np.float64]
        :param inputs: Inputs for network. 2x1 floats.
        :type inputs: npt.NDArray[np.float64]
        :returns: The output of the network.
        :rtype: np.float64

        """
        # First layer
        n0 = np.maximum(0, np.dot(params[:2], inputs) + params[2])
        n1 = np.maximum(0, np.dot(params[3:5], inputs) + params[5])

        # Second layer
        output: np.float64 = np.maximum(
            0, n0 * params[6] + n1 * params[7] + params[8]
        )
        return output

    def evaluate(self, population: list[Genotype]) -> list[float]:
        """Measure one set of parameters.

        :param population: The population of parameters to measure.
        :type population: list[Genotype]
        :returns: Negative sum of squared errors and each individual
            error. 5x1 floats.
        :rtype: list[float]

        """
        results = []
        for genotype in population:
            # Define all possible inputs for xor and the expected outputs
            inputs = np.array([[0, 0], [1, 0], [0, 1], [1, 1]])
            expected_outputs = np.array([0, 1, 1, 0])

            # Evaluate the provided network parameters
            outputs = np.array([
                self.evaluate_network(genotype.parameters, input)
                for input in inputs
            ])

            # Calculate the difference between the network outputs and the expect outputs
            errors = outputs - expected_outputs
            """Now we add the sum of squared errors to the results.

            In our case 0 would be an optimal result. We invert so we
            can maximize the fitness instead of minimize. Finally we
            convert from a numpy float_ type to the python float type.
            This is not really important.
            """
            results.append(float(-np.sum(errors**2)))
        return results
