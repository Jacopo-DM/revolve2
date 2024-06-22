"""Physical modular robot remote control."""

from modular_robot_physical.remote._remote import run_remote
from modular_robot_physical.remote._test_physical_robot import (
    test_physical_robot,
)

__all__ = ["run_remote", "test_physical_robot"]
