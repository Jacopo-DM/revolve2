"""Interfaces to the hardware."""

from modular_robot_physical.physical_interfaces._get_interface import (
    get_interface,
)
from modular_robot_physical.physical_interfaces._physical_interface import (
    PhysicalInterface,
)

__all__ = ["PhysicalInterface", "get_interface"]
