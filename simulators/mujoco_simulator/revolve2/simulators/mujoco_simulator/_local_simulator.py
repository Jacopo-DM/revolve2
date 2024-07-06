import logging

from ._simulate_scene_minimal import simulate_scene_minimal

logging.debug(
    "'simulate_scene_minimal' must be first import to not break the renderers"
)
from ._simulate_scene import simulate_scene

logging.debug(
    "'simulate_scene' must be the second import to not break the renderers"
)

import concurrent.futures
import logging
from pathlib import Path

from revolve2.simulation.scene import SimulationState
from revolve2.simulation.simulator import Batch, Simulator

from ._simulate_manual_scene import (
    simulate_manual_scene,
)
from .viewers import ViewerType


class LocalSimulator(Simulator):
    """Simulator using MuJoCo."""

    _headless: bool
    _start_paused: bool
    _num_simulators: int
    _cast_shadows: bool
    _fast_sim: bool
    _manual_control: bool
    _viewer_type: ViewerType

    def __init__(
        self,
        viewer_type: ViewerType | str = ViewerType.CUSTOM,
        num_simulators: int = 1,
        *,
        headless: bool = False,
        start_paused: bool = False,
        cast_shadows: bool = False,
        fast_sim: bool = False,
        manual_control: bool = False,
    ) -> None:
        """Initialize this object.

        :param headless: If True, the simulation will not be rendered.
            This drastically improves performance.
        :param start_paused: If True, start the simulation paused. Only
            possible when not in headless mode.
        :param num_simulators: The number of simulators to deploy in
            parallel. They will take one core each but will share space
            on the main python thread for calculating control.
        :param cast_shadows: Whether shadows are cast in the simulation.
        :param fast_sim: Whether more complex rendering prohibited.
        :param manual_control: Whether the simulation should be
            controlled manually.
        :param viewer_type: The viewer-implementation to use in the
            local simulator.
        """
        if not (headless or num_simulators == 1):
            msg = "Cannot have parallel simulators when visualizing."
            raise ValueError(msg)

        if headless and start_paused:
            msg = "Cannot start simulation paused in headless mode."
            raise ValueError(msg)

        self._headless = headless
        self._start_paused = start_paused
        self._num_simulators = num_simulators
        self._cast_shadows = cast_shadows
        self._fast_sim = fast_sim
        self._manual_control = manual_control
        self._viewer_type = (
            ViewerType.from_string(viewer_type)
            if isinstance(viewer_type, str)
            else viewer_type
        )

    def simulate_batch(self, batch: Batch) -> list[list[SimulationState]]:
        """Simulate the provided batch by simulating each contained scene.

        :param batch: The batch to run.
        :type batch: Batch
        :returns: List of simulation states in ascending order of time.
        :rtype: list[list[SimulationState]]
        :raises Exception: If manual control is selected, but headless
            is enabled.

        """
        logging.info("Starting simulation batch with MuJoCo.")

        control_step = 1.0 / batch.parameters.control_frequency
        sample_step = (
            None
            if batch.parameters.sampling_frequency is None
            else 1.0 / batch.parameters.sampling_frequency
        )
        if batch.record_settings is not None:
            path_to_video = Path(batch.record_settings.video_directory)
            path_to_video.mkdir(
                exist_ok=batch.record_settings.overwrite,
            )

        if self._manual_control:
            if self._headless:
                msg = "Manual control only works with rendered simulations. Please disable headless mode."
                raise ValueError(msg)
            for scene in batch.scenes:
                simulate_manual_scene(scene=scene)
            return [[]]

        if self._num_simulators > 1:
            with concurrent.futures.ProcessPoolExecutor(
                max_workers=self._num_simulators
            ) as executor:
                futures = [
                    executor.submit(
                        # This is the function to call, followed by the parameters of the function
                        simulate_scene,
                        viewer_type=self._viewer_type,
                        scene_id=scene_index,
                        scene=scene,
                        record_settings=batch.record_settings,
                        control_step=control_step,
                        sample_step=sample_step,
                        simulation_time=batch.parameters.simulation_time,
                        simulation_timestep=batch.parameters.simulation_timestep,
                        integrator=batch.parameters.integrator,
                        headless=self._headless,
                        start_paused=self._start_paused,
                        cast_shadows=self._cast_shadows,
                        fast_sim=self._fast_sim,
                    )
                    for scene_index, scene in enumerate(batch.scenes)
                ]
                results = [future.result() for future in futures]
        else:
            results = [
                simulate_scene_minimal(
                    viewer_type=self._viewer_type,
                    scene_id=scene_index,
                    scene=scene,
                    record_settings=batch.record_settings,
                    control_step=control_step,
                    sample_step=sample_step,
                    simulation_time=batch.parameters.simulation_time,
                    simulation_timestep=batch.parameters.simulation_timestep,
                    integrator=batch.parameters.integrator,
                    headless=self._headless,
                    start_paused=self._start_paused,
                    cast_shadows=self._cast_shadows,
                    fast_sim=self._fast_sim,
                )
                for scene_index, scene in enumerate(batch.scenes)
            ]

        logging.info("Finished batch.")

        return results
