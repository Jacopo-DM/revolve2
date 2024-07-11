import logging
import os
from pathlib import Path

import numpy as np

print("Setting environment variable to use GPU rendering:")
os.environ["MUJOCO_GL"] = "egl"

xla_flags = os.environ.get("XLA_FLAGS", "")
xla_flags += " --xla_gpu_triton_gemm_any=True"
os.environ["XLA_FLAGS"] = xla_flags

import math
from time import time as tt

import mediapy as media
import mujoco
from revolve2.simulation.scene import Scene, SimulationState

from ._control_interface_impl import (
    ControlInterfaceImpl,
)
from ._scene_to_model import scene_to_model
from ._simulation_state_impl import (
    SimulationStateImpl,
)


def simulate_scene_minimal(
    scene: Scene,
    simulation_timestep: float,
    integrator: str,
    sample_step: float | None,
    simulation_time: int | None,
    control_step: float,
    *,
    cast_shadows: bool,
    fast_sim: bool,
    **kwargs,
):
    model, mapping = scene_to_model(
        scene=scene,
        simulation_timestep=simulation_timestep,
        integrator=integrator,
        cast_shadows=cast_shadows,
        fast_sim=fast_sim,
    )
    data = mujoco.MjData(model)

    control_interface = ControlInterfaceImpl(
        data=data, abstraction_to_mujoco_mapping=mapping
    )

    last_control_time = 0.0
    last_sample_time = 0.0

    images = {}

    simulation_states: list[SimulationState] = []

    mujoco.mj_forward(model, data)

    if sample_step is not None:
        simulation_states.append(
            SimulationStateImpl(
                data=data,
                abstraction_to_mujoco_mapping=mapping,
                camera_views=images,
            )
        )

    # enable joint visualization option:
    scene_option = mujoco.MjvOption()
    scene_option.flags[mujoco.mjtVisFlag.mjVIS_JOINT] = True

    frames = []
    w, h = 640, 480
    framerate = 24
    renderer = mujoco.Renderer(model, height=h, width=w)

    while (time := data.time) < (
        float("inf") if simulation_time is None else simulation_time
    ):
        if len(frames) < data.time * framerate:
            renderer.update_scene(data, scene_option=scene_option)
            pixels = renderer.render()
            frames.append(pixels)

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

        if sample_step is not None and time >= last_sample_time + sample_step:
            last_sample_time = int(time / sample_step) * sample_step
            simulation_states.append(
                SimulationStateImpl(
                    data=data,
                    abstraction_to_mujoco_mapping=mapping,
                    camera_views=images,
                )
            )

        mujoco.mj_step(model, data)

    timestamp = int(tt())
    name = ""

    logging.info(f"Writing video to video/{timestamp}{name}.mp4")
    logging.info(f"Frames dimension: {np.array(frames).shape}")

    # make dir if not exists
    Path("video").mkdir(parents=True, exist_ok=True)

    media.write_video(
        path=f"video/{timestamp}{name}.mp4", images=frames, fps=framerate
    )

    if sample_step is not None:
        simulation_states.append(
            SimulationStateImpl(
                data=data,
                abstraction_to_mujoco_mapping=mapping,
                camera_views=images,
            )
        )

    return simulation_states
