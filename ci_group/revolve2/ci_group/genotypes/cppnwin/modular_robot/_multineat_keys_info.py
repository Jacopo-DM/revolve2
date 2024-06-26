"""Module contains the keys that are safe to be used in the MultiNEAT configuration file."""

SAFE_KEYS: set[str] = {
    "ActivationADiffCoeff",
    "ActivationAMutationMaxPower",
    "ActivationBDiffCoeff",
    "ActivationBMutationMaxPower",
    "ActivationFunctionDiffCoeff",
    "ActivationFunction_Abs_Prob",
    "ActivationFunction_Linear_Prob",
    "ActivationFunction_SignedGauss_Prob",
    "ActivationFunction_SignedSigmoid_Prob",
    "ActivationFunction_SignedSine_Prob",
    "ActivationFunction_SignedStep_Prob",
    "ActivationFunction_TanhCubic_Prob",
    "ActivationFunction_Tanh_Prob",
    "ActivationFunction_UnsignedGauss_Prob",
    "ActivationFunction_UnsignedSigmoid_Prob",
    "ActivationFunction_UnsignedSine_Prob",
    "ActivationFunction_UnsignedStep_Prob",
    "AllowClones",
    "AllowLoops",
    "ArchiveEnforcement",
    "BandThreshold",
    "BiasDiffCoeff",
    "BiasMutationMaxPower",
    "CPPN_Bias",
    "ClearLinkTraitParameters",
    "CompatTreshChangeInterval_Evaluations",
    "CompatTreshChangeInterval_Generations",
    "CompatTreshold",
    "CompatTresholdModifier",
    "ComplexityFloorGenerations",
    "CrossoverRate",
    "DeltaCoding",
    "DetectCompetetiveCoevolutionStagnation",
    "DisjointCoeff",
    "DivisionThreshold",
    "DontUseBiasNeuron",
    "DynamicCompatibility",
    "EliteFraction",
    "ExcessCoeff",
    "GeometrySeed",
    "GetLinkTraitParameters",
    "Height",
    "InitialDepth",
    "InnovationsForever",
    "InterspeciesCrossoverRate",
    "KillWorstAge",
    "KillWorstSpeciesEach",
    "Leo",
    "LeoSeed",
    "LeoThreshold",
    "LinkTries",
    "ListLinkTraitParameters",
    "Load",
    "MaxActivationA",
    "MaxActivationB",
    "MaxDepth",
    "MaxNeuronBias",
    "MaxNeuronTimeConstant",
    "MaxSpecies",
    "MaxWeight",
    "MinActivationA",
    "MinActivationB",
    "MinCompatTreshold",
    "MinNeuronBias",
    "MinNeuronTimeConstant",
    "MinSpecies",
    "MultipointCrossoverRate",
    "MutateActivationAProb",
    "MutateActivationBProb",
    "MutateAddLinkFromBiasProb",
    "MutateAddLinkProb",
    "MutateAddNeuronProb",
    "MutateLinkTraitsProb",
    "MutateNeuronActivationTypeProb",
    "MutateNeuronBiasesProb",
    "MutateNeuronTimeConstantsProb",
    "MutateNeuronTraitsProb",
    "MutateOutputActivationFunction",
    "MutateRemLinkProb",
    "MutateRemSimpleNeuronProb",
    "MutateWeightsProb",
    "MutateWeightsSevereProb",
    "NeuronRecursionLimit",
    "NormalizeGenomeSize",
    "NoveltySearch_Dynamic_Pmin",
    "NoveltySearch_K",
    "NoveltySearch_No_Archiving_Stagnation_Treshold",
    "NoveltySearch_P_min",
    "NoveltySearch_Pmin_lowering_multiplier",
    "NoveltySearch_Pmin_min",
    "NoveltySearch_Pmin_raising_multiplier",
    "NoveltySearch_Quick_Archiving_Min_Evaluations",
    "NoveltySearch_Recompute_Sparseness_Each",
    "OldAgePenalty",
    "OldAgeTreshold",
    "OverallMutationRate",
    "PhasedSearching",
    "PopulationSize",
    "Qtree_X",
    "Qtree_Y",
    "RecurrentLoopProb",
    "RecurrentProb",
    "RouletteWheelSelection",
    "SetGenomeTraitParameters",
    "SetNeuronTraitParameters",
    "SimplifyingPhaseMPCTreshold",
    "SimplifyingPhaseStagnationTreshold",
    "SpeciesDropoffAge",
    "SplitLoopedRecurrent",
    "SplitRecurrent",
    "StagnationDelta",
    "SurvivalRate",
    "TimeConstantDiffCoeff",
    "TimeConstantMutationMaxPower",
    "TournamentSize",
    "VarianceThreshold",
    "WeightDiffCoeff",
    "WeightMutationMaxPower",
    "WeightMutationRate",
    "WeightReplacementMaxPower",
    "WeightReplacementRate",
    "Width",
    "YoungAgeFitnessBoost",
    "YoungAgeTreshold",
}

UNSAFE_KEYS: set[str] = {
    "__class__",
    "__delattr__",
    "__dir__",
    "__doc__",
    "__eq__",
    "__format__",
    "__ge__",
    "__getattribute__",
    "__getstate__",
    "__gt__",
    "__hash__",
    "__init__",
    "__init_subclass__",
    "__le__",
    "__lt__",
    "__module__",
    "__ne__",
    "__new__",
    "__reduce__",
    "__reduce_ex__",
    "__repr__",
    "__setattr__",
    "__setstate__",
    "__sizeof__",
    "__str__",
    "__subclasshook__",
    "ClearGenomeTraitParameters",
    "ClearNeuronTraitParameters",
    "CustomConstraints",
    "GetGenomeTraitParameters",
    "GetNeuronTraitParameters",
    "ListGenomeTraitParameters",
    "ListNeuronTraitParameters",
    "Reset",
    "Save",
    "SetLinkTraitParameters",
}
