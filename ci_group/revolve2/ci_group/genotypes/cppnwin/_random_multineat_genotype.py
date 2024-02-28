import multineat
from .modular_robot._multineat_params import DefaultGenome

HIDDEN_ACT_F = multineat.ActivationFunction.TANH
SEARCH_MODE = multineat.SearchMode.COMPLEXIFYING


def random_multineat_genotype(
    innov_db: multineat.InnovationDatabase,
    rng: multineat.RNG,
    multineat_params: multineat.Parameters,
    output_activation_func: multineat.ActivationFunction,
    num_inputs: int,
    num_outputs: int,
    num_initial_mutations: int,
) -> multineat.Genome:
    """
    Create a random multineat genotype.

    A CPPNWIN network starts empty.
    A random network is created by mutating `num_initial_mutations` times.

    :param innov_db: Multineat innovation database. See Multineat library.
    :param rng: Random number generator.
    :param multineat_params: Multineat parameters. See Multineat library.
    :param output_activation_func: Activation function for the output layer. See Multineat library.
    :param num_inputs: Number of input for the network.
    :param num_outputs: Number fo outputs for the network.
    :param num_initial_mutations: The number of times to mutate to create a random network.
    :returns: The created genotype.
    """
    genotype = multineat.Genome(
        0,  # ID
        num_inputs,
        0,  # n_hidden
        num_outputs,
        False,  # FS_NEAT
        output_activation_func,  # output activation type
        HIDDEN_ACT_F,  # hidden activation type
        0,  # seed_type
        multineat_params,
        0,  # number of hidden layers
    )

    for _ in range(num_initial_mutations):
        genotype = genotype.MutateWithConstraints(
            False,
            SEARCH_MODE,
            innov_db,
            multineat_params,
            rng,
        )

    return genotype
