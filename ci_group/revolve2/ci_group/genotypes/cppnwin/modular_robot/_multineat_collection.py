from dataclasses import dataclass
from typing import ClassVar


@dataclass
class CollectionOfDefaultValues:
    """Collection of default values for MultiNEAT parameters."""

    __all__ = (
        "Empty",
        "GenericOld",
        "gym_lunar_lander",
        "gym_pole_balancing",
        "gym_swing",
        "gym_walker",
        "PythonObjectTraits",
        "ball_keeper",
        "NoveltySearch",
        "TestCondTraits",
        "TestESHyperNEAT_xor_3d",
        "TestHyperNEAT_xor",
        "TestNEAT_xor",
        "TestTraits",
    )

    __seg_fault_prone__: frozenset[str] = frozenset([
        # [ ] Verify which of value dicts cause seg-faults
    ])

    MadeBreaker: ClassVar[dict[str, float | int | bool]] = {
        # [ ] Complete experimentation around seg-faulting
    }

    DefaultConfig: ClassVar[dict[str, float | int | bool]] = {
        # [ ] Transfer values from examples/DefaultConfig.NEAT
    }

    Empty: ClassVar[dict[str, float | int | bool]] = {}

    Jacked: ClassVar[dict[str, float | int | bool]] = {
        # ---
        "AllowClones": False,  # -> True
        "DetectCompetetiveCoevolutionStagnation": True,  # -> False
        "DontUseBiasNeuron": True,  # -> False
        "RouletteWheelSelection": True,  # -> False
        # ---
        "DynamicCompatibility": True,
        "InnovationsForever": True,
        "NormalizeGenomeSize": True,  # -> True
        "NoveltySearch_Dynamic_Pmin": True,
        "SplitLoopedRecurrent": True,
        "SplitRecurrent": False,
        # ---
        # "MutateActivationAProb": 0.01,  # -> 0.0
        # "MutateActivationBProb": 0.005,  # -> 0.0
        "MutateNeuronActivationTypeProb": 0.03,  # -> 0.0
        # "ActivationAMutationMaxPower": 0.5,  # -> 0.0
        # "ActivationBMutationMaxPower": 0.25,  # -> 0.0
        # "ActivationFunctionDiffCoeff": 0.15,  # -> 0.0
        # "ActivationADiffCoeff": 0.05,  # -> 0.0
        # "ActivationBDiffCoeff": 0.05,  # -> 0.0
        # "ActivationFunction_Abs_Prob": 0.05,
        # "ActivationFunction_Linear_Prob": 0.05,
        # "ActivationFunction_SignedGauss_Prob": 0.05,
        "ActivationFunction_SignedSigmoid_Prob": 1.0,
        "ActivationFunction_SignedSine_Prob": 0.05,
        "ActivationFunction_SignedStep_Prob": 0.05,
        # "ActivationFunction_TanhCubic_Prob": 0.05,
        "ActivationFunction_Tanh_Prob": 0.1,
        # "ActivationFunction_UnsignedGauss_Prob": 0.01,
        "ActivationFunction_UnsignedSigmoid_Prob": 0.5,
        # "ActivationFunction_UnsignedSine_Prob": 0.01,
        # "ActivationFunction_UnsignedStep_Prob": 0.01,
        # ---
        "BiasMutationMaxPower": 0.5,  # -> 1.0
        "CompatTreshold": 2.0,  # -> 5.0
        "CrossoverRate": 0.5,  # -> 0.7
        "DivisionThreshold": 0.5,  # -> 0.03
        # "EliteFraction": 0.001,  # -> 0.01
        "LeoThreshold": 0.3,  # -> 0.1
        # "MaxActivationA": 6.9,  # -> 1.0
        # "MinActivationA": 1.1,  # -> 1.0
        "MaxNeuronBias": 3.0,  # -> 0.0
        "MinNeuronBias": -3.0,  # -> 0.0
        "MaxNeuronTimeConstant": 0.24,  # -> 0.0
        "MinNeuronTimeConstant": 0.04,  # -> 0.0
        "MultipointCrossoverRate": 0.4,  # -> 0.75
        "MutateAddLinkProb": 0.02,  # -> 0.03
        "MutateAddNeuronProb": 0.1,  # -> 0.01
        # "MutateLinkTraitsProb": 0.0,  # -> 1.0
        # "MutateNeuronTraitsProb": 0.0,  # -> 1.0
        "MutateRemLinkProb": 0.02,  # -> 0.0
        "TimeConstantMutationMaxPower": 0.1,  # -> 0.0
        # --
        "MaxSpecies": 14,  # -> 10
        "MinSpecies": 7,  # -> 5
        # --
        "OldAgeTreshold": 40,  # -> 30
        "SpeciesDropoffAge": 100,  # -> 50
        "YoungAgeTreshold": 20,  # -> 5
    }

    GenericOld: ClassVar[dict[str, float | int | bool]] = {
        "ActivationFunction_Tanh_Prob": 1.0,  # -> 0.0
        "ActivationFunction_UnsignedSigmoid_Prob": 0.0,  # -> 1.0
        "CompatTresholdModifier": 0.2,  # -> 0.3
        "CrossoverRate": 0.75,  # -> 0.7
        "MutateAddLinkProb": 0.07,  # -> 0.03
        "MutateRemLinkProb": 0.01,  # -> 0.0
        "MutateWeightsProb": 0.75,  # -> 0.9
        "OldAgePenalty": 1.0,  # -> 0.5
        "WeightDiffCoeff": 1.5,  # -> 0.5
        "LinkTries": 128,  # -> 32
    }

    gym_lunar_lander: ClassVar[dict[str, float | int | bool]] = {
        "EliteFraction": 1.0,  # -> 0.01
        "MaxActivationA": 6.0,  # -> 1.0
        "MaxNeuronBias": 8.0,  # -> 0.0
        "MaxNeuronTimeConstant": 0.24,  # -> 0.0
        "MinNeuronBias": -8.0,  # -> 0.0
        "MinNeuronTimeConstant": 0.04,  # -> 0.0
        "MultipointCrossoverRate": 0.4,  # -> 0.75
        "MutateAddLinkProb": 0.2,  # -> 0.03
        "MutateAddNeuronProb": 0.1,  # -> 0.01
        "MutateLinkTraitsProb": 0.0,  # -> 1.0
        "MutateNeuronBiasesProb": 0.1,  # -> 0.0
        "MutateNeuronTimeConstantsProb": 0.1,  # -> 0.0
        "MutateNeuronTraitsProb": 0.0,  # -> 1.0
        "MutateWeightsProb": 0.8,  # -> 0.9
        "MutateWeightsSevereProb": 0.5,  # -> 0.25
        "OverallMutationRate": 0.2,  # -> 0.25
        "SurvivalRate": 0.2,  # -> 0.25
        "TimeConstantMutationMaxPower": 0.1,  # -> 0.0
        "WeightDiffCoeff": 1.0,  # -> 0.5
        "WeightMutationMaxPower": 0.5,  # -> 1.0
        "WeightMutationRate": 0.25,  # -> 1.0
        "MaxSpecies": 4,  # -> 10
        "MinSpecies": 2,  # -> 5
        "OldAgeTreshold": 35,  # -> 30
        "SpeciesDropoffAge": 15,  # -> 50
        "YoungAgeTreshold": 15,  # -> 5
    }

    gym_pole_balancing: ClassVar[dict[str, float | int | bool]] = {
        "AllowClones": False,  # -> True
        "CrossoverRate": 0.5,  # -> 0.7
        "MaxWeight": 20.0,  # -> 8.0
        "MutateAddLinkProb": 0.02,  # -> 0.03
        "MutateLinkTraitsProb": 0.0,  # -> 1.0
        "MutateNeuronTraitsProb": 0.0,  # -> 1.0
        "MutateWeightsSevereProb": 0.01,  # -> 0.25
        "OverallMutationRate": 0.02,  # -> 0.25
        "WeightMutationRate": 0.75,  # -> 1.0
        "WeightReplacementMaxPower": 5.0,  # -> 1.0
        "MinSpecies": 3,  # -> 5
        "OldAgeTreshold": 35,  # -> 30
        "SpeciesDropoffAge": 100,  # -> 50
        "YoungAgeTreshold": 15,  # -> 5
    }

    gym_swing: ClassVar[dict[str, float | int | bool]] = {
        "ActivationFunction_Tanh_Prob": 1.0,  # -> 0.0
        "ActivationFunction_UnsignedSigmoid_Prob": 0.0,  # -> 1.0
        "BiasMutationMaxPower": 0.5,  # -> 1.0
        "CompatTreshold": 2.0,  # -> 5.0
        "CrossoverRate": 0.75,  # -> 0.7
        "MaxActivationA": 6.2,  # -> 1.0
        "MaxNeuronBias": 8.0,  # -> 0.0
        "MaxNeuronTimeConstant": 0.09,  # -> 0.0
        "MinNeuronBias": -8.0,  # -> 0.0
        "MinNeuronTimeConstant": 0.04,  # -> 0.0
        "MultipointCrossoverRate": 0.4,  # -> 0.75
        "MutateAddLinkProb": 0.2,  # -> 0.03
        "MutateAddNeuronProb": 0.1,  # -> 0.01
        "MutateLinkTraitsProb": 0.0,  # -> 1.0
        "MutateNeuronBiasesProb": 0.1,  # -> 0.0
        "MutateNeuronTimeConstantsProb": 0.1,  # -> 0.0
        "MutateNeuronTraitsProb": 0.0,  # -> 1.0
        "MutateWeightsProb": 0.8,  # -> 0.9
        "MutateWeightsSevereProb": 0.15,  # -> 0.25
        "OverallMutationRate": 0.2,  # -> 0.25
        "SurvivalRate": 0.2,  # -> 0.25
        "TimeConstantMutationMaxPower": 0.1,  # -> 0.0
        "WeightDiffCoeff": 1.0,  # -> 0.5
        "WeightMutationMaxPower": 0.5,  # -> 1.0
        "WeightMutationRate": 0.25,  # -> 1.0
        "OldAgeTreshold": 35,  # -> 30
        "SpeciesDropoffAge": 15,  # -> 50
        "YoungAgeTreshold": 15,  # -> 5
    }

    gym_walker: ClassVar[dict[str, float | int | bool]] = {
        "ActivationAMutationMaxPower": 0.5,  # -> 0.0
        "ActivationFunction_Tanh_Prob": 1.0,  # -> 0.0
        "ActivationFunction_UnsignedSigmoid_Prob": 0.0,  # -> 1.0
        "BiasMutationMaxPower": 0.5,  # -> 1.0
        "CompatTreshold": 2.0,  # -> 5.0
        "CrossoverRate": 0.75,  # -> 0.7
        "EliteFraction": 1.0,  # -> 0.01
        "MaxActivationA": 6.9,  # -> 1.0
        "MaxNeuronBias": 8.0,  # -> 0.0
        "MaxNeuronTimeConstant": 0.24,  # -> 0.0
        "MinActivationA": 1.1,  # -> 1.0
        "MinNeuronBias": -8.0,  # -> 0.0
        "MinNeuronTimeConstant": 0.04,  # -> 0.0
        "MultipointCrossoverRate": 0.4,  # -> 0.75
        "MutateAddLinkProb": 0.2,  # -> 0.03
        "MutateAddNeuronProb": 0.1,  # -> 0.01
        "MutateLinkTraitsProb": 0.0,  # -> 1.0
        "MutateNeuronTraitsProb": 0.0,  # -> 1.0
        "MutateWeightsProb": 0.8,  # -> 0.9
        "MutateWeightsSevereProb": 0.5,  # -> 0.25
        "OverallMutationRate": 0.2,  # -> 0.25
        "SurvivalRate": 0.2,  # -> 0.25
        "TimeConstantMutationMaxPower": 0.1,  # -> 0.0
        "WeightDiffCoeff": 1.0,  # -> 0.5
        "WeightMutationMaxPower": 0.5,  # -> 1.0
        "WeightMutationRate": 0.25,  # -> 1.0
        "OldAgeTreshold": 35,  # -> 30
        "SpeciesDropoffAge": 15,  # -> 50
        "YoungAgeTreshold": 15,  # -> 5
    }

    PythonObjectTraits: ClassVar[dict[str, float | int | bool]] = {
        "DynamicCompatibility": False,  # -> True
        "CompatTreshold": 1200000.5,  # -> 5.0
        "CrossoverRate": 0.5,  # -> 0.7
        "DisjointCoeff": 8.0,  # -> 1.0
        "EliteFraction": 1.0,  # -> 0.01
        "ExcessCoeff": 8.0,  # -> 1.0
        "MultipointCrossoverRate": 0.5,  # -> 0.75
        "MutateAddLinkProb": 0.0,  # -> 0.03
        "MutateAddNeuronProb": 0.0,  # -> 0.01
        "MutateLinkTraitsProb": 0.0,  # -> 1.0
        "MutateNeuronTraitsProb": 0.0,  # -> 1.0
        "MutateWeightsProb": 0.0,  # -> 0.9
        "OverallMutationRate": 0.5,  # -> 0.25
        "SurvivalRate": 0.05,  # -> 0.25
        "WeightDiffCoeff": 0.0,  # -> 0.5
        "MinSpecies": 1,  # -> 5
        "OldAgeTreshold": 50,  # -> 30
        "SpeciesDropoffAge": 15,  # -> 50
        "YoungAgeTreshold": 15,  # -> 5
    }

    ball_keeper: ClassVar[dict[str, float | int | bool]] = {
        "AllowClones": False,  # -> True
        "GeometrySeed": True,  # -> False
        "Leo": True,  # -> False
        "LeoSeed": True,  # -> False
        "RouletteWheelSelection": True,  # -> False
        "CPPN_Bias": -3.0,  # -> 1.0
        "CrossoverRate": 0.5,  # -> 0.7
        "DivisionThreshold": 0.5,  # -> 0.03
        "EliteFraction": 0.1,  # -> 0.01
        "Height": 1.0,  # -> 2.0
        "LeoThreshold": 0.3,  # -> 0.1
        "MaxWeight": 20.0,  # -> 8.0
        "MutateAddLinkProb": 0.02,  # -> 0.03
        "MutateLinkTraitsProb": 0.0,  # -> 1.0
        "MutateNeuronTraitsProb": 0.0,  # -> 1.0
        "MutateWeightsSevereProb": 0.01,  # -> 0.25
        "OverallMutationRate": 0.02,  # -> 0.25
        "WeightMutationRate": 0.75,  # -> 1.0
        "WeightReplacementMaxPower": 5.0,  # -> 1.0
        "Width": 1.0,  # -> 2.0
        "MaxDepth": 4,  # -> 3
        "MinSpecies": 3,  # -> 5
        "OldAgeTreshold": 35,  # -> 30
        "SpeciesDropoffAge": 100,  # -> 50
        "YoungAgeTreshold": 15,  # -> 5
    }

    NoveltySearch: ClassVar[dict[str, float | int | bool]] = {
        "AllowClones": False,  # -> True
        "RouletteWheelSelection": True,  # -> False
        "CrossoverRate": 0.5,  # -> 0.7
        "EliteFraction": 0.1,  # -> 0.01
        "MutateAddLinkProb": 0.02,  # -> 0.03
        "MutateLinkTraitsProb": 0.0,  # -> 1.0
        "MutateNeuronTraitsProb": 0.0,  # -> 1.0
        "MutateWeightsSevereProb": 0.01,  # -> 0.25
        "OverallMutationRate": 0.02,  # -> 0.25
        "WeightMutationRate": 0.75,  # -> 1.0
        "WeightReplacementMaxPower": 5.0,  # -> 1.0
        "MinSpecies": 3,  # -> 5
        "OldAgeTreshold": 35,  # -> 30
        "SpeciesDropoffAge": 100,  # -> 50
        "YoungAgeTreshold": 15,  # -> 5
    }

    TestCondTraits: ClassVar[dict[str, float | int | bool]] = {
        "CompatTreshold": 3.0,  # -> 5.0
        "CrossoverRate": 0.75,  # -> 0.7
        "MaxWeight": 0.0,  # -> 8.0
        "MultipointCrossoverRate": 0.4,  # -> 0.75
        "MutateAddLinkProb": 0.01,  # -> 0.03
        "MutateAddNeuronProb": 0.001,  # -> 0.01
        "MutateLinkTraitsProb": 0.8,  # -> 1.0
        "MutateNeuronTraitsProb": 0.8,  # -> 1.0
        "MutateWeightsProb": 0.0,  # -> 0.9
        "MutateWeightsSevereProb": 0.0,  # -> 0.25
        "OverallMutationRate": 0.8,  # -> 0.25
        "SurvivalRate": 0.2,  # -> 0.25
        "WeightDiffCoeff": 0.0,  # -> 0.5
        "WeightMutationMaxPower": 0.0,  # -> 1.0
        "WeightMutationRate": 0.0,  # -> 1.0
        "WeightReplacementMaxPower": 0.0,  # -> 1.0
        "OldAgeTreshold": 35,  # -> 30
        "SpeciesDropoffAge": 15,  # -> 50
        "YoungAgeTreshold": 15,  # -> 5
    }

    TestESHyperNEAT_xor_3d: ClassVar[dict[str, float | int | bool]] = {
        "ActivationFunction_Linear_Prob": 1.0,  # -> 0.0
        "ActivationFunction_SignedGauss_Prob": 1.0,  # -> 0.0
        "ActivationFunction_SignedSine_Prob": 1.0,  # -> 0.0
        "ActivationFunction_SignedStep_Prob": 1.0,  # -> 0.0
        "ActivationFunction_Tanh_Prob": 1.0,  # -> 0.0
        "ActivationFunction_UnsignedSigmoid_Prob": 0.0,  # -> 1.0
        "CPPN_Bias": -1.0,  # -> 1.0
        "CompatTreshold": 2.0,  # -> 5.0
        "DivisionThreshold": 0.5,  # -> 0.03
        "EliteFraction": 0.1,  # -> 0.01
        "Height": 1.0,  # -> 2.0
        "LeoThreshold": 0.3,  # -> 0.1
        "MaxActivationA": 6.0,  # -> 1.0
        "MinActivationA": 0.05,  # -> 1.0
        "MutateAddLinkProb": 0.08,  # -> 0.03
        "MutateLinkTraitsProb": 0.0,  # -> 1.0
        "MutateNeuronActivationTypeProb": 0.03,  # -> 0.0
        "MutateNeuronTraitsProb": 0.0,  # -> 1.0
        "MutateRemLinkProb": 0.02,  # -> 0.0
        "OverallMutationRate": 0.15,  # -> 0.25
        "WeightMutationMaxPower": 0.2,  # -> 1.0
        "Width": 1.0,  # -> 2.0
        "InitialDepth": 2,  # -> 3
        "OldAgeTreshold": 35,  # -> 30
        "SpeciesDropoffAge": 100,  # -> 50
        "YoungAgeTreshold": 15,  # -> 5
    }

    TestHyperNEAT_xor: ClassVar[dict[str, float | int | bool]] = {
        "ActivationAMutationMaxPower": 0.5,  # -> 0.0
        "ActivationFunction_Linear_Prob": 1.0,  # -> 0.0
        "ActivationFunction_SignedGauss_Prob": 1.0,  # -> 0.0
        "ActivationFunction_SignedSine_Prob": 1.0,  # -> 0.0
        "ActivationFunction_SignedStep_Prob": 1.0,  # -> 0.0
        "ActivationFunction_Tanh_Prob": 1.0,  # -> 0.0
        "ActivationFunction_UnsignedSigmoid_Prob": 0.0,  # -> 1.0
        "CompatTreshold": 2.0,  # -> 5.0
        "MaxActivationA": 6.0,  # -> 1.0
        "MinActivationA": 0.05,  # -> 1.0
        "MutateAddLinkProb": 0.08,  # -> 0.03
        "MutateLinkTraitsProb": 0.0,  # -> 1.0
        "MutateNeuronActivationTypeProb": 0.03,  # -> 0.0
        "MutateNeuronTraitsProb": 0.0,  # -> 1.0
        "MutateRemLinkProb": 0.02,  # -> 0.0
        "OverallMutationRate": 0.15,  # -> 0.25
        "WeightMutationMaxPower": 0.2,  # -> 1.0
        "OldAgeTreshold": 35,  # -> 30
        "SpeciesDropoffAge": 100,  # -> 50
        "YoungAgeTreshold": 15,  # -> 5
    }

    TestNEAT_xor: ClassVar[dict[str, float | int | bool]] = {
        "CompatTreshold": 2.0,  # -> 5.0
        "CrossoverRate": 0.0,  # -> 0.7
        "MaxActivationA": 4.9,  # -> 1.0
        "MinActivationA": 4.9,  # -> 1.0
        "MultipointCrossoverRate": 0.0,  # -> 0.75
        "MutateAddLinkProb": 0.3,  # -> 0.03
        "MutateAddNeuronProb": 0.001,  # -> 0.01
        "MutateLinkTraitsProb": 0.0,  # -> 1.0
        "MutateNeuronTraitsProb": 0.0,  # -> 1.0
        "MutateWeightsProb": 0.05,  # -> 0.9
        "MutateWeightsSevereProb": 0.0,  # -> 0.25
        "OverallMutationRate": 1.0,  # -> 0.25
        "SurvivalRate": 0.2,  # -> 0.25
        "WeightDiffCoeff": 0.1,  # -> 0.5
        "WeightMutationMaxPower": 0.5,  # -> 1.0
        "WeightMutationRate": 0.25,  # -> 1.0
        "WeightReplacementMaxPower": 8.0,  # -> 1.0
        "WeightReplacementRate": 0.9,  # -> 0.2
        "MinSpecies": 2,  # -> 5
        "OldAgeTreshold": 35,  # -> 30
        "SpeciesDropoffAge": 15,  # -> 50
        "YoungAgeTreshold": 15,  # -> 5
    }

    TestTraits: ClassVar[dict[str, float | int | bool]] = {
        "CompatTreshold": 3.0,  # -> 5.0
        "CrossoverRate": 0.75,  # -> 0.7
        "MaxWeight": 0.0,  # -> 8.0
        "MultipointCrossoverRate": 0.4,  # -> 0.75
        "MutateAddLinkProb": 0.01,  # -> 0.03
        "MutateAddNeuronProb": 0.001,  # -> 0.01
        "MutateLinkTraitsProb": 0.8,  # -> 1.0
        "MutateNeuronTraitsProb": 0.8,  # -> 1.0
        "MutateWeightsProb": 0.0,  # -> 0.9
        "MutateWeightsSevereProb": 0.0,  # -> 0.25
        "OverallMutationRate": 0.8,  # -> 0.25
        "SurvivalRate": 0.2,  # -> 0.25
        "WeightDiffCoeff": 0.0,  # -> 0.5
        "WeightMutationMaxPower": 0.0,  # -> 1.0
        "WeightMutationRate": 0.0,  # -> 1.0
        "WeightReplacementMaxPower": 0.0,  # -> 1.0
        "OldAgeTreshold": 35,  # -> 30
        "SpeciesDropoffAge": 15,  # -> 50
        "YoungAgeTreshold": 15,  # -> 5
    }
