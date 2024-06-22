"""
DefaultGenome: genome parameters as found in the MultiNEAT documentation
GivenGenome: genome parameters when initializing a new genome with multineat.Parameters()
"""

DefaultGenome: dict[str, float | int | bool] = {
    # Size of population
    "PopulationSize": 300,
    # If true, this enables dynamic compatibility thresholding
    # It will keep the number of species between MinSpecies and MaxSpecies
    "DynamicCompatibility": True,
    # Minimum number of species
    "MinSpecies": 5,
    # Maximum number of species
    "MaxSpecies": 10,
    # Don't wipe the innovation database each generation?
    "InnovationsForever": True,
    # Allow clones or nearly identical genomes to exist simultaneously in the population.
    # This is useful for non-deterministic environments,
    # as the same individual will get more than one chance to prove himself, also
    # there will be more chances the same individual to mutate in different ways.
    # The drawback is greatly increased time for reproduction. If you want to
    # search quickly, yet less efficient, leave this to true.
    "AllowClones": True,
    # Keep an archive of genomes and don't allow any new genome to exist in the archive or the population
    "ArchiveEnforcement": False,
    # Normalize genome size when calculating compatibility
    "NormalizeGenomeSize": True,
    # When true, don't have a special bias neuron and treat all inputs equal
    "DontUseBiasNeuron": False,
    # When false, this prevents any recurrent pathways in the genomes from forming
    "AllowLoops": True,
    # Age treshold, meaning if a species is below it, it is considered young
    "YoungAgeTreshold": 5,
    # Fitness boost multiplier for young species (1.0 means no boost)
    # Make sure it is > 1.0 to avoid confusion
    "YoungAgeFitnessBoost": 1.1,
    # Number of generations without improvement (stagnation) allowed for a species
    "SpeciesMaxStagnation": 50,
    # Minimum jump in fitness necessary to be considered as improvement.
    # Setting this value to 0.0 makes the system to behave like regular NEAT.
    "StagnationDelta": 0.0,
    # AgeGens threshold, meaning if a species is above it, it is considered old
    "OldAgeTreshold": 30,
    # Multiplier that penalizes old species.
    # Make sure it is < 1.0 to avoid confusion.
    "OldAgePenalty": 0.5,
    # Detect competetive coevolution stagnation
    # This kills the worst species of age >N (each X generations)
    "DetectCompetetiveCoevolutionStagnation": False,
    # Each X generation..
    "KillWorstSpeciesEach": 15,
    # Of age above..
    "KillWorstAge": 10,
    # Percent of best individuals that are allowed to reproduce. 1.0 100%
    "SurvivalRate": 0.25,
    # Prob. for a baby to result from sexual reproduction (crossover/mating). 1.0 100%
    # If asexual reproduction is chosen, the baby will be mutated 100%
    "CrossoverRate": 0.7,
    # If a baby results from sexual reproduction, this Prob. determines if mutation will
    # be performed after crossover. 1.0 100% (always mutate after crossover)
    "OverallMutationRate": 0.25,
    # Prob. for a baby to result from inter-species mating.
    "InterspeciesCrossoverRate": 0.0001,
    # Prob. for a baby to result from Multipoint Crossover when mating. 1.0 100%
    # The default is the Average mating.(params):
    "MultipointCrossoverRate": 0.75,
    # Performing roulette wheel selection or not?
    "RouletteWheelSelection": False,
    # For tournament selection
    "TournamentSize": 4,
    # Fraction of individuals to be copied unchanged
    "EliteFraction": 0.01,
    "NeuronRecursionLimit": 16384,
    # Using phased search or not
    "PhasedSearching": False,
    # Using delta coding or not
    "DeltaCoding": False,
    # What is the MPC + base MPC needed to begin simplifying phase
    "SimplifyingPhaseMPCTreshold": 20,
    # How many generations of global stagnation should have passed to enter simplifying phase
    "SimplifyingPhaseStagnationTreshold": 30,
    # How many generations of MPC stagnation are needed to turn back on complexifying
    "ComplexityFloorGenerations": 40,
    # the K constant
    "NoveltySearch_K": 15,
    # Sparseness treshold. Add to the archive if above
    "NoveltySearch_P_min": 0.5,
    # Dynamic Pmin?
    "NoveltySearch_Dynamic_Pmin": True,
    # How many evaluations should pass without adding to the archive
    # in order to lower Pmin
    "NoveltySearch_No_Archiving_Stagnation_Treshold": 150,
    # How should it be multiplied (make it less than 1.0)
    "NoveltySearch_Pmin_lowering_multiplier": 0.9,
    # Not lower than this value
    "NoveltySearch_Pmin_min": 0.05,
    # How many one-after-another additions to the archive should
    # pass in order to raise Pmin
    "NoveltySearch_Quick_Archiving_Min_Evaluations": 8,
    # How should it be multiplied (make it more than 1.0)
    "NoveltySearch_Pmin_raising_multiplier": 1.1,
    # Per how many evaluations to recompute the sparseness of the population
    "NoveltySearch_Recompute_Sparseness_Each": 25,
    # Prob. for a baby to be mutated with the Add-Neuron mutation.
    "MutateAddNeuronProb": 0.01,
    # Allow splitting of any recurrent links
    "SplitRecurrent": True,
    # Allow splitting of looped recurrent links
    "SplitLoopedRecurrent": True,
    # missing --> "NeuronTries": 64,
    # Prob. for a baby to be mutated with the Add-Link mutation
    "MutateAddLinkProb": 0.03,
    # Prob. for a new incoming link to be from the bias neuron
    # This enforces it. A value of 0.0 doesn't mean there will not be such links
    "MutateAddLinkFromBiasProb": 0.0,
    # Prob. for a baby to be mutated with the Remove-Link mutation
    "MutateRemLinkProb": 0.0,
    # Prob. for a baby that a simple neuron will be replaced with a link
    "MutateRemSimpleNeuronProb": 0.0,
    # Maximum number of tries to find 2 neurons to add/remove a link
    "LinkTries": 32,
    # Prob. that a link mutation will be made recurrent
    "RecurrentProb": 0.25,
    # Prob. that a recurrent link mutation will be looped
    "RecurrentLoopProb": 0.25,
    # Prob. for a baby's weights to be mutated
    "MutateWeightsProb": 0.90,
    # Prob. for a severe (shaking) weight mutation
    "MutateWeightsSevereProb": 0.25,
    # Prob. for a particular gene's weight to be mutated. 1.0 100%
    "WeightMutationRate": 1.0,
    # Prob. for a particular gene to be mutated via replacement of the weight. 1.0 = 100%
    "WeightReplacementRate": 0.2,
    # Maximum perturbation for a weight mutation
    "WeightMutationMaxPower": 1.0,
    # Maximum magnitude of a replaced weight
    "WeightReplacementMaxPower": 1.0,
    # Maximum absolute magnitude of a weight
    "MaxWeight": 8.0,
    # Prob. for a baby's A activation function parameters to be perturbed
    "MutateActivationAProb": 0.0,
    # Prob. for a baby's B activation function parameters to be perturbed
    "MutateActivationBProb": 0.0,
    # Maximum magnitude for the A parameter perturbation
    "ActivationAMutationMaxPower": 0.0,
    # Maximum magnitude for the B parameter perturbation
    "ActivationBMutationMaxPower": 0.0,
    # Maximum magnitude for time costants perturbation
    "TimeConstantMutationMaxPower": 0.0,
    # Maximum magnitude for biases perturbation
    "BiasMutationMaxPower": 1.0,  # = WeightMutationMaxPower
    # Activation parameter A min/max
    "MinActivationA": 1.0,
    "MaxActivationA": 1.0,
    # Activation parameter B min/max
    "MinActivationB": 0.0,
    "MaxActivationB": 0.0,
    # Prob. for a baby that an activation function type will be changed for a single neuron
    # considered a structural mutation because of the large impact on fitness
    "MutateNeuronActivationTypeProb": 0.0,
    "MutateOutputActivationFunction": False,
    # Probs. for a particular activation function appearance
    "ActivationFunction_SignedSigmoid_Prob": 0.0,
    "ActivationFunction_UnsignedSigmoid_Prob": 1.0,
    "ActivationFunction_Tanh_Prob": 0.0,
    "ActivationFunction_TanhCubic_Prob": 0.0,
    "ActivationFunction_SignedStep_Prob": 0.0,
    "ActivationFunction_UnsignedStep_Prob": 0.0,
    "ActivationFunction_SignedGauss_Prob": 0.0,
    "ActivationFunction_UnsignedGauss_Prob": 0.0,
    "ActivationFunction_Abs_Prob": 0.0,
    "ActivationFunction_SignedSine_Prob": 0.0,
    "ActivationFunction_UnsignedSine_Prob": 0.0,
    "ActivationFunction_Linear_Prob": 0.0,
    # missing --> "ActivationFunction_SignedSquare_Prob": 0.0,
    # missing --> "ActivationFunction_UnsignedSquare_Prob": 0.0,
    # missing --> "ActivationFunction_Relu_Prob": 0.0,
    # missing --> "ActivationFunction_Softplus_Prob": 0.0,
    # Prob. for a baby's neuron time constant values to be mutated
    "MutateNeuronTimeConstantsProb": 0.0,
    # Prob. for a baby's neuron bias values to be mutated
    "MutateNeuronBiasesProb": 0.0,
    # Time constant range
    "MinNeuronTimeConstant": 0.0,
    "MaxNeuronTimeConstant": 0.0,
    # Bias range
    "MinNeuronBias": 0.0,
    "MaxNeuronBias": 0.0,
    # missing --> "NeuronTraits": None,
    # missing --> "LinkTraits": None,
    # missing --> "GenomeTraits": None,
    # Trait mutation probabilities
    "MutateNeuronTraitsProb": 1.0,
    "MutateLinkTraitsProb": 1.0,
    "MutateGenomeTraitsProb": 1.0,
    # Percent of disjoint genes importance
    "DisjointCoeff": 1.0,
    # Percent of excess genes importance
    "ExcessCoeff": 1.0,
    # Node-specific activation parameter A difference importance
    "ActivationADiffCoeff": 0.0,
    # Node-specific activation parameter B difference importance
    "ActivationBDiffCoeff": 0.0,
    # Average weight difference importance
    "WeightDiffCoeff": 0.5,
    # Average time constant difference importance
    "TimeConstantDiffCoeff": 0.0,
    # Average bias difference importance
    "BiasDiffCoeff": 0.0,
    # Activation function type difference importance
    "ActivationFunctionDiffCoeff": 0.0,
    # Compatibility treshold
    "CompatTreshold": 5.0,
    # Minumal value of the compatibility treshold
    "MinCompatTreshold": 0.2,
    # Modifier per generation for keeping the species stable
    "CompatTresholdModifier": 0.3,
    # Per how many generations to change the treshold
    # (used in generational mode)
    "CompatTreshChangeInterval_Generations": 1,
    # Per how many evaluations to change the treshold
    # (used in steady state mode)
    "CompatTreshChangeInterval_Evaluations": 10,
    # How deep the quadtree will search. Default is 0.3
    "DivisionThreshold": 0.03,
    # How much variance is needed in order to express stuff
    "VarianceThreshold": 0.03,
    # Used for Band prunning
    "BandThreshold": 0.3,
    # Max and Min Depths of the quadtree
    "InitialDepth": 3,
    "MaxDepth": 3,
    # How many hidden layers before connecting nodes to output. At 0 there is
    # one hidden layer. At 1, there are two and so on.
    "IterationLevel": 1,
    # The Bias value for the CPPN queries
    "CPPN_Bias": 1.0,
    # Quadtree Dimensions
    # The range of the tree. Typically set to 2,
    "Width": 2.0,
    "Height": 2.0,
    # The (x, y) coordinates of the tree
    "Qtree_X": 0.0,
    "Qtree_Y": 0.0,
    # Use Link Expression output
    "Leo": False,
    # Threshold above which a connection is expressed
    "LeoThreshold": 0.1,
    # Use geometric seeding. Currently only along the X axis
    "LeoSeed": False,
    "GeometrySeed": False,
}

GivenGenome: dict[str, float | int | bool] = {
    # -- > bool
    "AllowClones": True,
    "AllowLoops": True,
    "ArchiveEnforcement": False,
    "DeltaCoding": False,
    "DetectCompetetiveCoevolutionStagnation": False,
    "DontUseBiasNeuron": False,
    "DynamicCompatibility": True,
    "GeometrySeed": False,
    "InnovationsForever": True,
    "Leo": False,
    "LeoSeed": False,
    "MutateOutputActivationFunction": False,
    "NormalizeGenomeSize": True,
    "NoveltySearch_Dynamic_Pmin": True,
    "PhasedSearching": False,
    "RouletteWheelSelection": False,
    "SplitLoopedRecurrent": True,
    "SplitRecurrent": True,
    # -- > float
    "ActivationADiffCoeff": 0.0,
    "ActivationAMutationMaxPower": 0.0,
    "ActivationBDiffCoeff": 0.0,
    "ActivationBMutationMaxPower": 0.0,
    "ActivationFunctionDiffCoeff": 0.0,
    "ActivationFunction_Abs_Prob": 0.0,
    "ActivationFunction_Linear_Prob": 0.0,
    "ActivationFunction_SignedGauss_Prob": 0.0,
    "ActivationFunction_SignedSigmoid_Prob": 0.0,
    "ActivationFunction_SignedSine_Prob": 0.0,
    "ActivationFunction_SignedStep_Prob": 0.0,
    "ActivationFunction_TanhCubic_Prob": 0.0,
    "ActivationFunction_Tanh_Prob": 0.0,
    "ActivationFunction_UnsignedGauss_Prob": 0.0,
    "ActivationFunction_UnsignedSigmoid_Prob": 1.0,
    "ActivationFunction_UnsignedSine_Prob": 0.0,
    "ActivationFunction_UnsignedStep_Prob": 0.0,
    "BandThreshold": 0.3,
    "BiasDiffCoeff": 0.0,
    "BiasMutationMaxPower": 1.0,
    "CPPN_Bias": 1.0,
    "CompatTreshold": 5.0,
    "CompatTresholdModifier": 0.3,
    "CrossoverRate": 0.7,
    "DisjointCoeff": 1.0,
    "DivisionThreshold": 0.03,
    "EliteFraction": 0.01,
    "ExcessCoeff": 1.0,
    "Height": 2.0,
    "InterspeciesCrossoverRate": 0.0001,
    "LeoThreshold": 0.1,
    "MaxActivationA": 1.0,
    "MaxActivationB": 0.0,
    "MaxNeuronBias": 0.0,
    "MaxNeuronTimeConstant": 0.0,
    "MaxWeight": 8.0,
    "MinActivationA": 1.0,
    "MinActivationB": 0.0,
    "MinCompatTreshold": 0.2,
    "MinNeuronBias": 0.0,
    "MinNeuronTimeConstant": 0.0,
    "MultipointCrossoverRate": 0.75,
    "MutateActivationAProb": 0.0,
    "MutateActivationBProb": 0.0,
    "MutateAddLinkFromBiasProb": 0.0,
    "MutateAddLinkProb": 0.03,
    "MutateAddNeuronProb": 0.01,
    "MutateLinkTraitsProb": 1.0,
    "MutateNeuronActivationTypeProb": 0.0,
    "MutateNeuronBiasesProb": 0.0,
    "MutateNeuronTimeConstantsProb": 0.0,
    "MutateNeuronTraitsProb": 1.0,
    "MutateRemLinkProb": 0.0,
    "MutateRemSimpleNeuronProb": 0.0,
    "MutateWeightsProb": 0.9,
    "MutateWeightsSevereProb": 0.25,
    "NoveltySearch_P_min": 0.5,
    "NoveltySearch_Pmin_lowering_multiplier": 0.9,
    "NoveltySearch_Pmin_min": 0.05,
    "NoveltySearch_Pmin_raising_multiplier": 1.1,
    "OldAgePenalty": 0.5,
    "OverallMutationRate": 0.25,
    "Qtree_X": 0.0,
    "Qtree_Y": 0.0,
    "RecurrentLoopProb": 0.25,
    "RecurrentProb": 0.25,
    "StagnationDelta": 0.0,
    "SurvivalRate": 0.25,
    "TimeConstantDiffCoeff": 0.0,
    "TimeConstantMutationMaxPower": 0.0,
    "VarianceThreshold": 0.03,
    "WeightDiffCoeff": 0.5,
    "WeightMutationMaxPower": 1.0,
    "WeightMutationRate": 1.0,
    "WeightReplacementMaxPower": 1.0,
    "WeightReplacementRate": 0.2,
    "Width": 2.0,
    "YoungAgeFitnessBoost": 1.1,
    # -- > int
    "CompatTreshChangeInterval_Evaluations": 10,
    "CompatTreshChangeInterval_Generations": 1,
    "ComplexityFloorGenerations": 40,
    "InitialDepth": 3,
    "KillWorstAge": 10,
    "KillWorstSpeciesEach": 15,
    "LinkTries": 32,
    "MaxDepth": 3,
    "MaxSpecies": 10,
    "MinSpecies": 5,
    "NeuronRecursionLimit": 16384,
    "NoveltySearch_K": 15,
    "NoveltySearch_No_Archiving_Stagnation_Treshold": 150,
    "NoveltySearch_Quick_Archiving_Min_Evaluations": 8,
    "NoveltySearch_Recompute_Sparseness_Each": 25,
    "OldAgeTreshold": 30,
    "PopulationSize": 300,
    "SimplifyingPhaseMPCTreshold": 20,
    "SimplifyingPhaseStagnationTreshold": 30,
    "SpeciesDropoffAge": 50,
    "TournamentSize": 4,
    "YoungAgeTreshold": 5,
}
