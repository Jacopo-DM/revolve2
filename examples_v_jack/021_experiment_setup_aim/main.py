"""Main script for the example."""

import logging
from datetime import datetime

import config
import numpy as np
from aim import Run
from revolve2.experimentation.logging import setup_logging


def run_experiment(
    num_samples: int, probability: float, repetitions: int
) -> None:
    """
    Run all runs of an experiment using the provided parameters.

    :param num_samples: The number of samples to use for this experiment.
    :param probability: The probability to use for this experiment.
    """
    success_ratios = []

    run = Run()
    run["hparams"] = {
        "num_samples": num_samples,
        "probability": probability,
        "repetitions": repetitions,
    }

    for rep_id in range(repetitions):
        logging.info(
            f"Running experiment ( repetition {rep_id} num_samples {num_samples} probability {probability} )"
        )

        # Create a seed from the current time in microseconds.
        seed = int(datetime.now().timestamp() * 1e6)
        rng = np.random.Generator(np.random.PCG64(seed))

        # Perform the experiment
        samples = rng.binomial(n=1, p=probability, size=num_samples)

        # Calculate the ratio of success and save it.
        success_ratio = np.sum(samples == 1) / num_samples
        success_ratios.append(success_ratio)

        # Log the success ratio for this repetition.
        run.track(success_ratio, name="success_ratio", step=rep_id)
        run.track(seed, name="seed", step=rep_id)

    # Do some simple analysis using the performed repetitions.
    std = np.std(success_ratios)
    mean = np.mean(success_ratios)
    logging.info(f"mean {mean} std {std}")
    run.track(mean, name="mean")
    run.track(std, name="std")


def main() -> None:
    """Run the simulation."""
    setup_logging()

    logging.info("Starting program.")
    for num_samples in config.NUM_SAMPLES:
        for probability in config.PROBABILITIES:
            for repetitions in config.NUM_REPETITIONS:
                run_experiment(
                    num_samples=num_samples,
                    probability=probability,
                    repetitions=repetitions,
                )


if __name__ == "__main__":
    main()
