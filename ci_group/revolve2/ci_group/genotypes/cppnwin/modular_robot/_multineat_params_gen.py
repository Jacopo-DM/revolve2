import sys
from dataclasses import dataclass

import multineat


@dataclass
class DefaultGenome:
    # Basic Parameters
    PopulationSize: int
    Speciation: bool
    DynamicCompatibility: bool
    MinSpecies: int
    MaxSpecies: int
    InnovationsForever: bool
    AllowClones: bool
    ArchiveEnforcement: bool
    NormalizeGenomeSize: bool

    # GA Parameters
    YoungAgeTreshold: int
    YoungAgeFitnessBoost: float
    SpeciesMaxStagnation: int
    StagnationDelta: float
    OldAgeTreshold: int
    OldAgePenalty: float
    DetectCompetetiveCoevolutionStagnation: bool
    KillWorstSpeciesEach: int
    KillWorstAge: int
    SurvivalRate: float
    CrossoverRate: float
    OverallMutationRate: float
    InterspeciesCrossoverRate: float
    MultipointCrossoverRate: float
    PreferFitterParentRate: float
    SelectionScheme: int
    RouletteWheelSelection: bool
    TournamentSize: int
    EliteFraction: float

    # Phased Search Parameters
    PhasedSearching: bool
    DeltaCoding: bool
    SimplifyingPhaseMPCTreshold: int
    SimplifyingPhaseStagnationTreshold: int
    ComplexityFloorGenerations: int

    # Novelty Search Parameters
    NoveltySearch_K: int
    NoveltySearch_P_min: float
    NoveltySearch_Dynamic_Pmin: bool
    NoveltySearch_No_Archiving_Stagnation_Treshold: int
    NoveltySearch_Pmin_lowering_multiplier: float
    NoveltySearch_Pmin_min: float
    NoveltySearch_Quick_Archiving_Min_Evaluations: int
    NoveltySearch_Pmin_raising_multiplier: float
    NoveltySearch_Recompute_Sparseness_Each: int

    # Mutation Parameters
    MutateAddNeuronProb: float
    SplitRecurrent: bool
    SplitLoopedRecurrent: bool
    NeuronTries: int
    MutateAddLinkProb: float
    MutateAddLinkFromBiasProb: float
    MutateRemLinkProb: float
    MutateRemSimpleNeuronProb: float
    LinkTries: int
    MaxLinks: int
    MaxNeurons: int
    RecurrentProb: float
    RecurrentLoopProb: float
    MutateWeightsProb: float
    MutateWeightsSevereProb: float
    WeightMutationRate: float
    WeightReplacementRate: float
    WeightMutationMaxPower: float
    WeightReplacementMaxPower: float
    MaxWeight: float
    MinWeight: float
    MutateActivationAProb: float
    MutateActivationBProb: float
    ActivationAMutationMaxPower: float
    ActivationBMutationMaxPower: float
    TimeConstantMutationMaxPower: float
    BiasMutationMaxPower: float
    MinActivationA: float
    MaxActivationA: float
    MinActivationB: float
    MaxActivationB: float
    MutateNeuronActivationTypeProb: float
    ActivationFunction_SignedSigmoid_Prob: float
    ActivationFunction_UnsignedSigmoid_Prob: float
    ActivationFunction_UnsignedSigmoid_Prob: float
    ActivationFunction_Tanh_Prob: float
    ActivationFunction_TanhCubic_Prob: float
    ActivationFunction_SignedStep_Prob: float
    ActivationFunction_UnsignedStep_Prob: float
    ActivationFunction_SignedGauss_Prob: float
    ActivationFunction_UnsignedGauss_Prob: float
    ActivationFunction_Abs_Prob: float
    ActivationFunction_SignedSine_Prob: float
    ActivationFunction_UnsignedSine_Prob: float
    ActivationFunction_Linear_Prob: float
    ActivationFunction_Relu_Prob: float
    ActivationFunction_Softplus_Prob: float
    MutateNeuronTimeConstantsProb: float
    MutateNeuronBiasesProb: float
    MinNeuronTimeConstant: float
    MaxNeuronTimeConstant: float
    MinNeuronBias: float
    MaxNeuronBias: float

    # Speciation Parameters
    DisjointCoeff: float
    ExcessCoeff: float
    ActivationADiffCoeff: float
    ActivationBDiffCoeff: float
    WeightDiffCoeff: float
    TimeConstantDiffCoeff: float
    BiasDiffCoeff: float
    ActivationFunctionDiffCoeff: float
    CompatTreshold: float
    MinCompatTreshold: float
    CompatTresholdModifier: float
    CompatTreshChangeInterval_Generations: int
    CompatTreshChangeInterval_Evaluations: int
    MinDeltaCompatEqualGenomes: float
    ConstraintTrials: int

    # Genome Properties Params
    DontUseBiasNeuron: bool
    AllowLoops: bool

    # ES HyperNEAT Params
    DivisionThreshold: float
    VarianceThreshold: float
    BandThreshold: float
    InitialDepth: int
    MaxDepth: int
    IterationLevel: int
    CPPN_Bias: float
    Width: float
    Height: float
    Qtree_X: float
    Qtree_Y: float
    Leo: bool
    LeoThreshold: float
    LeoSeed: bool
    GeometrySeed: bool

    # Universal Traits
    MutateNeuronTraitsProb: float
    MutateLinkTraitsProb: float
    MutateGenomeTraitsProb: float

    # Hidden Parameters
    MutateOutputActivationFunction: bool
    SpeciesDropoffAge: int
    NeuronRecursionLimit: int

    def __init__(self) -> None:
        self.basic_parameters()
        self.ga_parameters()
        self.phased_search_parameters()
        self.novelty_search_parameters()
        self.mutation_parameters()
        self.activation_functions()
        self.speciation_parameters()
        self.genome_properties_parameters()
        self.es_hyperneat_params()
        self.universal_traits()
        self.hidden_parameters()

    def hidden_parameters(self):
        self.MutateOutputActivationFunction = False
        self.SpeciesDropoffAge = 50
        self.NeuronRecursionLimit = 16384

    def universal_traits(self):
        self.MutateNeuronTraitsProb = 1.0  # 0.0
        self.MutateLinkTraitsProb = 1.0  #  0.0
        self.MutateGenomeTraitsProb = 0.1

    def es_hyperneat_params(self):
        self.DivisionThreshold = 0.03
        self.VarianceThreshold = 0.03
        self.BandThreshold = 0.3
        self.InitialDepth = 3
        self.MaxDepth = 3
        self.IterationLevel = 1
        self.CPPN_Bias = 1.0
        self.Width = 2.0
        self.Height = 2.0
        self.Qtree_X = 0.0
        self.Qtree_Y = 0.0
        self.Leo = False
        self.LeoThreshold = 0.1
        self.LeoSeed = False
        self.GeometrySeed = False

    def genome_properties_parameters(self):
        self.DontUseBiasNeuron = False
        self.AllowLoops = False  # <- True

    def speciation_parameters(self):
        self.DisjointCoeff = 1.0
        self.ExcessCoeff = 1.0
        self.ActivationADiffCoeff = 0.0
        self.ActivationBDiffCoeff = 0.0
        self.WeightDiffCoeff = 0.5
        self.TimeConstantDiffCoeff = 0.0
        self.BiasDiffCoeff = 0.0
        self.ActivationFunctionDiffCoeff = 0.0
        self.CompatTreshold = 5.0
        self.MinCompatTreshold = 0.2
        self.CompatTresholdModifier = 0.3
        self.CompatTreshChangeInterval_Generations = 1
        self.CompatTreshChangeInterval_Evaluations = 10
        self.MinDeltaCompatEqualGenomes = 0.1
        self.ConstraintTrials = 128

    def mutation_parameters(self):
        self.MutateAddNeuronProb = 0.01
        self.SplitRecurrent = True
        self.SplitLoopedRecurrent = True
        self.NeuronTries = 64
        self.MutateAddLinkProb = 0.03  # 0.08
        self.MutateAddLinkFromBiasProb = 0.0
        self.MutateRemLinkProb = 0.0  # 0.02
        self.MutateRemSimpleNeuronProb = 0.0
        self.LinkTries = 32
        self.MaxLinks = 64
        self.MaxNeurons = 64
        self.RecurrentProb = 0.0  # <- 0.25
        self.RecurrentLoopProb = 0.0
        self.MutateWeightsProb = 0.9
        self.MutateWeightsSevereProb = 0.25
        self.WeightMutationRate = 1.0
        self.WeightReplacementRate = 0.2
        self.WeightMutationMaxPower = 1.0  # 0.2
        self.WeightReplacementMaxPower = 1.0
        self.MaxWeight = 8.0
        self.MinWeight = -8.0
        self.MutateActivationAProb = 0.0
        self.MutateActivationBProb = 0.0
        self.ActivationAMutationMaxPower = 0.0  # 0.5
        self.ActivationBMutationMaxPower = 0.0
        self.TimeConstantMutationMaxPower = 0.0
        self.BiasMutationMaxPower = 1.0
        self.MinActivationA = 1.0  # 0.05
        self.MaxActivationA = 1.0  # 6.0
        self.MinActivationB = 0.0
        self.MaxActivationB = 0.0
        self.MutateNeuronActivationTypeProb = 0.0  # 0.03
        self.MutateNeuronTimeConstantsProb = 0.0
        self.MutateNeuronBiasesProb = 0.0
        self.MinNeuronTimeConstant = 0.0
        self.MaxNeuronTimeConstant = 0.0
        self.MinNeuronBias = 0.0
        self.MaxNeuronBias = 0.0

    def activation_functions(self):
        self.ActivationFunction_SignedSigmoid_Prob = 0.0
        self.ActivationFunction_UnsignedSigmoid_Prob = 1.0  # 0.0
        self.ActivationFunction_Tanh_Prob = 0.0  # 1.0
        self.ActivationFunction_TanhCubic_Prob = 0.0
        self.ActivationFunction_SignedStep_Prob = 0.0  # 1.0
        self.ActivationFunction_UnsignedStep_Prob = 0.0
        self.ActivationFunction_SignedGauss_Prob = 0.0  # 1.0
        self.ActivationFunction_UnsignedGauss_Prob = 0.0
        self.ActivationFunction_Abs_Prob = 0.0
        self.ActivationFunction_SignedSine_Prob = 0.0  # 1.0
        self.ActivationFunction_UnsignedSine_Prob = 0.0
        self.ActivationFunction_Linear_Prob = 0.0  # 1.0
        self.ActivationFunction_Relu_Prob = 0.0
        self.ActivationFunction_Softplus_Prob = 0.0

    def novelty_search_parameters(self):
        self.NoveltySearch_K = 15
        self.NoveltySearch_P_min = 0.5
        self.NoveltySearch_Dynamic_Pmin = True
        self.NoveltySearch_No_Archiving_Stagnation_Treshold = 150
        self.NoveltySearch_Pmin_lowering_multiplier = 0.9
        self.NoveltySearch_Pmin_min = 0.05
        self.NoveltySearch_Quick_Archiving_Min_Evaluations = 8
        self.NoveltySearch_Pmin_raising_multiplier = 1.1
        self.NoveltySearch_Recompute_Sparseness_Each = 25

    def phased_search_parameters(self):
        self.PhasedSearching = False
        self.DeltaCoding = False
        self.SimplifyingPhaseMPCTreshold = 20
        self.SimplifyingPhaseStagnationTreshold = 30
        self.ComplexityFloorGenerations = 40

    def ga_parameters(self):
        self.YoungAgeTreshold = 5
        self.YoungAgeFitnessBoost = 1.1  # >= 1.0
        self.SpeciesMaxStagnation = 15
        self.StagnationDelta = 0.01  # <- 0.0, 0.0 == NEAT
        self.OldAgeTreshold = 30
        self.OldAgePenalty = 0.5  # < 1.0
        self.DetectCompetetiveCoevolutionStagnation = True  # <- False
        self.KillWorstSpeciesEach = 15
        self.KillWorstAge = 10
        self.SurvivalRate = 0.25
        self.CrossoverRate = 0.75  # <- 0.7
        self.OverallMutationRate = 0.25  # <- 0.0, 0.15
        self.InterspeciesCrossoverRate = 0.01  # <- 0.0001
        self.MultipointCrossoverRate = 0.75
        self.PreferFitterParentRate = 0.6
        self.SelectionScheme = 2
        self.RouletteWheelSelection = False
        self.TournamentSize = 5  # <- 4
        self.EliteFraction = 0.05  # <- 0.01

    def basic_parameters(self):
        self.PopulationSize = 300
        self.Speciation = True
        self.DynamicCompatibility = True
        self.MinSpecies = 5
        self.MaxSpecies = 10
        self.InnovationsForever = True
        self.AllowClones = True
        self.ArchiveEnforcement = False
        self.NormalizeGenomeSize = True

    def gen_multineat_params(self):
        # Create the parameters
        multineat_params = multineat.Parameters()

        # Ignore fields
        ignore_fields = {
            "Reset",
            "Load",
            "Save",
            "ListNeuronTraitParameters",
            "ListLinkTraitParameters",
            "ListGenomeTraitParameters",
            "SetNeuronTraitParameters",
            "SetLinkTraitParameters",
            "SetGenomeTraitParameters",
            "GetNeuronTraitParameters",
            "GetLinkTraitParameters",
            "GetGenomeTraitParameters",
            "ClearNeuronTraitParameters",
            "ClearLinkTraitParameters",
            "ClearGenomeTraitParameters",
            "CustomConstraints",
        }

        # Remove unwanted fields
        param_keys = set(multineat_params.__dir__())
        param_keys = [key for key in param_keys if "__" not in key]
        param_keys = [key for key in param_keys if key not in ignore_fields]

        # Set the parameters
        for key in param_keys:
            sys.stdout.write(f"    {key} = {getattr(self, key)}\n")
        sys.stdout.write("\n")

        # Get diff
        for key in param_keys:
            old_param = getattr(multineat_params, key)
            new_param = getattr(self, key)
            if old_param != new_param:
                sys.stdout.write(f"{key}: {old_param} -> {new_param}\n")


if __name__ == "__main__":
    DefaultGenome().gen_multineat_params()
