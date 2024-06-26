from .._hardware_type import HardwareType
from ._physical_interface import (
    PhysicalInterface,
)


def get_interface(
    hardware_type: HardwareType, debug: bool, dry: bool
) -> PhysicalInterface:
    """Get the interface for the given hardware type.

    :param hardware_type: The type of hardware.
    :type hardware_type: HardwareType
    :param debug: If debugging messages are activated.
    :type debug: bool
    :param dry: If servo outputs are not propagated to the physical
        servos.:
    :type dry: bool
    :returns: The interface.
    :rtype: PhysicalInterface
    :raises NotImplementedError: If the hardware type is not supported
        or if careful is enabled and not supported for the hardware
        type.
    :raises ModuleNotFoundError: If some required package are not
        installed.

    """
    try:
        match hardware_type:
            case HardwareType.v1:
                from .v1 import (
                    V1PhysicalInterface,
                )

                return V1PhysicalInterface(debug=debug, dry=dry)
            case HardwareType.v2:
                from .v2 import (
                    V2PhysicalInterface,
                )

                return V2PhysicalInterface(debug=debug, dry=dry)
            case _:
                msg = "Hardware type not supported."
                raise NotImplementedError(msg)
    except ModuleNotFoundError as e:
        msg = f"Could not import physical interface, did you install the required extras? Error: {e}"
        raise ModuleNotFoundError(msg) from None
