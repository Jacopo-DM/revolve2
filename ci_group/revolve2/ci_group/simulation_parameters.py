"""Standard simulation functions and parameters."""

from revolve2.simulation.simulator import BatchParameters

STANDARD_SIMULATION_TIME = 60
STANDARD_SAMPLING_FREQUENCY = 5
STANDARD_SIMULATION_TIMESTEP = 0.004
STANDARD_CONTROL_FREQUENCY = 15


def make_standard_batch_parameters(
    simulation_time: int = STANDARD_SIMULATION_TIME,
    sampling_frequency: float | None = STANDARD_SAMPLING_FREQUENCY,
    simulation_timestep: float = STANDARD_SIMULATION_TIMESTEP,
    control_frequency: float = STANDARD_CONTROL_FREQUENCY,
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
    return BatchParameters(
        simulation_time=simulation_time,
        sampling_frequency=sampling_frequency,
        simulation_timestep=simulation_timestep,
        control_frequency=control_frequency,
    )
