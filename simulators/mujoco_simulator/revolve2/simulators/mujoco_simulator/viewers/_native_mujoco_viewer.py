"""The native rendering viewer for mujoco."""

from collections.abc import Callable
from typing import Any

import mujoco.viewer
from mujoco.viewer import Handle
from revolve2.simulation.simulator import Viewer


class NativeMujocoViewer(Viewer):  # type: ignore[misc]
    # TODO(jmdm): Fix type ignore"↑"
    """Native Viewer Object."""

    _viewer: Handle
    _model: mujoco.MjModel
    _data: mujoco.MjData

    def __init__(
        self,
        model: mujoco.MjModel,
        data: mujoco.MjData,
        *,
        key_callback: Callable[[int], None] | None = None,
        **_: Any,
    ) -> None:
        """
        Initialize the Viewer.

        :param model: The mujoco models.
        :param data: The mujoco data.
        :param key_callback: A key callback listener.
        :param _: Some unused kwargs.
        """
        self._model = model
        self._data = data
        self._viewer = mujoco.viewer.launch_passive(
            model,
            data,
            key_callback=key_callback,
        )

    def render(self) -> int | None:
        """
        Render the scene.

        :return: A cycle position if applicable.
        """
        self._viewer.sync()
        return None

    def close_viewer(self) -> None:
        """Close the viewer."""
        self._viewer.close()

    def current_viewport_size(self) -> tuple[int, int]:
        """
        Grabs the *current* viewport size (and updates the cached values).

        :raises NotImplementedError: As it is not implemented.
        """
        msg = "current_viewport_size is not implemented for the native mujoco viewer yet."
        raise NotImplementedError(msg)

    @property
    def context(self) -> mujoco.MjrContext:
        """
        Get the context.

        :returns: The context.
        """
        return mujoco.MjrContext(
            self._model, mujoco.mjtFontScale.mjFONTSCALE_150.value
        )

    @property
    def view_port(self) -> mujoco.MjrRect:
        """
        Get the view port.

        :raises NotImplementedError: As it is not implemented.
        """
        msg = "view_port is not implemented for the native mujoco viewer yet."
        raise NotImplementedError(msg)

    @property
    def can_record(self) -> bool:
        """
        Return False.

        :returns: False.
        """
        return False
