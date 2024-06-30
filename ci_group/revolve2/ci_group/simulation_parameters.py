"""Standard simulation functions and parameters."""

import logging

from revolve2.simulation.simulator import BatchParameters

# TODO(jmdm): do different integrators make a difference?
STANDARD_SIMULATION_TIME = 100
STANDARD_SAMPLING_FREQUENCY = 5
STANDARD_SIMULATION_TIMESTEP = 0.005
STANDARD_CONTROL_FREQUENCY = 20
STANDARD_INTEGRATOR: str = "RK4"  # "implicitfast"

ran_once = False


def make_standard_batch_parameters(
    simulation_time: int = STANDARD_SIMULATION_TIME,
    sampling_frequency: float | None = STANDARD_SAMPLING_FREQUENCY,
    simulation_timestep: float = STANDARD_SIMULATION_TIMESTEP,
    control_frequency: float = STANDARD_CONTROL_FREQUENCY,
    integrator: str = STANDARD_INTEGRATOR,
) -> BatchParameters:
    """Create batch parameters as standardized within the CI Group.

    :param simulation_time: As defined in the `BatchParameters` class.
        (Default value = STANDARD_SIMULATION_TIME)
    :type simulation_time: int
    :param sampling_frequency: As defined in the `BatchParameters`
        class. (Default value = STANDARD_SAMPLING_FREQUENCY)
    :type sampling_frequency: float | None
    :param simulation_timestep: As defined in the `BatchParameters`
        class. (Default value = STANDARD_SIMULATION_TIMESTEP)
    :type simulation_timestep: float
    :param control_frequency: As defined in the `BatchParameters` class.
        (Default value = STANDARD_CONTROL_FREQUENCY)
    :type control_frequency: float
    :returns: The create batch parameters.
    :rtype: BatchParameters

    """
    global ran_once
    if not ran_once:
        logging.info(f"ST = {simulation_time}")
        logging.info(
            f"SF = {sampling_frequency}~{round(1 / sampling_frequency, 4)}"
        )
        logging.info(f"TS = {simulation_timestep}")
        logging.info(
            f"CF = {control_frequency}~{round(1 / control_frequency, 4)}"
        )
        logging.info(f"DT = {integrator}")
        ran_once = True

    return BatchParameters(
        simulation_time=simulation_time,
        sampling_frequency=sampling_frequency,
        simulation_timestep=simulation_timestep,
        control_frequency=control_frequency,
        integrator=integrator,
    )
