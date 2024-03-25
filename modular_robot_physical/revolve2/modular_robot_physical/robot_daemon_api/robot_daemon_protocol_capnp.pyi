"""
This is an automatically generated stub for `robot_daemon_protocol.capnp`.

This file was manually edited to work better with the code tools.

Added __init__ functions
Made `dict` into `dict[Any,Any]`
Formatted file with black
RoboServer
"""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from contextlib import contextmanager
from io import BufferedWriter
from typing import Any, Literal

class SetupArgs:
    version: str
    activePins: Sequence[int]
    def __init__(
        self,
        version: str,
        activePins: Sequence[int],
    ) -> None: ...
    @staticmethod
    @contextmanager
    def from_bytes(
        data: bytes,
        traversal_limit_in_words: int | None = ...,
        nesting_limit: int | None = ...,
    ) -> Iterator[SetupArgsReader]: ...
    @staticmethod
    def from_bytes_packed(
        data: bytes,
        traversal_limit_in_words: int | None = ...,
        nesting_limit: int | None = ...,
    ) -> SetupArgsReader: ...
    @staticmethod
    def new_message() -> SetupArgsBuilder: ...
    def to_dict(self) -> dict[Any, Any]: ...

class SetupArgsReader(SetupArgs):
    def as_builder(self) -> SetupArgsBuilder: ...

class SetupArgsBuilder(SetupArgs):
    @staticmethod
    def from_dict(dictionary: dict[Any, Any]) -> SetupArgsBuilder: ...
    def copy(self) -> SetupArgsBuilder: ...
    def to_bytes(self) -> bytes: ...
    def to_bytes_packed(self) -> bytes: ...
    def to_segments(self) -> list[bytes]: ...
    def as_reader(self) -> SetupArgsReader: ...
    @staticmethod
    def write(file: BufferedWriter) -> None: ...
    @staticmethod
    def write_packed(file: BufferedWriter) -> None: ...

HardwareType = Literal["v1", "v2"]

class SetupResponse:
    versionOk: bool
    hardwareType: HardwareType
    def __init__(
        self, versionOk: bool, hardwareType: HardwareType
    ) -> None: ...
    @staticmethod
    @contextmanager
    def from_bytes(
        data: bytes,
        traversal_limit_in_words: int | None = ...,
        nesting_limit: int | None = ...,
    ) -> Iterator[SetupResponseReader]: ...
    @staticmethod
    def from_bytes_packed(
        data: bytes,
        traversal_limit_in_words: int | None = ...,
        nesting_limit: int | None = ...,
    ) -> SetupResponseReader: ...
    @staticmethod
    def new_message() -> SetupResponseBuilder: ...
    def to_dict(self) -> dict[Any, Any]: ...

class SetupResponseReader(SetupResponse):
    def as_builder(self) -> SetupResponseBuilder: ...

class SetupResponseBuilder(SetupResponse):
    @staticmethod
    def from_dict(dictionary: dict[Any, Any]) -> SetupResponseBuilder: ...
    def copy(self) -> SetupResponseBuilder: ...
    def to_bytes(self) -> bytes: ...
    def to_bytes_packed(self) -> bytes: ...
    def to_segments(self) -> list[bytes]: ...
    def as_reader(self) -> SetupResponseReader: ...
    @staticmethod
    def write(file: BufferedWriter) -> None: ...
    @staticmethod
    def write_packed(file: BufferedWriter) -> None: ...

class PinControl:
    pin: int
    target: float
    def __init__(self, pin: int, target: float) -> None: ...
    @staticmethod
    @contextmanager
    def from_bytes(
        data: bytes,
        traversal_limit_in_words: int | None = ...,
        nesting_limit: int | None = ...,
    ) -> Iterator[PinControlReader]: ...
    @staticmethod
    def from_bytes_packed(
        data: bytes,
        traversal_limit_in_words: int | None = ...,
        nesting_limit: int | None = ...,
    ) -> PinControlReader: ...
    @staticmethod
    def new_message() -> PinControlBuilder: ...
    def to_dict(self) -> dict[Any, Any]: ...

class PinControlReader(PinControl):
    def as_builder(self) -> PinControlBuilder: ...

class PinControlBuilder(PinControl):
    @staticmethod
    def from_dict(dictionary: dict[Any, Any]) -> PinControlBuilder: ...
    def copy(self) -> PinControlBuilder: ...
    def to_bytes(self) -> bytes: ...
    def to_bytes_packed(self) -> bytes: ...
    def to_segments(self) -> list[bytes]: ...
    def as_reader(self) -> PinControlReader: ...
    @staticmethod
    def write(file: BufferedWriter) -> None: ...
    @staticmethod
    def write_packed(file: BufferedWriter) -> None: ...

class ControlArgs:
    setPins: Sequence[PinControl | PinControlBuilder | PinControlReader]
    def __init__(
        self,
        setPins: Sequence[PinControl | PinControlBuilder | PinControlReader],
    ) -> None: ...
    @staticmethod
    @contextmanager
    def from_bytes(
        data: bytes,
        traversal_limit_in_words: int | None = ...,
        nesting_limit: int | None = ...,
    ) -> Iterator[ControlArgsReader]: ...
    @staticmethod
    def from_bytes_packed(
        data: bytes,
        traversal_limit_in_words: int | None = ...,
        nesting_limit: int | None = ...,
    ) -> ControlArgsReader: ...
    @staticmethod
    def new_message() -> ControlArgsBuilder: ...
    def to_dict(self) -> dict[Any, Any]: ...

class ControlArgsReader(ControlArgs):
    setPins: Sequence[PinControlReader]
    def as_builder(self) -> ControlArgsBuilder: ...

class ControlArgsBuilder(ControlArgs):
    setPins: Sequence[PinControl | PinControlBuilder | PinControlReader]
    @staticmethod
    def from_dict(dictionary: dict[Any, Any]) -> ControlArgsBuilder: ...
    def copy(self) -> ControlArgsBuilder: ...
    def to_bytes(self) -> bytes: ...
    def to_bytes_packed(self) -> bytes: ...
    def to_segments(self) -> list[bytes]: ...
    def as_reader(self) -> ControlArgsReader: ...
    @staticmethod
    def write(file: BufferedWriter) -> None: ...
    @staticmethod
    def write_packed(file: BufferedWriter) -> None: ...

class ReadSensorsArgs:
    readPins: Sequence[int]
    def __init__(self, readPins: Sequence[int]) -> None: ...
    @staticmethod
    @contextmanager
    def from_bytes(
        data: bytes,
        traversal_limit_in_words: int | None = ...,
        nesting_limit: int | None = ...,
    ) -> Iterator[ReadSensorsArgsReader]: ...
    @staticmethod
    def from_bytes_packed(
        data: bytes,
        traversal_limit_in_words: int | None = ...,
        nesting_limit: int | None = ...,
    ) -> ReadSensorsArgsReader: ...
    @staticmethod
    def new_message() -> ReadSensorsArgsBuilder: ...
    def to_dict(self) -> dict[Any, Any]: ...

class ReadSensorsArgsReader(ReadSensorsArgs):
    def as_builder(self) -> ReadSensorsArgsBuilder: ...

class ReadSensorsArgsBuilder(ReadSensorsArgs):
    @staticmethod
    def from_dict(dictionary: dict[Any, Any]) -> ReadSensorsArgsBuilder: ...
    def copy(self) -> ReadSensorsArgsBuilder: ...
    def to_bytes(self) -> bytes: ...
    def to_bytes_packed(self) -> bytes: ...
    def to_segments(self) -> list[bytes]: ...
    def as_reader(self) -> ReadSensorsArgsReader: ...
    @staticmethod
    def write(file: BufferedWriter) -> None: ...
    @staticmethod
    def write_packed(file: BufferedWriter) -> None: ...

class ControlAndReadSensorsArgs:
    setPins: Sequence[PinControl | PinControlBuilder | PinControlReader]
    readPins: Sequence[int]
    def __init__(
        self,
        setPins: Sequence[PinControl | PinControlBuilder | PinControlReader],
        readPins: Sequence[int],
    ) -> None: ...
    @staticmethod
    @contextmanager
    def from_bytes(
        data: bytes,
        traversal_limit_in_words: int | None = ...,
        nesting_limit: int | None = ...,
    ) -> Iterator[ControlAndReadSensorsArgsReader]: ...
    @staticmethod
    def from_bytes_packed(
        data: bytes,
        traversal_limit_in_words: int | None = ...,
        nesting_limit: int | None = ...,
    ) -> ControlAndReadSensorsArgsReader: ...
    @staticmethod
    def new_message() -> ControlAndReadSensorsArgsBuilder: ...
    def to_dict(self) -> dict[Any, Any]: ...

class ControlAndReadSensorsArgsReader(ControlAndReadSensorsArgs):
    setPins: Sequence[PinControlReader]
    def as_builder(self) -> ControlAndReadSensorsArgsBuilder: ...

class ControlAndReadSensorsArgsBuilder(ControlAndReadSensorsArgs):
    setPins: Sequence[PinControl | PinControlBuilder | PinControlReader]
    @staticmethod
    def from_dict(
        dictionary: dict[Any, Any],
    ) -> ControlAndReadSensorsArgsBuilder: ...
    def copy(self) -> ControlAndReadSensorsArgsBuilder: ...
    def to_bytes(self) -> bytes: ...
    def to_bytes_packed(self) -> bytes: ...
    def to_segments(self) -> list[bytes]: ...
    def as_reader(self) -> ControlAndReadSensorsArgsReader: ...
    @staticmethod
    def write(file: BufferedWriter) -> None: ...
    @staticmethod
    def write_packed(file: BufferedWriter) -> None: ...

class SensorReadings:
    pins: Sequence[float]
    battery: float
    def __init__(self, pins: Sequence[float], battery: float) -> None: ...
    @staticmethod
    @contextmanager
    def from_bytes(
        data: bytes,
        traversal_limit_in_words: int | None = ...,
        nesting_limit: int | None = ...,
    ) -> Iterator[SensorReadingsReader]: ...
    @staticmethod
    def from_bytes_packed(
        data: bytes,
        traversal_limit_in_words: int | None = ...,
        nesting_limit: int | None = ...,
    ) -> SensorReadingsReader: ...
    @staticmethod
    def new_message() -> SensorReadingsBuilder: ...
    def to_dict(self) -> dict[Any, Any]: ...

class SensorReadingsReader(SensorReadings):
    def as_builder(self) -> SensorReadingsBuilder: ...

class SensorReadingsBuilder(SensorReadings):
    @staticmethod
    def from_dict(dictionary: dict[Any, Any]) -> SensorReadingsBuilder: ...
    def copy(self) -> SensorReadingsBuilder: ...
    def to_bytes(self) -> bytes: ...
    def to_bytes_packed(self) -> bytes: ...
    def to_segments(self) -> list[bytes]: ...
    def as_reader(self) -> SensorReadingsReader: ...
    @staticmethod
    def write(file: BufferedWriter) -> None: ...
    @staticmethod
    def write_packed(file: BufferedWriter) -> None: ...

# Defining the interface as any. The stub generator does not generate for interfaces yet.
RoboServer = Any
