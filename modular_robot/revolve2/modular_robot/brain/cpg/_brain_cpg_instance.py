import numpy as np
import numpy.typing as npt

from ..._modular_robot_control_interface import (
    ModularRobotControlInterface,
)
from ...body.base import ActiveHinge
from ...sensor_state import ModularRobotSensorState
from .._brain_instance import BrainInstance


class BrainCpgInstance(BrainInstance):
    """CPG network brain.

    A state array that is integrated over time following the differential equation `X'=WX`.
    W is a weight matrix that is multiplied by the state array.
    The outputs of the controller are defined by the `outputs`, a list of indices for the state array.
    """

    _initial_state: npt.NDArray[np.float64]
    _weight_matrix: npt.NDArray[np.float64]
    # nxn matrix matching number of neurons
    _output_mapping: list[tuple[int, ActiveHinge]]

    def __init__(
        self,
        initial_state: npt.NDArray[np.float64],
        weight_matrix: npt.NDArray[np.float64],
        output_mapping: list[tuple[int, ActiveHinge]],
    ) -> None:
        """Initialize this CPG Brain Instance.

        :param initial_state: The initial state of the neural network.
        :param weight_matrix: The weight matrix used during integration.
        :param output_mapping: Marks neurons as controller outputs and
            map them to the correct active hinge.
        """
        assert initial_state.ndim == 1
        assert weight_matrix.ndim == 2
        assert weight_matrix.shape[0] == weight_matrix.shape[1]
        assert initial_state.shape[0] == weight_matrix.shape[0]
        assert all(i >= 0 and i < len(initial_state) for i, _ in output_mapping)

        # Stabilise the state by integrating it for a while.
        # WARN very hacky way to stabilise the state
        # [ ] find a faster/better way to stabilise the state
        for _ in range(50):
            initial_state, _ = self._newtown_raphson(
                initial_state, weight_matrix, 0.05
            )

        self._state = initial_state
        self._weight_matrix = weight_matrix
        self._output_mapping = output_mapping

    @staticmethod
    def _rk45(
        state: npt.NDArray[np.float64],
        a_mat: npt.NDArray[np.float64],
        dt: float,
    ) -> tuple[npt.NDArray[np.float64], npt.NDArray[np.float64]]:
        """Calculate the next state using the RK45 method.

        This implementation of the Runge–Kutta–Fehlberg method allows us to improve accuracy of state calculations by comparing solutions at different step sizes.
        For more info see: See https://en.wikipedia.org/wiki/Runge%E2%80%93Kutta%E2%80%93Fehlberg_method.
        RK45 is a method of order 4 with an error estimator of order 5 (Fehlberg, E. (1969). Low-order classical Runge-Kutta formulas with stepsize control. NASA Technical Report R-315.).

        :param state: The current state of the network.
        :type state: npt.NDArray[np.float64]
        :param a_mat:
        :type a_mat: npt.NDArray[np.float64]
        :param dt: The step size (elapsed simulation time).
        :type dt: float
        :returns: The new state.
        :rtype: tuple[npt.NDArray[np.float64],npt.NDArray[np.float64]]
        """
        a_mat_1: npt.NDArray[np.float64] = np.matmul(a_mat, state)
        a_mat_2: npt.NDArray[np.float64] = np.matmul(
            a_mat, (state + dt / 2 * a_mat_1)
        )
        a_mat_3: npt.NDArray[np.float64] = np.matmul(
            a_mat, (state + dt / 2 * a_mat_2)
        )
        a_mat_4: npt.NDArray[np.float64] = np.matmul(
            a_mat, (state + dt * a_mat_3)
        )
        delta = dt / 6 * (a_mat_1 + 2 * (a_mat_2 + a_mat_3) + a_mat_4)
        return np.clip(state + delta, -1, 1), delta

    @staticmethod
    def _newtown_raphson(
        state: npt.NDArray[np.float64], a: npt.NDArray[np.float64], dt: float
    ) -> tuple[npt.NDArray[np.float64], npt.NDArray[np.float64]]:
        """:param state:
        :type state: npt.NDArray[np.float64]
        :param a:
        :type a: npt.NDArray[np.float64]
        :param dt:
        :type dt: float
        :rtype: tuple[npt.NDArray[np.float64],npt.NDArray[np.float64]]
        """
        delta = np.matmul(a, state) * dt
        return np.clip(state + delta, -1, 1), delta

    def control(
        self,
        dt: float,
        sensor_state: ModularRobotSensorState,
        control_interface: ModularRobotControlInterface,
    ) -> None:
        """Control the modular robot.

        Set the active hinge targets to the values in the state array as
        defined by the mapping provided in the constructor.

        :param dt: Elapsed seconds since last call to this function.
        :type dt: float
        :param sensor_state: Interface for reading the current sensor
            state.
        :type sensor_state: ModularRobotSensorState
        :param control_interface: Interface for controlling the robot.
        :type control_interface: ModularRobotControlInterface
        :rtype: None
        """
        # Integrate ODE to obtain new state.
        self._state, delta = self._newtown_raphson(  # _rk45
            self._state, self._weight_matrix, dt
        )

        # Set active hinge targets to match newly calculated state.
        for state_index, active_hinge in self._output_mapping:
            # TODO(jmdm): delta or absolute state?
            # see ../../mujoco_simulator/_control_interface_impl.py
            control_interface.set_active_hinge_target(
                active_hinge,
                float(delta[state_index]) * active_hinge.range,
                # self._state[state_index] delta[state_index]
            )
