import math
import time
from collections.abc import Sequence

import numpy as np
import pigpio
from numpy.typing import NDArray
from pyrr import Vector3

from .._physical_interface import (
    PhysicalInterface,
)


class V1PhysicalInterface(PhysicalInterface):
    """Implementation of PhysicalInterface for V1 modular robots."""

    _PWM_FREQUENCY = 50
    _CENTER = 157.0
    _ANGLE60 = 64.0
    _PINS = list(range(2, 28))

    _debug: bool
    _dry: bool

    _gpio: pigpio.pi | None

    def __init__(self, debug: bool, dry: bool) -> None:
        """Initialize this object.

        :param debug: If debugging messages are activated.
        :param dry: If servo outputs are not propagated to the physical
            servos.
        :raises RuntimeError: If GPIOs could not initialize.
        """
        self._debug = debug
        self._dry = dry

        if not self._dry:
            self._gpio = pigpio.pi()
            if not self._gpio.connected:
                msg = "Failed to reach pigpio daemon."
                raise RuntimeError(msg)

            for pin in self._PINS:
                self._gpio.set_PWM_frequency(pin, self._PWM_FREQUENCY)
                self._gpio.set_PWM_range(pin, 2048)
                self._gpio.set_PWM_dutycycle(pin, 0)
        else:
            self._gpio = None

        if self._debug:
            pass

    def set_servo_targets(self, pins: list[int], targets: list[float]) -> None:
        """Set the target for multiple servos.

        This can be a fairly slow operation.

        :param pins: The GPIO pins.
        :type pins: list[int]
        :param targets: The target angles.
        :rtype: None
        :type targets: list[float]
        :rtype: None

        """
        if not self._dry:
            assert self._gpio is not None
            for pin, target in zip(pins, targets, strict=False):
                angle = (
                    self._CENTER
                    + target / (1.0 / 3.0 * math.pi) * self._ANGLE60
                )
                self._gpio.set_PWM_dutycycle(pin, angle)

    def enable(self) -> None:
        """Start the robot.


        :rtype: None

        """
        if not self._dry:
            assert self._gpio is not None
            for pin in self._PINS:
                self._gpio.set_PWM_dutycycle(pin, self._CENTER)
                if self._debug:
                    pass
                time.sleep(0.1)

    def disable(self) -> None:
        """Set the robot to low power mode.

        This disables all active modules and sensors.


        :rtype: None

        """
        if self._debug:
            pass
        if not self._dry:
            assert self._gpio is not None

            for pin in self._PINS:
                self._gpio.set_PWM_dutycycle(pin, 0)

    def get_battery_level(self) -> float:
        """Get the battery level.


        :rtype: float

        :raises NotImplementedError: If getting the battery level is not
            supported on this hardware.

        """
        msg = "Getting battery level not supported on v1 harware."
        raise NotImplementedError(msg)

    def get_multiple_servo_positions(self, pins: Sequence[int]) -> list[float]:
        """Get the current position of multiple servos.

        :param pins: The GPIO pins.
        :rtype: list[float]
        :type pins: Sequence[int]
        :rtype: list[float]
        :raises NotImplementedError: If getting the servo position is
            not supported on this hardware.

        """
        msg = "Getting servo position not supported on v1 harware."
        raise NotImplementedError(msg)

    def get_imu_angular_rate(self) -> Vector3:
        """Get the angular rate from the IMU.


        :rtype: Vector3

        :raises NotImplementedError: Always.

        """
        raise NotImplementedError

    def get_imu_orientation(self) -> Vector3:
        """Get the orientation from the IMU.


        :rtype: Vector3

        :raises NotImplementedError: Always.

        """
        raise NotImplementedError

    def get_imu_specific_force(self) -> Vector3:
        """Get the specific force from the IMU.


        :rtype: Vector3

        :raises NotImplementedError: Always.

        """
        raise NotImplementedError

    def get_camera_view(self) -> NDArray[np.uint8]:
        """Get the current view from the camera.


        :rtype: NDArray[np.uint8]

        :raises NotImplementedError: If the Camera is not supported on
            this hardware.

        """
        raise NotImplementedError
