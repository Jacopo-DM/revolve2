from __future__ import annotations

import faulthandler
import logging
import typing as t
from copy import deepcopy
from sys import stdout
from typing import ClassVar

import multineat

from ci_group.genotypes.cppnwin.modular_robot._multineat_collection import (
    CollectionOfDefaultValues,
)

if t.TYPE_CHECKING:
    from multineat._multineat import Parameters as multiNEATParamType

# Enable faulthandler to dump tracebacks on segfault.
faulthandler.enable()


def pretty_print(func: t.Callable[..., None]) -> t.Callable[..., None]:
    def wrapper(*args: list[t.Any], **kwargs: dict[str, t.Any]) -> None:
        size = 80
        stdout.write(f"{'=' * size}\n")
        stdout.write(f"{func.__name__:^80}\n")
        stdout.write(f"{'=' * size}\n")
        func(*args, **kwargs)
        stdout.write(f"{'-' * size}\n")
        stdout.write(f"{' ' * size}\n")
        stdout.flush()

    return wrapper


class ParamAnalyzer:
    def __init__(self, *, params: bool | multiNEATParamType = None) -> None:
        # Create an instance of multineat.Parameters
        if params is None:
            params = multineat.Parameters()

        # Initialize states
        self._analyse_parameters(params)

    def _analyse_parameters(self, params: multiNEATParamType) -> None:
        # Initialize empty lists to store values and keys
        safe_keys: dict[str, tuple[float | int | bool | str, str]] = {
            key: ("na", "na") for key in dir(params) if not key.startswith("__")
        }
        unsafe_keys: set[str] = {
            key for key in dir(params) if key.startswith("__")
        }

        # Iterate over all keys in params
        for key in dir(params):
            if key.startswith("__"):
                continue

            # Retrieve the value of the key (ensure it causes no errors)
            try:
                value = getattr(params, key)
            except TypeError:
                unsafe_keys.update(key)
                safe_keys.pop(key)
                continue

            # Check if the value is valid
            if not isinstance(value, float | int | bool | str):
                unsafe_keys.update(key)
                safe_keys.pop(key)
                continue

            # Append the value to the values list
            safe_keys[key] = (value, value.__class__.__name__)

        # Store the values and keys
        self.safe_keys: dict[str, tuple[float | int | bool | str, str]] = (
            safe_keys
        )
        self.unsafe_keys: set[str] = unsafe_keys

    def get_keys(self) -> dict[str, tuple[float | int | bool | str, str]]:
        return self.safe_keys

    def get_unsafe_keys(self) -> set[str]:
        return self.unsafe_keys

    def __sub__(
        self, other: ParamAnalyzer, *, verbose: bool = True
    ) -> tuple[
        dict[str, tuple[float | int | bool | str, str]],
        dict[str, tuple[float | int | bool | str, str]],
    ]:
        # Find the differences in the values (from self to other)
        diff_from: dict[str, tuple[float | int | bool | str, str]] = {
            key: value
            for key, value in self.safe_keys.items()
            if value != other.safe_keys[key]
        }

        diff_to: dict[str, tuple[float | int | bool | str, str]] = {
            key: value
            for key, value in other.safe_keys.items()
            if value != self.safe_keys[key]
        }

        if verbose:
            # Print the differences
            self.print_sub(diff_from, diff_to)

        # Return the differences
        return diff_from, diff_to

    @classmethod
    @pretty_print
    def print_sub(
        cls,
        diff_from: dict[str, tuple[float | int | bool | str, str]],
        diff_to: dict[str, tuple[float | int | bool | str, str]],
    ) -> None:
        for key, value in diff_from.items():
            stdout.write(f"{key:<50}: {value[0]:>7} -> {diff_to[key][0]:<7}\n")

    @pretty_print
    def print_multineat_params_full(self) -> None:
        # Print the header
        tab = "    "
        stdout.write(f"{' ' * 40}\n")
        header = "DefaultGenome: dict[str, float | int | bool] = {"
        stdout.write(f"{header}\n")

        # Print the values
        current_type = None
        for key, (value, _type) in sorted(
            self.safe_keys.items(),
            # sort by _type and then by key
            key=lambda x: (x[1][1], x[0]),
        ):
            if current_type != _type:
                stdout.write(f"{tab}# -- > {_type}\n")
                current_type = _type

            # Print the key and value
            stdout.write(f"{tab}'{key}': {value},\n")

        # Close the dictionary
        stdout.write("}\n")

    @pretty_print
    def print_multineat_params_with_ref(
        self,
        other: ParamAnalyzer,
        name: str = "Valid",
    ) -> None:
        # Print the header
        stdout.write(f"{' ' * 40}\n")
        tab = "    "
        header = f"{tab}{name}: ClassVar[dict[str, float | int | bool]] = {'{'}"
        stdout.write(f"{header}\n")

        for key, value in sorted(
            self.safe_keys.items(),
            # sort by _type and then by key
            key=lambda x: (x[1][1], x[0]),
        ):
            if value != other.safe_keys[key]:
                stdout.write(
                    f"{tab * 2}'{key}': {value[0]}, # -> {other.safe_keys[key][0]}\n"
                )

        # Close the dictionary
        stdout.write(f"{tab}{'}'}\n")


class MultiNEATParamsWriter:
    __safe_keys__: ClassVar[set[str]] = {
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

    __unsafe_keys__: ClassVar[set[str]] = {
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

    def _check_validity(self, source: dict[str, float | int | bool]) -> None:
        # Make set of keys and check if source is empty
        source_keys = set(source.keys())
        if not source_keys:
            logging.warning("Empty source provided, this may be an error.")

        # Make sure no unsafe keys are present
        if from_unsafe := source_keys.intersection(self.__unsafe_keys__):
            msg = f"Unsafe keys found: {from_unsafe}"
            raise ValueError(msg)

        # Make sure every key is known
        if len(from_safe := source_keys - self.__safe_keys__) != 0:
            msg = f"Found unkown keys: {from_safe}"
            raise ValueError(msg)

        # Replace any rejected keys with the correct ones
        for old_key, new_key in self.__rejection__.items():
            if old_key in source:
                new_value = source.pop(old_key)
                if new_key is not None:
                    source[new_key] = new_value

    def strip_params(
        self,
        source: multiNEATParamType,
        to_remove: dict[str, float | int | bool] | None = None,
    ) -> multiNEATParamType:
        # Check if to_remove is None
        if to_remove is None:
            to_remove = self.__inject_override__

        # Load the original values
        org = deepcopy(multineat.Parameters())

        # Replace the source values
        for key in to_remove:
            setattr(source, key, getattr(org, key))

        # Return the target
        return source

    def set_params(
        self,
        target: dict[str, float | int | bool],
        *,
        prevalidated: bool = False,
    ) -> multiNEATParamType:
        # Check validity of target
        if not prevalidated:
            logging.warning("Source not prevalidated, this may cause crashes.")
            self._check_validity(target)

        # Create the parameters
        params = deepcopy(multineat.Parameters())

        # Load params from dict
        for key, value in target.items():
            setattr(params, key, value)

        # Override parameters
        for key, value in self.__inject_override__.items():
            setattr(params, key, value)

        # Return the parameters
        return params


def get_multineat_params(name: str = "NoveltySearch") -> multiNEATParamType:
    param_writer = MultiNEATParamsWriter()
    target = getattr(CollectionOfDefaultValues, name)
    return param_writer.set_params(target, prevalidated=True)
