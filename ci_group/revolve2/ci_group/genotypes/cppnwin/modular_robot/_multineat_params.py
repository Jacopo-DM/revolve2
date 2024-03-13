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

    MadeBreaker: ClassVar[dict[str, float | int | bool]] = {
        "PopulationSize": 300,
        "DynamicCompatibility": True,
        "MinSpecies": 5,
        "MaxSpecies": 10,
        "InnovationsForever": True,
        "AllowClones": True,
        "ArchiveEnforcement": False,
        "NormalizeGenomeSize": True,
        "DontUseBiasNeuron": False,
        "AllowLoops": True,
        "YoungAgeTreshold": 5,
        "YoungAgeFitnessBoost": 1.1,
        "SpeciesMaxStagnation": 50,
        "StagnationDelta": 0.0,
        "OldAgeTreshold": 30,
        "OldAgePenalty": 0.5,
        "DetectCompetetiveCoevolutionStagnation": False,
        "KillWorstSpeciesEach": 15,
        "KillWorstAge": 10,
        "SurvivalRate": 0.25,
        "CrossoverRate": 0.7,
        "OverallMutationRate": 0.25,
        "InterspeciesCrossoverRate": 0.0001,
        "MultipointCrossoverRate": 0.75,
        "RouletteWheelSelection": False,
        "TournamentSize": 4,
        "EliteFraction": 0.01,
        "NeuronRecursionLimit": 16384,
        "PhasedSearching": False,
        "DeltaCoding": False,
        "SimplifyingPhaseMPCTreshold": 20,
        "SimplifyingPhaseStagnationTreshold": 30,
        "ComplexityFloorGenerations": 40,
        "NoveltySearch_K": 15,
        "NoveltySearch_P_min": 0.5,
        "NoveltySearch_Dynamic_Pmin": True,
        "NoveltySearch_No_Archiving_Stagnation_Treshold": 150,
        "NoveltySearch_Pmin_lowering_multiplier": 0.9,
        "NoveltySearch_Pmin_min": 0.05,
        "NoveltySearch_Quick_Archiving_Min_Evaluations": 8,
        "NoveltySearch_Pmin_raising_multiplier": 1.1,
        "NoveltySearch_Recompute_Sparseness_Each": 25,
        "MutateAddNeuronProb": 0.01,
        "SplitRecurrent": True,
        "SplitLoopedRecurrent": True,
        # "NeuronTries": 64,
        "MutateAddLinkProb": 0.03,
        "MutateAddLinkFromBiasProb": 0.0,
        "MutateRemLinkProb": 0.0,
        "MutateRemSimpleNeuronProb": 0.0,
        "LinkTries": 32,
        "RecurrentProb": 0.25,
        "RecurrentLoopProb": 0.25,
        "MutateWeightsProb": 0.90,
        "MutateWeightsSevereProb": 0.25,
        "WeightMutationRate": 1.0,
        "WeightReplacementRate": 0.2,
        "WeightMutationMaxPower": 1.0,
        "WeightReplacementMaxPower": 1.0,
        "MaxWeight": 8.0,
        "MutateActivationAProb": 0.0,
        "MutateActivationBProb": 0.0,
        "ActivationAMutationMaxPower": 0.0,
        "ActivationBMutationMaxPower": 0.0,
        "TimeConstantMutationMaxPower": 0.0,
        "BiasMutationMaxPower": 1.0,  # = WeightMutationMaxPower
        "MinActivationA": 1.0,
        "MaxActivationA": 1.0,
        "MinActivationB": 0.0,
        "MaxActivationB": 0.0,
        "MutateNeuronActivationTypeProb": 0.0,
        "MutateOutputActivationFunction": False,
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
        # "ActivationFunction_Relu_Prob": 0.0,
        # "ActivationFunction_Softplus_Prob": 0.0,
        "MutateNeuronTimeConstantsProb": 0.0,
        "MutateNeuronBiasesProb": 0.0,
        "MinNeuronTimeConstant": 0.0,
        "MaxNeuronTimeConstant": 0.0,
        "MinNeuronBias": 0.0,
        "MaxNeuronBias": 0.0,
        # "NeuronTraits": None,
        # "LinkTraits": None,
        # "GenomeTraits": None,
        "MutateNeuronTraitsProb": 1.0,
        "MutateLinkTraitsProb": 1.0,
        "MutateGenomeTraitsProb": 1.0,
        "DisjointCoeff": 1.0,
        "ExcessCoeff": 1.0,
        "ActivationADiffCoeff": 0.0,
        "ActivationBDiffCoeff": 0.0,
        "WeightDiffCoeff": 0.5,
        "TimeConstantDiffCoeff": 0.0,
        "BiasDiffCoeff": 0.0,
        "ActivationFunctionDiffCoeff": 0.0,
        "CompatTreshold": 5.0,
        "MinCompatTreshold": 0.2,
        "CompatTresholdModifier": 0.3,
        "CompatTreshChangeInterval_Generations": 1,
        "CompatTreshChangeInterval_Evaluations": 10,
        "DivisionThreshold": 0.03,
        "VarianceThreshold": 0.03,
        "BandThreshold": 0.3,
        "InitialDepth": 3,
        "MaxDepth": 3,
        "IterationLevel": 1,
        "CPPN_Bias": 1.0,
        "Width": 2.0,
        "Height": 2.0,
        "Qtree_X": 0.0,
        "Qtree_Y": 0.0,
        "Leo": False,
        "LeoThreshold": 0.1,
        "LeoSeed": False,
        "GeometrySeed": False,
    }

    ball_keeper: ClassVar[dict[str, float | int | bool]] = {}
    NoveltySearch: ClassVar[dict[str, float | int | bool]] = {}
    TestTraits: ClassVar[dict[str, float | int | bool]] = {}
    TestCondTraits: ClassVar[dict[str, float | int | bool]] = {}
    TestNEAT_xor: ClassVar[dict[str, float | int | bool]] = {}
    TestHyperNEAT_xor: ClassVar[dict[str, float | int | bool]] = {}
    TestESHyperNEAT_xor: ClassVar[dict[str, float | int | bool]] = {}
    TestESHyperNEAT_xor_3d: ClassVar[dict[str, float | int | bool]] = {}

    __inject_override__: ClassVar[dict[str, float | int | bool]] = {
        # NOTE - These field-values are enforced in every case
        "PhasedSearching": True,  # def: False
        "DeltaCoding": True,  # def: False
        "MutateOutputActivationFunction": False,
    }

    __rejection__: ClassVar[dict[str, str | None]] = {
        # NOTE - These fields are not allowed, use the following instead
        "Elitism": "EliteFraction",
        "SpeciesMaxStagnation": "SpeciesDropoffAge",
        "IterationLevel": None,
        "MutateGenomeTraitsProb": None,
    }

    __seg_fault_prone__: frozenset = frozenset(
        [
            # TODO Verify which of these are seg-fault prone
            "Default",
            "GenericOld",
            "ball_keeper",
            "NoveltySearch",
            "TestTraits",
            "TestCondTraits",
            "TestNEAT_xor",
            "TestHyperNEAT_xor",
            "TestESHyperNEAT_xor",
            "TestESHyperNEAT_xor_3d",
        ]
    )

    def _set_params(self, source: dict) -> multiNEATParamType:
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

    def _clean_source(self, params_list: list):
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
            for key in params_list
            if key not in ignore_fields and not key.startswith("_")
        ]

    def _extract_source(self, source: dict):
        # Check if source has reject fields
        for old_key, new_key in self.__rejection__.items():
            if old_key in source:
                value = source.pop(old_key)
                if new_key is not None:
                    source[new_key] = value

        # Extract params
        params = self._set_params(source)

        # Extract dictionary
        params_list = params.__dir__()

        # Get clean sources
        clean_source_keys = self._clean_source(params_list)

        # Get values
        return {key: getattr(params, key) for key in clean_source_keys}

    def _diff_source_vals(self, source_1: dict, source_2: dict):
        # Get values
        clean_source_1 = self._extract_source(source_1)
        clean_source_2 = self._extract_source(source_2)

        # Get differences
        return {
            key_1: [value_1, clean_source_2[key_1]]
            for key_1, value_1 in clean_source_1.items()
        }

    def _print_diff(self, differences: dict, mode: str = "diff"):
        sys.stdout.write("\n")
        allowed_modes = {"all", "same", "diff"}
        for key, (new_value, old_value) in differences.items():
            are_same = new_value == old_value
            if are_same and mode in {"all", "same"}:
                self.__print_diff_generic__(key, old_value, " == ", new_value)
            elif not are_same and mode in {"all", "diff"}:
                self.__print_diff_generic__(key, old_value, " -> ", new_value)
            elif mode not in allowed_modes:
                raise ValueError(f"Invalid mode: {mode}")

    def __print_diff_generic__(self, key, old_value, symbol, new_value):
        sys.stdout.write(f"{key}\n")
        sys.stdout.write(f"\t{old_value}{symbol}{new_value}\n")
        sys.stdout.write("\n")

    def _print_diff_dict(
        self,
        differences: dict,
        name: str,
        ref: str = "def:",
        mode: str = "diff",
    ):
        sys.stdout.write("\n")
        allowed_modes = {"all", "same", "diff"}

        indent = " " * 4
        sys.stdout.write(
            f"\n{indent}{name}: ClassVar[dict[str, float | int | bool]]"
            + " = {\n"
        )

        for key, (new_value, old_value) in differences.items():
            are_same = new_value == old_value
            if are_same and mode in {"all", "same"}:
                self.__print_diff_dict__(key, new_value)
            elif not are_same and mode in {"all", "diff"}:
                self.__print_diff_dict__(
                    key, new_value, f"  # {ref} ", old_value
                )
            elif mode not in allowed_modes:
                raise ValueError(f"Invalid mode: {mode}")
        sys.stdout.write(f"{indent}" + "}\n")

    def __print_diff_dict__(self, key, new_value, symbol="", old_value=""):
        indent = " " * 8
        sys.stdout.write(f'{indent}"{key}": {new_value},{symbol}{old_value}\n')


def get_multineat_params(
    source_name: str = "GenericOld",
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
    target_name = "GenericOld"
    target = getattr(collection_obj, target_name)
    default = collection_obj.Default
    diff = collection_obj._diff_source_vals(target, default)
    collection_obj._print_diff(diff)
    collection_obj._print_diff_dict(diff, target_name)
