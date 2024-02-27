import numpy as np
import numpy.typing as npt

from ..._modular_robot_control_interface import ModularRobotControlInterface
from ...body.base import ActiveHinge
from ...sensor_state._modular_robot_sensor_state import ModularRobotSensorState
from .._brain_instance import BrainInstance

NP_ARRAY = npt.NDArray[np.float64]


class BrainCpgInstance(BrainInstance):
    """
    Cpg network brain.

    A state array that is integrated over time following the differential equation `X'=WX`.
    W is a weight matrix that is multiplied by the state array.
    The outputs of the controller are defined by the `outputs`, a list of indices for the state array.
    """

    _initial_state: NP_ARRAY
    _weight_matrix: NP_ARRAY
    # nxn matrix matching number of neurons
    _output_mapping: list[tuple[int, ActiveHinge]]

    def __init__(
        self,
        initial_state: NP_ARRAY,
        weight_matrix: NP_ARRAY,
        output_mapping: list[tuple[int, ActiveHinge]],
    ) -> None:
        """
        Initialize this object.

        :param initial_state: The initial state of the neural network.
        :param weight_matrix: The weight matrix used during integration.
        :param output_mapping: Marks neurons as controller outputs and map them to the correct active hinge.
        """
        assert initial_state.ndim == 1
        assert weight_matrix.ndim == 2
        assert weight_matrix.shape[0] == weight_matrix.shape[1]
        assert initial_state.shape[0] == weight_matrix.shape[0]
        assert all(
            i >= 0 and i < len(initial_state) for i, _ in output_mapping
        )

        # Stabilise the state by integrating it for a while.
        # TODO find a faster way to stabilise the state
        for _ in range(200):
            initial_state, _ = self._newtown_raphson(
                initial_state, weight_matrix, 0.05
            )
            initial_state = np.clip(initial_state, -1, 1)

        self._state = initial_state
        self._weight_matrix = weight_matrix
        self._output_mapping = output_mapping

    @staticmethod
    def _rk45(
        state: NP_ARRAY,
        a_mat: NP_ARRAY,
        dt: float,
    ) -> NP_ARRAY:
        a_mat_1: NP_ARRAY = np.matmul(a_mat, state)
        a_mat_2: NP_ARRAY = np.matmul(a_mat, (state + dt / 2 * a_mat_1))
        a_mat_3: NP_ARRAY = np.matmul(a_mat, (state + dt / 2 * a_mat_2))
        a_mat_4: NP_ARRAY = np.matmul(a_mat, (state + dt * a_mat_3))
        delta = dt / 6 * (a_mat_1 + 2 * (a_mat_2 + a_mat_3) + a_mat_4)
        return state + delta, delta

    @staticmethod
    def _newtown_raphson(state: NP_ARRAY, A: NP_ARRAY, dt: float) -> NP_ARRAY:
        delta = np.matmul(A, state) * dt
        return state + delta, delta

    def control(
        self,
        dt: float,
        sensor_state: ModularRobotSensorState,
        control_interface: ModularRobotControlInterface,
    ) -> None:
        """
        Control the modular robot.

        Sets the active hinge targets to the values in the state array as defined by the mapping provided in the constructor.

        :param dt: Elapsed seconds since last call to this function.
        :param sensor_state: Interface for reading the current sensor state.
        :param control_interface: Interface for controlling the robot.
        """
        # Integrate ODE to obtain new state.
        # self._state, delta = self._rk45(self._state, self._weight_matrix, dt)
        self._state, delta = self._newtown_raphson(
            self._state, self._weight_matrix, dt
        )
        self._state = np.clip(self._state, -1, 1)

        # Set active hinge targets to match newly calculated state.
        for state_index, active_hinge in self._output_mapping:
            control_interface.set_active_hinge_target(
                active_hinge,
                float(delta[state_index]),
            )
