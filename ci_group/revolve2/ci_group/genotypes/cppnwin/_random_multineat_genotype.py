import multineat


def random_multineat_genotype(
    innov_db: multineat.InnovationDatabase,
    rng: multineat.RNG,
    multineat_params: multineat.Parameters,
    output_activation_func: multineat.ActivationFunction,
    num_inputs: int,
    num_outputs: int,
    num_initial_mutations: int,
    hidden_act_f: multineat.ActivationFunction,
    search_mode: multineat.SearchMode,
) -> multineat.Genome:
    """Create a random multineat genotype.

    A CPPNWIN network starts empty.
    A random network is created by mutating `num_initial_mutations` times.

    :param innov_db: Multineat innovation database. See Multineat
        library.
    :type innov_db: multineat.InnovationDatabase
    :param rng: Random number generator.
    :type rng: multineat.RNG
    :param multineat_params: Multineat parameters. See Multineat
        library.
    :type multineat_params: multineat.Parameters
    :param output_activation_func: Activation function for the output
        layer. See Multineat library.
    :type output_activation_func: multineat.ActivationFunction
    :param num_inputs: Number of input for the network.
    :type num_inputs: int
    :param num_outputs: Number fo outputs for the network.
    :type num_outputs: int
    :param num_initial_mutations: The number of times to mutate to
        create a random network.
    :type num_initial_mutations: int
    :param search_mode: (Default value = multineat.SearchMode.BLENDED)
    :type search_mode: multineat.SearchMode
    :param hidden_act_f: (Default value =
        multineat.ActivationFunction.LINEAR)
    :type hidden_act_f: multineat.ActivationFunction
    :returns: The created genotype.
    :rtype: multineat.Genome

    """
    genotype = multineat.Genome(
        0,  # ID
        num_inputs,
        num_inputs,  # hidden size if seed_type == 1, else ignored
        num_outputs,
        False,  # FS_NEAT
        output_activation_func,  # output activation type
        hidden_act_f,  # hidden activation type
        1,  # seed_type
        multineat_params,
        2,  # number of hidden layers
    )

    for _ in range(num_initial_mutations):
        genotype = genotype.MutateWithConstraints(
            False,
            search_mode,
            innov_db,
            multineat_params,
            rng,
        )

    return genotype
