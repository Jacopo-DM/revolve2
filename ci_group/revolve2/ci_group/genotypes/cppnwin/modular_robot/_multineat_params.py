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
        "ActivationFunction_Tanh_Prob": 1.0,  # def:0.0
        "ActivationFunction_UnsignedSigmoid_Prob": 0.0,  # def:1.0
        "CompatTresholdModifier": 0.2,  # def:0.3
        "CrossoverRate": 0.75,  # def:0.7
        "LinkTries": 128,  # def:32
        "MutateAddLinkProb": 0.07,  # def:0.03
        "MutateRemLinkProb": 0.01,  # def:0.0
        "MutateWeightsProb": 0.75,  # def:0.9
        "OldAgePenalty": 1.0,  # def:0.5
        "WeightDiffCoeff": 1.5,  # def:0.5
    }
    ball_keeper: ClassVar[dict[str, float | int | bool]] = {
        "PopulationSize": 150,
        "DynamicCompatibility": True,
        "AllowClones": False,
        "CompatTreshold": 5.0,
        "CompatTresholdModifier": 0.3,
        "YoungAgeTreshold": 15,
        "SpeciesMaxStagnation": 100,
        "OldAgeTreshold": 35,
        "MinSpecies": 3,
        "MaxSpecies": 10,
        "RouletteWheelSelection": True,
        "RecurrentProb": 0.0,
        "OverallMutationRate": 0.02,
        "MutateWeightsProb": 0.90,
        "WeightMutationMaxPower": 1.0,
        "WeightReplacementMaxPower": 5.0,
        "MutateWeightsSevereProb": 0.5,
        "WeightMutationRate": 0.75,
        "MaxWeight": 20,
        "MutateAddNeuronProb": 0.01,
        "MutateAddLinkProb": 0.02,
        "MutateRemLinkProb": 0.00,
        "DivisionThreshold": 0.5,
        "VarianceThreshold": 0.03,
        "BandThreshold": 0.3,
        "InitialDepth": 3,
        "MaxDepth": 4,
        "IterationLevel": 1,
        "Leo": True,
        "GeometrySeed": True,
        "LeoSeed": True,
        "LeoThreshold": 0.3,
        "CPPN_Bias": -3.0,
        "Qtree_X": 0.0,
        "Qtree_Y": 0.0,
        "Width": 1.0,
        "Height": 1.0,
        "Elitism": 0.1,
        "CrossoverRate": 0.5,
        "MutateWeightsSevereProb": 0.01,
        "MutateNeuronTraitsProb": 0,
        "MutateLinkTraitsProb": 0,
    }
    NoveltySearch: ClassVar[dict[str, float | int | bool]] = {}
    TestTraits: ClassVar[dict[str, float | int | bool]] = {}
    TestCondTraits: ClassVar[dict[str, float | int | bool]] = {}
    TestNEAT_xor: ClassVar[dict[str, float | int | bool]] = {}
    TestHyperNEAT_xor: ClassVar[dict[str, float | int | bool]] = {}
    TestESHyperNEAT_xor: ClassVar[dict[str, float | int | bool]] = {}
    TestESHyperNEAT_xor_3d: ClassVar[dict[str, float | int | bool]] = {}

    __rejection__: ClassVar[dict[str, str | None]] = {
        # NOTE - These fields are not allowed, use the following instead
        "Elitism": "EliteFraction",
        "SpeciesMaxStagnation": "SpeciesDropoffAge",
        "IterationLevel": None,
        "MutateGenomeTraitsProb": None,
    }

    __seg_fault_prone__: frozenset = frozenset(
        [
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

    @property
    def __collection__(self) -> dict:
        return {
            key: getattr(self, key)
            for key in self.__dir__()
            if not key.startswith("_")
        }

    def _set_params(self, source: dict) -> multiNEATParamType:
        # Create the parameters
        params = multineat.Parameters()

        # Check if source has reject fields
        for old_key, new_key in self.__rejection__.items():
            if old_key in source:
                value = source.pop(old_key)
                if new_key is not None:
                    source[new_key] = value

        # Load params from dict
        for key, value in source.items():
            setattr(params, key, value)

        # Return the parameters
        return params

    def _clean_source(self, params: multiNEATParamType):
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
        param_keys = set(params.__dir__())
        param_keys = [key for key in param_keys if "__" not in key]
        param_keys = [key for key in param_keys if key not in ignore_fields]
        param_keys.sort()

        # Retrieve values
        param_values = [getattr(params, key) for key in param_keys]
        return dict(zip(param_keys, param_values))

    def _compare_sources(self, source_1: dict, source_2: dict):
        # Extract params
        params_1 = self._set_params(source_1)
        params_2 = self._set_params(source_2)

        # Get clean sources
        clean_source_1 = self._clean_source(params_1)
        clean_source_2 = self._clean_source(params_2)

        # Get differences
        return {
            key_1: [value_1, clean_source_2[key_1]]
            for key_1, value_1 in clean_source_1.items()
            if value_1 != clean_source_2[key_1]
        }

    def _dict_printer(self, differences: dict, name: str, ref: str = "def:"):
        # Print header
        sys.stdout.write(
            f"\n{' '*4}{name}: ClassVar[dict[str, float | int | bool]]"
            + " = {\n"
        )
        for key, (new_value, old_value) in differences.items():
            sys.stdout.write(
                f'{" "*8}"{key}": {new_value},  # {ref}{old_value}\n'
            )
        sys.stdout.write(f'{" "*4}' + "}\n")

    def _diff_printer(self, differences: dict):
        sys.stdout.write("\n")
        for key, (new_value, old_value) in differences.items():
            sys.stdout.write(f"{key}\n")
            sys.stdout.write(f"\t{old_value} -> {new_value}\n")
            sys.stdout.write("\n")


SOURCE = CollectionOfDefaultValues().GenericOld


def get_multineat_params():
    # Create the parameters
    params = multineat.Parameters()

    # Load params from dict
    for key, value in SOURCE.items():
        setattr(params, key, value)

    # Return the parameters
    return params


if __name__ == "__main__":
    # _print_multineat_params_diff()
    collection_obj = CollectionOfDefaultValues()
    source_1 = collection_obj.GenericOld
    source_2 = collection_obj.Default
    diff = collection_obj._compare_sources(source_1, source_2)
    collection_obj._diff_printer(diff)
