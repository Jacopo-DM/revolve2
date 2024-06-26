import logging
import math

import cv2
import mujoco
import numpy as np
import numpy.typing as npt
from revolve2.simulation.scene import Scene, SimulationState
from revolve2.simulation.simulator import RecordSettings

from ._control_interface_impl import (
    ControlInterfaceImpl,
)
from ._open_gl_vision import OpenGLVision
from ._render_backend import RenderBackend
from ._scene_to_model import scene_to_model
from ._simulation_state_impl import (
    SimulationStateImpl,
)
from .viewers import (
    CustomMujocoViewer,
    NativeMujocoViewer,
    ViewerType,
)


def simulate_scene(
    viewer_type: ViewerType,
    scene_id: int,
    scene: Scene,
    record_settings: RecordSettings | None,
    control_step: float,
    sample_step: float | None,
    simulation_time: int | None,
    simulation_timestep: float,
    integrator: str,
    render_backend: RenderBackend = RenderBackend.GLFW,
    *,
    headless: bool,
    start_paused: bool,
    cast_shadows: bool,
    fast_sim: bool,
) -> list[SimulationState]:
    """Simulate a scene.

    :param viewer_type: The type of viewer used for the rendering in a
        window.
    :type viewer_type: ViewerType
    :param scene_id: An id for this scene, unique between all scenes ran
        in parallel.
    :type scene_id: int
    :param scene: The scene to simulate.
    :type scene: Scene
    :param record_settings: If not None, recording will be done
        according to these settings.
    :type record_settings: RecordSettings | None
    :param control_step: The time between each call to the handle
        function of the scene handler. In seconds.
    :type control_step: float
    :param sample_step: The time between each state sample of the
        simulation. In seconds.
    :type sample_step: float | None
    :param simulation_time: How long to simulate for. In seconds.
    :type simulation_time: int | None
    :param simulation_timestep: The duration to integrate over during
        each step of the simulation. In seconds.
    :type simulation_timestep: float
    :param render_backend: The backend to be used for rendering (EGL by
        default and switches to GLFW if no cameras are on the robot).
    :type render_backend: RenderBackend
    :param *:
    :param headless: If False, a viewer will be opened that allows a
        user to manually view and manually interact with the simulation.
    :type headless: bool
    :param start_paused: If true, the simulation will start in a paused
        state. Only makes sense when headless is False.
    :type start_paused: bool
    :param cast_shadows: If shadows are cast.
    :type cast_shadows: bool
    :param fast_sim: If fancy rendering is disabled.
    :type fast_sim: bool
    :returns: The results of simulation. The number of returned states
        depends on `sample_step`.
    :rtype: list[SimulationState]
    :raises ValueError: If the viewer is not able to record.

    """
    logging.debug("Simulating scene %d", scene_id)
    """Define mujoco data and model objects for simulating."""
    model, mapping = scene_to_model(
        scene=scene,
        simulation_timestep=simulation_timestep,
        integrator=integrator,
        cast_shadows=cast_shadows,
        fast_sim=fast_sim,
    )
    data = mujoco.MjData(model)
    """Define a control interface for the mujoco simulation (used to control
    robots)."""
    control_interface = ControlInterfaceImpl(
        data=data, abstraction_to_mujoco_mapping=mapping
    )
    """Make separate viewer for camera sensors."""
    camera_viewers: dict[int, OpenGLVision] = {
        camera.camera_id: OpenGLVision(
            model=model,
            camera=camera,
            headless=headless,
            open_gl_lib=render_backend,
        )
        for camera in mapping.camera_sensor.values()
    }
    """Define some additional control variables."""
    last_control_time = 0.0
    last_sample_time = 0.0
    last_video_time = 0.0  # time at which last video frame was saved

    simulation_states: list[
        SimulationState
    ] = []  # The measured states of the simulation
    """If we dont have cameras and the backend is not set we go to the default
    GLFW."""
    if len(mapping.camera_sensor.values()) == 0:
        render_backend = RenderBackend.EGL if headless else RenderBackend.GLFW

    """Initialize viewer object if we need to render the scene."""
    if not headless or record_settings is not None:
        match viewer_type:
            case viewer_type.CUSTOM:
                viewer = CustomMujocoViewer
            case viewer_type.NATIVE:
                viewer = NativeMujocoViewer
            case _:
                msg = f"Viewer of type {viewer_type} not defined in _simulate_scene."
                raise ValueError(msg)

        viewer = viewer(
            model=model,
            data=data,
            width=None if record_settings is None else record_settings.width,
            height=None if record_settings is None else record_settings.height,
            backend=render_backend,
            start_paused=start_paused,
            render_every_frame=False,
            hide_menus=(record_settings is not None),
        )

    """Record the scene if we want to record."""
    if record_settings is not None:
        if not viewer.can_record:
            msg = f"Selected Viewer {type(viewer).__name__} has no functionality to record."
            raise ValueError(msg)
        video_step = 1 / record_settings.fps
        video_file_path = f"{record_settings.video_directory}/{scene_id}.mp4"
        fourcc = cv2.VideoWriter.fourcc(*"mp4v")
        video = cv2.VideoWriter(
            video_file_path,
            fourcc,
            record_settings.fps,
            viewer.current_viewport_size(),
        )

    """
    Compute forward dynamics without actually stepping forward in time.
    This updates the data so we can read out the initial state.
    """
    mujoco.mj_forward(model, data)
    images = {
        camera_id: camera_viewer.process(model, data)
        for camera_id, camera_viewer in camera_viewers.items()
    }

    # Sample initial state.
    if sample_step is not None:
        simulation_states.append(
            SimulationStateImpl(
                data=data,
                abstraction_to_mujoco_mapping=mapping,
                camera_views=images,
            )
        )

    """After rendering the initial state, we enter the rendering loop."""
    while (time := data.time) < (
        float("inf") if simulation_time is None else simulation_time
    ):
        # do control if it is time
        if time >= last_control_time + control_step:
            last_control_time = math.floor(time / control_step) * control_step

            simulation_state = SimulationStateImpl(
                data=data,
                abstraction_to_mujoco_mapping=mapping,
                camera_views=images,
            )
            scene.handler.handle(
                simulation_state, control_interface, control_step
            )

        # sample state if it is time
        if sample_step is not None and time >= last_sample_time + sample_step:
            last_sample_time = int(time / sample_step) * sample_step
            simulation_states.append(
                SimulationStateImpl(
                    data=data,
                    abstraction_to_mujoco_mapping=mapping,
                    camera_views=images,
                )
            )

        # step simulation
        mujoco.mj_step(model, data)
        # extract images from camera sensors.
        images = {
            camera_id: camera_viewer.process(model, data)
            for camera_id, camera_viewer in camera_viewers.items()
        }

        # render if not headless. also render when recording and if it time for a new video frame.
        if not headless or (
            record_settings is not None and time >= last_video_time + video_step
        ):
            viewer_return = viewer.render()
            if viewer_return == "QUIT":
                logging.warning("Quitting viewer")
                raise SystemExit(0)

        # capture video frame if it's time
        if record_settings is not None and time >= last_video_time + video_step:
            last_video_time = int(time / video_step) * video_step

            # https://github.com/deepmind/mujoco/issues/285 (see also record.cc)
            img: npt.NDArray[np.uint8] = np.empty(
                (*viewer.current_viewport_size(), 3),
                dtype=np.uint8,
            )

            mujoco.mjr_readPixels(
                rgb=img,
                depth=None,
                viewport=viewer.view_port,
                con=viewer.context,
            )
            # Flip the image and map to OpenCV colormap (BGR -> RGB)
            img = np.flipud(img)[:, :, ::-1]
            video.write(img)

    """Once simulation is done we close the potential viewer and release the potential video."""
    if not headless or record_settings is not None:
        viewer.close_viewer()

    if record_settings is not None:
        video.release()

    # Sample one final time.
    if sample_step is not None:
        simulation_states.append(
            SimulationStateImpl(
                data=data,
                abstraction_to_mujoco_mapping=mapping,
                camera_views=images,
            )
        )

    logging.debug(f"Scene {scene_id} done.")
    return simulation_states
