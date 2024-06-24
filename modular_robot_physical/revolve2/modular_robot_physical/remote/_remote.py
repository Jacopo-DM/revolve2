import asyncio
import time
from collections.abc import Callable
from typing import TYPE_CHECKING

import capnp
import numpy as np
from numpy.typing import NDArray
from pyrr import Vector3
from revolve2.modular_robot.body.base import ActiveHinge
from revolve2.modular_robot.body.sensors import CameraSensor, IMUSensor

from .._config import Config
from .._hardware_type import HardwareType
from .._protocol_version import PROTOCOL_VERSION
from .._standard_port import STANDARD_PORT
from .._uuid_key import UUIDKey
from ..robot_daemon_api import (
    robot_daemon_protocol_capnp,
)
from ._camera_sensor_state_impl import (
    CameraSensorStateImpl,
)
from ._imu_sensor_state_impl import (
    IMUSensorStateImpl,
)
from ._modular_robot_control_interface_impl import (
    ModularRobotControlInterfaceImpl,
)
from ._modular_robot_sensor_state_impl_v1 import (
    ModularRobotSensorStateImplV1,
)
from ._modular_robot_sensor_state_impl_v2 import (
    ModularRobotSensorStateImplV2,
)

if TYPE_CHECKING:
    from revolve2.modular_robot.sensor_state import ModularRobotSensorState


def _active_hinge_targets_to_pin_controls(
    config: Config,
    active_hinges_and_targets: list[tuple[UUIDKey[ActiveHinge], float]],
) -> list[robot_daemon_protocol_capnp.PinControl]:
    """

    :param config: 
    :type config: Config
    :param active_hinges_and_targets: 
    :type active_hinges_and_targets: list[tuple[UUIDKey[ActiveHinge]
    :param float]]: 
    :rtype: list[robot_daemon_protocol_capnp.PinControl]

    """
    pins = [
        config.hinge_mapping[active_hinge]
        for active_hinge, _ in active_hinges_and_targets
    ]
    inverses = [config.inverse_servos.get(pin, False) for pin in pins]
    targets = [
        (-1.0 if inverse else 1.0)
        * min(max(target, -active_hinge.value.range), active_hinge.value.range)
        for (active_hinge, target), inverse in zip(
            active_hinges_and_targets, inverses, strict=False
        )
    ]
    return [
        robot_daemon_protocol_capnp.PinControl(pin=pin, target=target)
        for pin, target in zip(pins, targets, strict=False)
    ]


async def _run_remote_impl(
    config: Config,
    hostname: str,
    on_prepared: Callable[[], None],
    port: int,
    debug: bool,
    manual_mode: bool,
) -> None:
    """

    :param config: 
    :type config: Config
    :param hostname: 
    :type hostname: str
    :param on_prepared: 
    :type on_prepared: Callable[[]
    :param None]: 
    :param port: 
    :type port: int
    :param debug: 
    :type debug: bool
    :param manual_mode: 
    :type manual_mode: bool
    :rtype: None

    """
    active_hinge_sensor_to_pin = {
        UUIDKey(key.value.sensors.active_hinge_sensor): pin
        for key, pin in config.hinge_mapping.items()
        if key.value.sensors.active_hinge_sensor is not None
    }

    # Make controller
    controller = config.modular_robot.brain.make_instance()

    # Connect to robot
    try:
        connection = await capnp.AsyncIoStream.create_connection(
            host=hostname, port=port
        )
        client = capnp.TwoPartyClient(connection)
        service = client.bootstrap().cast_as(
            robot_daemon_protocol_capnp.RoboServer
        )
    except ConnectionRefusedError:
        msg = "Could not connect to robot."
        raise ConnectionRefusedError(msg)

    # Setup the robot and check protocol version
    setup_response: robot_daemon_protocol_capnp.SetupResponse = (
        await service.setup(
            robot_daemon_protocol_capnp.SetupArgs(
                version=PROTOCOL_VERSION, activePins=list(range(32))
            )
        )
    ).response
    if not setup_response.versionOk:
        msg = "Protocol version does not match for robot."
        raise RuntimeError(msg)
    match setup_response.hardwareType:
        case "v1":
            hardware_type = HardwareType.v1
        case "v2":
            hardware_type = HardwareType.v2
        case _:
            raise NotImplementedError

    # Set hinges to initial positions.
    pin_controls = _active_hinge_targets_to_pin_controls(
        config,
        [
            (active_hinge, config.initial_hinge_positions[active_hinge])
            for active_hinge in config.hinge_mapping
        ],
    )
    match hardware_type:
        case HardwareType.v1:
            await service.control(
                robot_daemon_protocol_capnp.ControlArgs(setPins=pin_controls)
            )
        case HardwareType.v2:
            sensor_readings: robot_daemon_protocol_capnp.SensorReadings = (
                await service.controlAndReadSensors(
                    robot_daemon_protocol_capnp.ControlAndReadSensorsArgs(
                        setPins=pin_controls, readPins=[]
                    )
                )
            ).response

    # Fire prepared callback
    on_prepared()

    if manual_mode:
        while True:
            try:
                target = float(input())
            except ValueError:
                continue
            if target < -1 or target > 1:
                continue
            pin_controls = _active_hinge_targets_to_pin_controls(
                config,
                [
                    (active_hinge, target)
                    for active_hinge in config.hinge_mapping
                ],
            )

            await service.control(
                robot_daemon_protocol_capnp.ControlArgs(setPins=pin_controls)
            )

    else:
        # Run the controller
        control_period = 1 / config.control_frequency

        start_time = time.time()
        last_update_time = start_time

        battery_print_timer = 0.0

        sensor_state: ModularRobotSensorState

        # Get initial sensor state
        match hardware_type:
            case HardwareType.v1:
                sensor_state = ModularRobotSensorStateImplV1()
            case HardwareType.v2:
                pins = list(active_hinge_sensor_to_pin.values())
                sensor_readings = (
                    await service.readSensors(
                        robot_daemon_protocol_capnp.ReadSensorsArgs(
                            readPins=pins
                        )
                    )
                ).response
                imu_sensor_states = _get_imu_sensor_state(
                    config.modular_robot.body.core.sensors.imu_sensor,
                    sensor_readings,
                )
                camera_sensor_states = _get_camera_sensor_state(
                    config.modular_robot.body.core.sensors.camera_sensor,
                    sensor_readings,
                )

                sensor_state = ModularRobotSensorStateImplV2(
                    hinge_sensor_mapping=active_hinge_sensor_to_pin,
                    hinge_positions=dict(
                        zip(pins, sensor_readings.pins, strict=False)
                    ),
                    imu_sensor_states=imu_sensor_states,
                    camera_sensor_states=camera_sensor_states,
                )
            case _:
                msg = "Hardware type not supported."
                raise NotImplementedError(msg)

        while (current_time := time.time()) - start_time < config.run_duration:
            # Sleep until next control update
            next_update_at = last_update_time + control_period
            if current_time < next_update_at:
                await asyncio.sleep(next_update_at - current_time)
                last_update_time = next_update_at
                elapsed_time = control_period
            else:
                elapsed_time = last_update_time - current_time
                last_update_time = current_time

            # Get targets from brain
            control_interface = ModularRobotControlInterfaceImpl()
            controller.control(
                elapsed_time,
                sensor_state=sensor_state,
                control_interface=control_interface,
            )

            # Increase the timer for the battery value message
            battery_print_timer += elapsed_time

            # Reading sensors will come in a later update.
            pin_controls = _active_hinge_targets_to_pin_controls(
                config, control_interface._set_active_hinges
            )
            match hardware_type:
                case HardwareType.v1:
                    await service.control(
                        robot_daemon_protocol_capnp.ControlArgs(
                            setPins=pin_controls
                        )
                    )
                    sensor_state = ModularRobotSensorStateImplV1()
                case HardwareType.v2:
                    pins = list(active_hinge_sensor_to_pin.values())
                    sensor_readings = (
                        await service.controlAndReadSensors(
                            robot_daemon_protocol_capnp.ControlAndReadSensorsArgs(
                                setPins=pin_controls, readPins=pins
                            )
                        )
                    ).response

                    imu_sensor_states = _get_imu_sensor_state(
                        config.modular_robot.body.core.sensors.imu_sensor,
                        sensor_readings,
                    )
                    camera_sensor_states = _get_camera_sensor_state(
                        config.modular_robot.body.core.sensors.camera_sensor,
                        sensor_readings,
                    )

                    sensor_state = ModularRobotSensorStateImplV2(
                        hinge_sensor_mapping=active_hinge_sensor_to_pin,
                        hinge_positions=dict(
                            zip(pins, sensor_readings.pins, strict=False)
                        ),
                        imu_sensor_states=imu_sensor_states,
                        camera_sensor_states=camera_sensor_states,
                    )

                    if battery_print_timer > 5.0:
                        battery_print_timer = 0.0
                case _:
                    msg = "Hardware type not supported."
                    raise NotImplementedError(msg)


def _capnp_to_vector3(vector: robot_daemon_protocol_capnp.Vector3) -> Vector3:
    """

    :param vector: 
    :type vector: robot_daemon_protocol_capnp.Vector3
    :rtype: Vector3

    """
    return Vector3([vector.x, vector.y, vector.z])


def _capnp_to_camera_view(
    image: robot_daemon_protocol_capnp.Image, camera_size: tuple[int, int]
) -> NDArray[np.uint8]:
    """Convert a capnp compatible Image into an NDArray.

    :param image: The capnp Image.
    :type image: robot_daemon_protocol_capnp.Image
    :param camera_size: The camera size to reconstruct the image.
    :type camera_size: tuple[int, int]
    :returns: The NDArray imag.
    :rtype: NDArray[np.uint8]

    """
    np_image = np.zeros(shape=(3, *camera_size), dtype=np.uint8)
    np_image[0] = np.array(image.r).reshape(camera_size).astype(np.uint8)
    np_image[1] = np.array(image.g).reshape(camera_size).astype(np.uint8)
    np_image[2] = np.array(image.b).reshape(camera_size).astype(np.uint8)
    return np_image


def _get_imu_sensor_state(
    imu_sensor: IMUSensor | None,
    sensor_readings: robot_daemon_protocol_capnp.SensorReadings,
) -> dict[UUIDKey[IMUSensor], IMUSensorStateImpl]:
    """Get the IMU sensor state.

    :param imu_sensor: The sensor in question.
    :type imu_sensor: IMUSensor | None
    :param sensor_readings: The sensor readings.
    :type sensor_readings: robot_daemon_protocol_capnp.SensorReadings
    :returns: The Sensor state.
    :rtype: dict[UUIDKey[IMUSensor],IMUSensorStateImpl]

    """
    if imu_sensor is None:
        return {}
    return {
        UUIDKey(imu_sensor): IMUSensorStateImpl(
            _capnp_to_vector3(sensor_readings.imuSpecificForce),
            _capnp_to_vector3(sensor_readings.imuAngularRate),
            _capnp_to_vector3(sensor_readings.imuOrientation),
        )
    }


def _get_camera_sensor_state(
    camera_sensor: CameraSensor | None,
    sensor_readings: robot_daemon_protocol_capnp.SensorReadings,
) -> dict[UUIDKey[CameraSensor], CameraSensorStateImpl]:
    """Get the camera sensor state.

    :param camera_sensor: The sensor in question.
    :type camera_sensor: CameraSensor | None
    :param sensor_readings: The sensor readings.
    :type sensor_readings: robot_daemon_protocol_capnp.SensorReadings
    :returns: The Sensor state.
    :rtype: dict[UUIDKey[CameraSensor],CameraSensorStateImpl]

    """
    if camera_sensor is None:
        return {}
    return {
        UUIDKey(camera_sensor): CameraSensorStateImpl(
            _capnp_to_camera_view(
                sensor_readings.cameraView, camera_sensor.camera_size
            )
        )
    }


def run_remote(
    config: Config,
    hostname: str,
    on_prepared: Callable[[], None] = lambda: None,
    port: int = STANDARD_PORT,
    debug: bool = False,
    manual_mode: bool = False,
) -> None:
    """Control a robot remotely, running the controller on your local machine.

    :param config: The robot configuration.
    :type config: Config
    :param hostname: Hostname or IP of the robot.
    :type hostname: str
    :param on_prepared: Callback for when everything is prepared, ready
        to run the actual controller. You can use this for timing when
        the actual controller starts.
    :type on_prepared: Callable[[]
    :param None]:  (Default value = lambda: None)
    :param port: Port the robot daemon uses. (Default value = STANDARD_PORT)
    :type port: int
    :param debug: Enable debug messages. (Default value = False)
    :type debug: bool
    :param manual_mode: Enable manual controls for the robot, ignoring
        the brain. (Default value = False)
    :type manual_mode: bool
    :rtype: None

    """
    asyncio.run(
        capnp.run(
            _run_remote_impl(
                config=config,
                hostname=hostname,
                on_prepared=on_prepared,
                port=port,
                debug=debug,
                manual_mode=manual_mode,
            )
        )
    )
