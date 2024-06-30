from __future__ import annotations

import faulthandler
import logging
import typing as t
from copy import deepcopy
from sys import stdout
from typing import ClassVar

import multineat

from ._multineat_collection import (
    CollectionOfDefaultValues,
)
from ._multineat_keys_info import (
    SAFE_KEYS,
    UNSAFE_KEYS,
)

if t.TYPE_CHECKING:
    from multineat._multineat import Parameters as multiNEATParamType

# Enable faulthandler to dump tracebacks on segfault.
faulthandler.enable()


def pretty_print(func: t.Callable[..., None]) -> t.Callable[..., None]:
    """Decorate a function to "pretty print" a header and footer around the
    decorated function.

    :param func: The function to be decorated.
    :type func: t.Callable[..., None]
    :returns: The decorated function.
    :rtype: t.Callable[...,None]
    """

    def wrapper(*args: list[t.Any], **kwargs: dict[str, t.Any]) -> None:
        """Wrap function to add the "pretty print" functionality.

        :param args:
        :type args: list[t.Any]
        :param kwargs:
        :type kwargs: dict[str, t.Any]
        :returns: None
        :rtype: None
        """
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
    """Class for analyzing and comparing parameters of multineat.Parameters
    objects.
    """

    def __init__(self, *, params: bool | multiNEATParamType = None) -> None:
        """Initialize a ParamAnalyzer object.

        :param params: The parameters to analyze. Defaults to None.
        :type params: bool | multiNEATParamType, optional
        """
        # Create an instance of multineat.Parameters
        if params is None:
            params = multineat.Parameters()

        # Initialize states
        self._analyse_parameters(params)

    def _analyse_parameters(self, params: multiNEATParamType) -> None:
        """Analyzes the parameters and stores the safe and unsafe keys.

        :param params:
        :type params: multiNEATParamType
        :rtype: None
        """
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
        """Return the dictionary of safe keys.

        :returns: dict[str, tuple[float | int | bool | str, str]]: The
            dictionary of safe keys.
        :rtype: dict[str,tuple[float|int|bool|str,str]]
        """
        return self.safe_keys

    def get_unsafe_keys(self) -> set[str]:
        """Return the set of unsafe keys.

        :returns: A set of strings representing the unsafe keys.
        :rtype: set[str]
        """
        return self.unsafe_keys

    def __sub__(
        self, other: ParamAnalyzer, *, verbose: bool = True
    ) -> tuple[
        dict[str, tuple[float | int | bool | str, str]],
        dict[str, tuple[float | int | bool | str, str]],
    ]:
        """Subtract two ParamAnalyzer objects and return the differences in
        their values.

        Parameters:
        - other (ParamAnalyzer): The ParamAnalyzer object to subtract from self.
        - verbose (bool): If True, print the differences in values.

        Returns:
        - tuple[dict[str, tuple[float | int | bool | str, str]], dict[str, tuple[float | int | bool | str, str]]]:

            A tuple containing two dictionaries:
            - diff_from: A dictionary containing the differences in values from self to other.
            - diff_to: A dictionary containing the differences in values from other to self.
        """
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
        """Print the differences in parameters.

        :param diff_from: The differences from self to other.
        :type diff_from: dict[str, tuple[float | int | bool | str, str]]
        :param diff_to: The differences from other to self.
        :type diff_to: dict[str, tuple[float | int | bool | str, str]]
        :rtype: None
        """
        for key, value in diff_from.items():
            stdout.write(f"{key:<50}: {value[0]:>7} -> {diff_to[key][0]:<7}\n")

    @pretty_print
    def print_multineat_params_full(self) -> None:
        """Print the full multineat parameters.

        :rtype: None
        """
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
        """Print the multineat parameters with reference to another
        ParamAnalyzer object.

        :param other: The ParamAnalyzer object to compare with.
        :type other: ParamAnalyzer
        :param name: The name of the reference. Defaults to "Valid".
        :type name: str
        :rtype: None
        """
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
    """A class that provides methods for manipulating MultiNEAT parameters."""

    __inject_override__: ClassVar[dict[str, float | int | bool]] = {
        # NOTE - These field-values are enforced in every case
        "PhasedSearching": True,  # def: False
        "DeltaCoding": True,  # def: False
        "MutateOutputActivationFunction": True,  # WARN CHANGED!
        "PopulationSize": 400,  # def: 150
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
        """Check the validity of the provided source dictionary.

        :param source: dict
        :type source: dict[str, float | int | bool]
        :returns: None
        :rtype: None
        :raises ValueError: If unsafe keys are found or unknown keys are
            found
        """
        # Make set of keys and check if source is empty
        source_keys = set(source.keys())
        if not source_keys:
            logging.warning("Empty source provided, this may be an error.")

        # Make sure no unsafe keys are present
        if from_unsafe := source_keys.intersection(UNSAFE_KEYS):
            msg = f"Unsafe keys found: {from_unsafe}"
            raise ValueError(msg)

        # Make sure every key is known
        if len(from_safe := source_keys - SAFE_KEYS) != 0:
            msg = f"Found unknown keys: {from_safe}"
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
        """Strip the specified parameters from the given source object and
        returns the modified object.

        :param source: multiNEATParamType
        :type source: multiNEATParamType
        :param to_remove: dict (Default value = None)
        :type to_remove: dict[str, float | int | bool] | None
        :returns: multiNEATParamType: The modified source object with
            the specified parameters stripped.
        :rtype: multiNEATParamType
        """
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
        """Set the parameters for the multiNEAT algorithm based on the given
        target dictionary.

        :param target: dict
        :type target: dict[str, float | int | bool]
        :param prevalidated: bool (Default value = False)
        :type prevalidated: bool
        :param :
        :returns: multiNEATParamType: The multiNEAT parameters object.
        :rtype: multiNEATParamType
        :raises ValueError: If the target dictionary is invalid
        """
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


def get_multineat_params(
    name: str = "Jacked",
) -> multiNEATParamType:
    """Retrieve the multiNEAT parameters for the specified name.

    :param name: str (Default value = "NoveltySearch")
    :type name: str
    :returns: multiNEATParamType: The multiNEAT parameters for the
        specified name.
    :rtype: multiNEATParamType
    """
    param_writer = MultiNEATParamsWriter()
    target = getattr(CollectionOfDefaultValues, name)
    return param_writer.set_params(target, prevalidated=True)
