from multineat._multineat import Parameters


class ParametersClone(Parameters):
    """
    Changed from base:
        CrossoverRate: 0.7 -> 0.75
        EliteFraction: 0.01 -> 0.05
        StagnationDelta: 0.0 -> 0.01
        AllowLoops: True -> False
        RecurrentProb: 0.25 -> 0.0
        InterspeciesCrossoverRate: 0.0001 -> 0.01
        TournamentSize: 4 -> 5
        RecurrentLoopProb: 0.25 -> 0.0
        DetectCompetetiveCoevolutionStagnation: False -> True
    """

    MaxSpecies = 10
    SimplifyingPhaseMPCTreshold = 20
    KillWorstSpeciesEach = 15
    NoveltySearch_Pmin_min = 0.05
    MutateLinkTraitsProb = 1.0
    BiasDiffCoeff = 0.0
    DynamicCompatibility = True
    ActivationFunction_UnsignedStep_Prob = 0.0
    ActivationFunctionDiffCoeff = 0.0
    MutateWeightsSevereProb = 0.25
    InnovationsForever = True
    ComplexityFloorGenerations = 40
    WeightDiffCoeff = 0.5
    ActivationFunction_UnsignedSigmoid_Prob = 1.0
    GeometrySeed = False
    CompatTresholdModifier = 0.3
    SimplifyingPhaseStagnationTreshold = 30
    EliteFraction = 0.05
    ActivationFunction_SignedStep_Prob = 0.0
    MutateRemSimpleNeuronProb = 0.0
    MinActivationA = 1.0
    ActivationFunction_Abs_Prob = 0.0
    ActivationAMutationMaxPower = 0.0
    MinNeuronTimeConstant = 0.0
    MultipointCrossoverRate = 0.75
    MinNeuronBias = 0.0
    NoveltySearch_Pmin_raising_multiplier = 1.1
    MutateNeuronActivationTypeProb = 0.0
    ActivationFunction_TanhCubic_Prob = 0.0
    DisjointCoeff = 1.0
    ActivationADiffCoeff = 0.0
    DeltaCoding = False
    MaxDepth = 3
    InitialDepth = 3
    MutateNeuronTraitsProb = 1.0
    ActivationFunction_SignedGauss_Prob = 0.0
    KillWorstAge = 10
    CompatTreshChangeInterval_Evaluations = 10
    MutateAddNeuronProb = 0.01
    ActivationBDiffCoeff = 0.0
    WeightMutationMaxPower = 1.0
    CompatTreshChangeInterval_Generations = 1
    WeightReplacementRate = 0.2
    MutateAddLinkFromBiasProb = 0.0
    ActivationFunction_SignedSine_Prob = 0.0
    ActivationFunction_UnsignedGauss_Prob = 0.0
    ActivationBMutationMaxPower = 0.0
    StagnationDelta = 0.01
    LinkTries = 32
    CPPN_Bias = 1.0
    MaxActivationA = 1.0
    WeightReplacementMaxPower = 1.0
    PopulationSize = 300
    NormalizeGenomeSize = True
    TimeConstantMutationMaxPower = 0.0
    YoungAgeFitnessBoost = 1.1
    MutateNeuronTimeConstantsProb = 0.0
    ExcessCoeff = 1.0
    AllowClones = True
    NoveltySearch_Pmin_lowering_multiplier = 0.9
    InterspeciesCrossoverRate = 0.01
    OverallMutationRate = 0.25
    BandThreshold = 0.3
    LeoThreshold = 0.1
    ActivationFunction_Tanh_Prob = 0.0
    TimeConstantDiffCoeff = 0.0
    MaxNeuronTimeConstant = 0.0
    MaxActivationB = 0.0
    MutateOutputActivationFunction = False
    DetectCompetetiveCoevolutionStagnation = True
    WeightMutationRate = 1.0
    ActivationFunction_SignedSigmoid_Prob = 0.0
    NoveltySearch_Dynamic_Pmin = True
    MinCompatTreshold = 0.2
    VarianceThreshold = 0.03
    DivisionThreshold = 0.03
    SplitRecurrent = True
    NoveltySearch_K = 15
    NoveltySearch_Quick_Archiving_Min_Evaluations = 8
    MinSpecies = 5
    MinActivationB = 0.0
    SplitLoopedRecurrent = True
    SurvivalRate = 0.25
    DontUseBiasNeuron = False
    NoveltySearch_No_Archiving_Stagnation_Treshold = 150
    BiasMutationMaxPower = 1.0
    Leo = False
    AllowLoops = False
    ArchiveEnforcement = False
    NeuronRecursionLimit = 16384
    RecurrentLoopProb = 0.0
    Height = 2.0
    NoveltySearch_P_min = 0.5
    SpeciesDropoffAge = 50
    MutateRemLinkProb = 0.0
    MutateActivationAProb = 0.0
    CompatTreshold = 5.0
    ActivationFunction_UnsignedSine_Prob = 0.0
    Qtree_X = 0.0
    OldAgeTreshold = 30
    CrossoverRate = 0.75
    NoveltySearch_Recompute_Sparseness_Each = 25
    MaxNeuronBias = 0.0
    Qtree_Y = 0.0
    MutateWeightsProb = 0.9
    MutateNeuronBiasesProb = 0.0
    RecurrentProb = 0.0
    Width = 2.0
    MutateActivationBProb = 0.0
    LeoSeed = False
    YoungAgeTreshold = 5
    TournamentSize = 5
    RouletteWheelSelection = False
    PhasedSearching = False
    OldAgePenalty = 0.5
    MutateAddLinkProb = 0.03
    MaxWeight = 8.0
    ActivationFunction_Linear_Prob = 0.0
