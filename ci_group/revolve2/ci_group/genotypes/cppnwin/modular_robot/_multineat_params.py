import faulthandler
import sys
from dataclasses import dataclass
from typing import ClassVar

import multineat
from multineat._multineat import Parameters as multiNEATParamType

# Enable faulthandler to dump tracebacks on segfault.
faulthandler.enable()


@dataclass
class CollectionOfDefaultValues:
    Default: ClassVar[dict[str, float | int | bool]] = {}

    GenericOld: ClassVar[dict[str, float | int | bool]] = {
        "OldAgePenalty": 1.0,  # def: 0.5
        "CrossoverRate": 0.75,  # def: 0.7
        "MutateAddLinkProb": 0.07,  # def: 0.03
        "MutateRemLinkProb": 0.01,  # def: 0.0
        "LinkTries": 128,  # def: 32
        "MutateWeightsProb": 0.75,  # def: 0.9
        "ActivationFunction_UnsignedSigmoid_Prob": 0.0,  # def: 1.0
        "ActivationFunction_Tanh_Prob": 1.0,  # def: 0.0
        "WeightDiffCoeff": 1.5,  # def: 0.5
        "CompatTresholdModifier": 0.2,  # def: 0.3
    }

    gym_lunar_lander: ClassVar[dict[str, float | int | bool]] = {
        "MinSpecies": 2,  # def: 5
        "MaxSpecies": 4,  # def: 10
        "YoungAgeTreshold": 15,  # def: 5
        "SpeciesDropoffAge": 15,  # def: 50
        "OldAgeTreshold": 35,  # def: 30
        "SurvivalRate": 0.2,  # def: 0.25
        "CrossoverRate": 0.75,  # def: 0.7
        "OverallMutationRate": 0.2,  # def: 0.25
        "MultipointCrossoverRate": 0.4,  # def: 0.75
        "MutateAddNeuronProb": 0.1,  # def: 0.01
        "MutateAddLinkProb": 0.2,  # def: 0.03
        "MutateWeightsProb": 0.8,  # def: 0.9
        "MutateWeightsSevereProb": 0.5,  # def: 0.25
        "WeightMutationRate": 0.25,  # def: 1.0
        "WeightMutationMaxPower": 0.5,  # def: 1.0
        "MaxActivationA": 6.0,  # def: 1.0
        "TimeConstantMutationMaxPower": 0.1,  # def: 0.0
        "BiasMutationMaxPower": 0.5,  # def: 1.0
        "MutateNeuronTimeConstantsProb": 0.1,  # def: 0.0
        "MutateNeuronBiasesProb": 0.1,  # def: 0.0
        "MinNeuronTimeConstant": 0.04,  # def: 0.0
        "MaxNeuronTimeConstant": 0.24,  # def: 0.0
        "MinNeuronBias": -8.0,  # def: 0.0
        "MaxNeuronBias": 8.0,  # def: 0.0
        "ActivationFunction_UnsignedSigmoid_Prob": 0.0,  # def: 1.0
        "ActivationFunction_Tanh_Prob": 1.0,  # def: 0.0
        "MutateNeuronTraitsProb": 0.0,  # def: 1.0
        "MutateLinkTraitsProb": 0.0,  # def: 1.0
        "WeightDiffCoeff": 1.0,  # def: 0.5
        "CompatTreshold": 2.0,  # def: 5.0
        "EliteFraction": 1.0,  # def: 0.01
    }

    gym_pole_balancing: ClassVar[dict[str, float | int | bool]] = {
        "MinSpecies": 3,  # def: 5
        "AllowClones": False,  # def: True
        "YoungAgeTreshold": 15,  # def: 5
        "SpeciesDropoffAge": 100,  # def: 50
        "OldAgeTreshold": 35,  # def: 30
        "CrossoverRate": 0.5,  # def: 0.7
        "OverallMutationRate": 0.02,  # def: 0.25
        "MutateAddLinkProb": 0.02,  # def: 0.03
        "MutateWeightsSevereProb": 0.01,  # def: 0.25
        "WeightMutationRate": 0.75,  # def: 1.0
        "WeightReplacementMaxPower": 5.0,  # def: 1.0
        "MaxWeight": 20.0,  # def: 8.0
        "MutateNeuronTraitsProb": 0.0,  # def: 1.0
        "MutateLinkTraitsProb": 0.0,  # def: 1.0
    }

    gym_swing: ClassVar[dict[str, float | int | bool]] = {
        "YoungAgeTreshold": 15,  # def: 5
        "SpeciesDropoffAge": 15,  # def: 50
        "OldAgeTreshold": 35,  # def: 30
        "SurvivalRate": 0.2,  # def: 0.25
        "CrossoverRate": 0.75,  # def: 0.7
        "OverallMutationRate": 0.2,  # def: 0.25
        "MultipointCrossoverRate": 0.4,  # def: 0.75
        "MutateAddNeuronProb": 0.1,  # def: 0.01
        "MutateAddLinkProb": 0.2,  # def: 0.03
        "MutateWeightsProb": 0.8,  # def: 0.9
        "MutateWeightsSevereProb": 0.15,  # def: 0.25
        "WeightMutationRate": 0.25,  # def: 1.0
        "WeightMutationMaxPower": 0.5,  # def: 1.0
        "MaxActivationA": 6.2,  # def: 1.0
        "TimeConstantMutationMaxPower": 0.1,  # def: 0.0
        "BiasMutationMaxPower": 0.5,  # def: 1.0
        "MutateNeuronTimeConstantsProb": 0.1,  # def: 0.0
        "MutateNeuronBiasesProb": 0.1,  # def: 0.0
        "MinNeuronTimeConstant": 0.04,  # def: 0.0
        "MaxNeuronTimeConstant": 0.09,  # def: 0.0
        "MinNeuronBias": -8.0,  # def: 0.0
        "MaxNeuronBias": 8.0,  # def: 0.0
        "ActivationFunction_UnsignedSigmoid_Prob": 0.0,  # def: 1.0
        "ActivationFunction_Tanh_Prob": 1.0,  # def: 0.0
        "MutateNeuronTraitsProb": 0.0,  # def: 1.0
        "MutateLinkTraitsProb": 0.0,  # def: 1.0
        "WeightDiffCoeff": 1.0,  # def: 0.5
        "CompatTreshold": 2.0,  # def: 5.0
    }

    gym_walker: ClassVar[dict[str, float | int | bool]] = {
        "YoungAgeTreshold": 15,  # def: 5
        "SpeciesDropoffAge": 15,  # def: 50
        "OldAgeTreshold": 35,  # def: 30
        "SurvivalRate": 0.2,  # def: 0.25
        "CrossoverRate": 0.75,  # def: 0.7
        "OverallMutationRate": 0.2,  # def: 0.25
        "MultipointCrossoverRate": 0.4,  # def: 0.75
        "MutateAddNeuronProb": 0.1,  # def: 0.01
        "MutateAddLinkProb": 0.2,  # def: 0.03
        "MutateWeightsProb": 0.8,  # def: 0.9
        "MutateWeightsSevereProb": 0.5,  # def: 0.25
        "WeightMutationRate": 0.25,  # def: 1.0
        "WeightMutationMaxPower": 0.5,  # def: 1.0
        "ActivationAMutationMaxPower": 0.5,  # def: 0.0
        "MinActivationA": 1.1,  # def: 1.0
        "MaxActivationA": 6.9,  # def: 1.0
        "TimeConstantMutationMaxPower": 0.1,  # def: 0.0
        "BiasMutationMaxPower": 0.5,  # def: 1.0
        "MinNeuronTimeConstant": 0.04,  # def: 0.0
        "MaxNeuronTimeConstant": 0.24,  # def: 0.0
        "MinNeuronBias": -8.0,  # def: 0.0
        "MaxNeuronBias": 8.0,  # def: 0.0
        "ActivationFunction_UnsignedSigmoid_Prob": 0.0,  # def: 1.0
        "ActivationFunction_Tanh_Prob": 1.0,  # def: 0.0
        "MutateNeuronTraitsProb": 0.0,  # def: 1.0
        "MutateLinkTraitsProb": 0.0,  # def: 1.0
        "WeightDiffCoeff": 1.0,  # def: 0.5
        "CompatTreshold": 2.0,  # def: 5.0
        "EliteFraction": 1.0,  # def: 0.01
    }

    PythonObjectTraits: ClassVar[dict[str, float | int | bool]] = {
        "DynamicCompatibility": False,  # def: True
        "MinSpecies": 1,  # def: 5
        "YoungAgeTreshold": 15,  # def: 5
        "SpeciesDropoffAge": 15,  # def: 50
        "OldAgeTreshold": 50,  # def: 30
        "SurvivalRate": 0.05,  # def: 0.25
        "CrossoverRate": 0.5,  # def: 0.7
        "OverallMutationRate": 0.5,  # def: 0.25
        "MultipointCrossoverRate": 0.5,  # def: 0.75
        "MutateAddNeuronProb": 0.0,  # def: 0.01
        "MutateAddLinkProb": 0.0,  # def: 0.03
        "MutateWeightsProb": 0.0,  # def: 0.9
        "MutateNeuronTraitsProb": 0.0,  # def: 1.0
        "MutateLinkTraitsProb": 0.0,  # def: 1.0
        "DisjointCoeff": 8.0,  # def: 1.0
        "ExcessCoeff": 8.0,  # def: 1.0
        "WeightDiffCoeff": 0.0,  # def: 0.5
        "CompatTreshold": 1200000.5,  # def: 5.0
        "EliteFraction": 1.0,  # def: 0.01
    }

    ball_keeper: ClassVar[dict[str, float | int | bool]] = {
        "MinSpecies": 3,  # def: 5
        "AllowClones": False,  # def: True
        "YoungAgeTreshold": 15,  # def: 5
        "SpeciesDropoffAge": 100,  # def: 50
        "OldAgeTreshold": 35,  # def: 30
        "CrossoverRate": 0.5,  # def: 0.7
        "OverallMutationRate": 0.02,  # def: 0.25
        "RouletteWheelSelection": True,  # def: False
        "MutateAddLinkProb": 0.02,  # def: 0.03
        "MutateWeightsSevereProb": 0.01,  # def: 0.25
        "WeightMutationRate": 0.75,  # def: 1.0
        "WeightReplacementMaxPower": 5.0,  # def: 1.0
        "MaxWeight": 20.0,  # def: 8.0
        "MutateNeuronTraitsProb": 0.0,  # def: 1.0
        "MutateLinkTraitsProb": 0.0,  # def: 1.0
        "DivisionThreshold": 0.5,  # def: 0.03
        "MaxDepth": 4,  # def: 3
        "CPPN_Bias": -3.0,  # def: 1.0
        "Width": 1.0,  # def: 2.0
        "Height": 1.0,  # def: 2.0
        "Leo": True,  # def: False
        "LeoThreshold": 0.3,  # def: 0.1
        "LeoSeed": True,  # def: False
        "GeometrySeed": True,  # def: False
        "EliteFraction": 0.1,  # def: 0.01
    }

    NoveltySearch: ClassVar[dict[str, float | int | bool]] = {
        "MinSpecies": 3,  # def: 5
        "AllowClones": False,  # def: True
        "YoungAgeTreshold": 15,  # def: 5
        "SpeciesDropoffAge": 100,  # def: 50
        "OldAgeTreshold": 35,  # def: 30
        "CrossoverRate": 0.5,  # def: 0.7
        "OverallMutationRate": 0.02,  # def: 0.25
        "RouletteWheelSelection": True,  # def: False
        "MutateAddLinkProb": 0.02,  # def: 0.03
        "MutateWeightsSevereProb": 0.01,  # def: 0.25
        "WeightMutationRate": 0.75,  # def: 1.0
        "WeightReplacementMaxPower": 5.0,  # def: 1.0
        "MutateNeuronTraitsProb": 0.0,  # def: 1.0
        "MutateLinkTraitsProb": 0.0,  # def: 1.0
        "EliteFraction": 0.1,  # def: 0.01
    }

    TestCondTraits: ClassVar[dict[str, float | int | bool]] = {
        "YoungAgeTreshold": 15,  # def: 5
        "SpeciesDropoffAge": 15,  # def: 50
        "OldAgeTreshold": 35,  # def: 30
        "SurvivalRate": 0.2,  # def: 0.25
        "CrossoverRate": 0.75,  # def: 0.7
        "OverallMutationRate": 0.8,  # def: 0.25
        "MultipointCrossoverRate": 0.4,  # def: 0.75
        "MutateAddNeuronProb": 0.001,  # def: 0.01
        "MutateAddLinkProb": 0.01,  # def: 0.03
        "MutateWeightsProb": 0.0,  # def: 0.9
        "MutateWeightsSevereProb": 0.0,  # def: 0.25
        "WeightMutationRate": 0.0,  # def: 1.0
        "WeightMutationMaxPower": 0.0,  # def: 1.0
        "WeightReplacementMaxPower": 0.0,  # def: 1.0
        "MaxWeight": 0.0,  # def: 8.0
        "MutateNeuronTraitsProb": 0.8,  # def: 1.0
        "MutateLinkTraitsProb": 0.8,  # def: 1.0
        "WeightDiffCoeff": 0.0,  # def: 0.5
        "CompatTreshold": 3.0,  # def: 5.0
    }

    TestESHyperNEAT_xor_3d: ClassVar[dict[str, float | int | bool]] = {
        "YoungAgeTreshold": 15,  # def: 5
        "SpeciesDropoffAge": 100,  # def: 50
        "OldAgeTreshold": 35,  # def: 30
        "OverallMutationRate": 0.15,  # def: 0.25
        "MutateAddLinkProb": 0.08,  # def: 0.03
        "MutateRemLinkProb": 0.02,  # def: 0.0
        "WeightMutationMaxPower": 0.2,  # def: 1.0
        "ActivationAMutationMaxPower": 0.5,  # def: 0.0
        "MinActivationA": 0.05,  # def: 1.0
        "MaxActivationA": 6.0,  # def: 1.0
        "MutateNeuronActivationTypeProb": 0.03,  # def: 0.0
        "ActivationFunction_UnsignedSigmoid_Prob": 0.0,  # def: 1.0
        "ActivationFunction_Tanh_Prob": 1.0,  # def: 0.0
        "ActivationFunction_SignedStep_Prob": 1.0,  # def: 0.0
        "ActivationFunction_SignedGauss_Prob": 1.0,  # def: 0.0
        "ActivationFunction_SignedSine_Prob": 1.0,  # def: 0.0
        "ActivationFunction_Linear_Prob": 1.0,  # def: 0.0
        "MutateNeuronTraitsProb": 0.0,  # def: 1.0
        "MutateLinkTraitsProb": 0.0,  # def: 1.0
        "CompatTreshold": 2.0,  # def: 5.0
        "DivisionThreshold": 0.5,  # def: 0.03
        "InitialDepth": 2,  # def: 3
        "CPPN_Bias": -1.0,  # def: 1.0
        "Width": 1.0,  # def: 2.0
        "Height": 1.0,  # def: 2.0
        "LeoThreshold": 0.3,  # def: 0.1
        "EliteFraction": 0.1,  # def: 0.01
    }

    TestHyperNEAT_xor: ClassVar[dict[str, float | int | bool]] = {
        "YoungAgeTreshold": 15,  # def: 5
        "SpeciesDropoffAge": 100,  # def: 50
        "OldAgeTreshold": 35,  # def: 30
        "OverallMutationRate": 0.15,  # def: 0.25
        "MutateAddLinkProb": 0.08,  # def: 0.03
        "MutateRemLinkProb": 0.02,  # def: 0.0
        "WeightMutationMaxPower": 0.2,  # def: 1.0
        "ActivationAMutationMaxPower": 0.5,  # def: 0.0
        "MinActivationA": 0.05,  # def: 1.0
        "MaxActivationA": 6.0,  # def: 1.0
        "MutateNeuronActivationTypeProb": 0.03,  # def: 0.0
        "ActivationFunction_UnsignedSigmoid_Prob": 0.0,  # def: 1.0
        "ActivationFunction_Tanh_Prob": 1.0,  # def: 0.0
        "ActivationFunction_SignedStep_Prob": 1.0,  # def: 0.0
        "ActivationFunction_SignedGauss_Prob": 1.0,  # def: 0.0
        "ActivationFunction_SignedSine_Prob": 1.0,  # def: 0.0
        "ActivationFunction_Linear_Prob": 1.0,  # def: 0.0
        "MutateNeuronTraitsProb": 0.0,  # def: 1.0
        "MutateLinkTraitsProb": 0.0,  # def: 1.0
        "CompatTreshold": 2.0,  # def: 5.0
    }

    TestNEAT_xor: ClassVar[dict[str, float | int | bool]] = {
        "MinSpecies": 2,  # def: 5
        "YoungAgeTreshold": 15,  # def: 5
        "SpeciesDropoffAge": 15,  # def: 50
        "OldAgeTreshold": 35,  # def: 30
        "SurvivalRate": 0.2,  # def: 0.25
        "CrossoverRate": 0.0,  # def: 0.7
        "OverallMutationRate": 1.0,  # def: 0.25
        "MultipointCrossoverRate": 0.0,  # def: 0.75
        "MutateAddNeuronProb": 0.001,  # def: 0.01
        "MutateAddLinkProb": 0.3,  # def: 0.03
        "MutateWeightsProb": 0.05,  # def: 0.9
        "MutateWeightsSevereProb": 0.0,  # def: 0.25
        "WeightMutationRate": 0.25,  # def: 1.0
        "WeightMutationMaxPower": 0.5,  # def: 1.0
        "WeightReplacementRate": 0.9,  # def: 0.2
        "WeightReplacementMaxPower": 8.0,  # def: 1.0
        "MinActivationA": 4.9,  # def: 1.0
        "MaxActivationA": 4.9,  # def: 1.0
        "MutateNeuronTraitsProb": 0.0,  # def: 1.0
        "MutateLinkTraitsProb": 0.0,  # def: 1.0
        "WeightDiffCoeff": 0.1,  # def: 0.5
        "CompatTreshold": 2.0,  # def: 5.0
    }

    TestTraits: ClassVar[dict[str, float | int | bool]] = {
        "YoungAgeTreshold": 15,  # def: 5
        "SpeciesDropoffAge": 15,  # def: 50
        "OldAgeTreshold": 35,  # def: 30
        "SurvivalRate": 0.2,  # def: 0.25
        "CrossoverRate": 0.75,  # def: 0.7
        "OverallMutationRate": 0.8,  # def: 0.25
        "MultipointCrossoverRate": 0.4,  # def: 0.75
        "MutateAddNeuronProb": 0.001,  # def: 0.01
        "MutateAddLinkProb": 0.01,  # def: 0.03
        "MutateWeightsProb": 0.0,  # def: 0.9
        "MutateWeightsSevereProb": 0.0,  # def: 0.25
        "WeightMutationRate": 0.0,  # def: 1.0
        "WeightMutationMaxPower": 0.0,  # def: 1.0
        "WeightReplacementMaxPower": 0.0,  # def: 1.0
        "MaxWeight": 0.0,  # def: 8.0
        "MutateNeuronTraitsProb": 0.8,  # def: 1.0
        "MutateLinkTraitsProb": 0.8,  # def: 1.0
        "WeightDiffCoeff": 0.0,  # def: 0.5
        "CompatTreshold": 3.0,  # def: 5.0
    }

    MadeBreaker: ClassVar[dict[str, float | int | bool]] = {
        # [ ] Complete experimentation around seg-faulting
    }

    DefaultConfig: ClassVar[dict[str, float | int | bool]] = {
        # [ ] Transfer values from examples/DefaultConfig.NEAT
    }

    __seg_fault_prone__: frozenset[str] = frozenset([
        # [ ] Verify which of value dicts cause seg-faults
    ])

    __inject_override__: ClassVar[dict[str, float | int | bool]] = {
        # NOTE - These field-values are enforced in every case
        "PhasedSearching": True,  # def: False
        "DeltaCoding": True,  # def: False
        "MutateOutputActivationFunction": False,
        "PopulationSize": 300,  # def: 150
        # WARN The following parameters seem to be the cause of the seg-fault
        #   └── [ ] To study
        "RecurrentProb": 0,  # def: 0.25,
        "RecurrentLoopProb": 0,  # def: 0.25,
        "AllowLoops": False,  # def: True,
    }

    __rejection__: ClassVar[dict[str, str | None]] = {
        # NOTE - These fields are not allowed, use the following instead
        "Elitism": "EliteFraction",
        "SpeciesMaxStagnation": "SpeciesDropoffAge",
        "IterationLevel": None,
        "MutateGenomeTraitsProb": None,
    }

    def _set_params(
        self, source: dict[str, float | bool]
    ) -> multiNEATParamType:
        # Create the parameters
        params = multineat.Parameters()

        # Load params from dict
        for key, value in source.items():
            setattr(params, key, value)

        # Override parameters
        for key, value in self.__inject_override__.items():
            setattr(params, key, value)

        # Return the parameters
        return params

    def _clean_source(self, params_dict: dict[str, float | bool]) -> list[str]:
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
        return [
            key
            for key in params_dict
            if key not in ignore_fields and not key.startswith("_")
        ]

    def _extract_source(
        self, source: dict[str, float | bool]
    ) -> dict[str, float | bool]:
        # Check if source has reject fields
        for old_key, new_key in self.__rejection__.items():
            if old_key in source:
                value = source.pop(old_key)
                if new_key is not None:
                    source[new_key] = value

        # Extract params
        params = self._set_params(source)

        # Extract dictionary
        params_dict = params.__dir__()

        # Get clean sources
        clean_source_keys = self._clean_source(params_dict)

        # Get values
        return {key: getattr(params, key) for key in clean_source_keys}

    def _diff_source_vals(
        self,
        source_1: dict[str, float | bool],
        source_2: dict[str, float | bool],
    ) -> dict[str, list[float | bool]]:
        # Get values
        clean_source_1 = self._extract_source(source_1)
        clean_source_2 = self._extract_source(source_2)

        # Get differences
        return {
            key_1: [value_1, clean_source_2[key_1]]
            for key_1, value_1 in clean_source_1.items()
        }

    def _print_diff(
        self, differences: dict[str, list[float | bool]], mode: str = "diff"
    ) -> None:
        sys.stdout.write("\n")
        allowed_modes = {"all", "same", "diff"}
        for key, (new_value, old_value) in differences.items():
            are_same = new_value == old_value
            if are_same and mode in {"all", "same"}:
                self.__print_diff_generic__(key, old_value, " == ", new_value)
            elif not are_same and mode in {"all", "diff"}:
                self.__print_diff_generic__(key, old_value, " -> ", new_value)
            elif mode not in allowed_modes:
                msg = f"Invalid mode: {mode}"
                raise ValueError(msg)

    def __print_diff_generic__(
        self,
        key: str,
        old_value: float | int | bool,
        symbol: str,
        new_value: float | int | bool,
    ) -> None:
        sys.stdout.write(f"{key}\n")
        sys.stdout.write(f"\t{old_value}{symbol}{new_value}\n")
        sys.stdout.write("\n")

    def _print_diff_dict(
        self,
        differences: dict[str, list[float | int | bool]],
        name: str,
        ref: str = "def:",
        mode: str = "diff",
    ) -> None:
        sys.stdout.write("\n")
        allowed_modes = {"all", "same", "diff"}

        indent = " " * 4
        sys.stdout.write(
            f"\n{indent}{name}: ClassVar[dict[str, float | int | bool]]"
            + " = {\n"
        )

        for key, value_list in differences.items():
            new_value, old_value = value_list[:1]
            are_same = new_value == old_value
            if are_same and mode in {"all", "same"}:
                self.__print_diff_dict__(key, new_value)
            elif not are_same and mode in {"all", "diff"}:
                self.__print_diff_dict__(
                    key, new_value, f"  # {ref} ", old_value
                )
            elif mode not in allowed_modes:
                msg = f"Invalid mode: {mode}"
                raise ValueError(msg)
        sys.stdout.write(f"{indent}" + "}\n")

    def __print_diff_dict__(
        self,
        key: str,
        new_value: float | int | bool,
        symbol: str = "",
        old_value: str | float | int | bool = "",
    ) -> None:
        indent = " " * 8
        sys.stdout.write(f'{indent}"{key}": {new_value},{symbol}{old_value}\n')


def get_multineat_params(
    source_name: str = "TestESHyperNEAT_xor",
) -> multiNEATParamType:
    # Get source
    def_vals = CollectionOfDefaultValues()
    source = getattr(def_vals, source_name)
    params = def_vals._set_params(source)

    # Return the parameters
    del def_vals, source
    return params


if __name__ == "__main__":
    collection_obj = CollectionOfDefaultValues()
    target_name = "TestTraits"
    target = getattr(collection_obj, target_name)
    default = collection_obj.Default
    diff = collection_obj._diff_source_vals(target, default)
    collection_obj._print_diff(diff)
    collection_obj._print_diff_dict(diff, target_name)
