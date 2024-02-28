from dataclasses import dataclass
from queue import Queue
from typing import Any

import multineat
import numpy as np
from numpy.typing import NDArray
from pyrr import Quaternion, Vector3
from revolve2.modular_robot.body import AttachmentPoint, Module
from revolve2.modular_robot.body.v2 import ActiveHingeV2, BodyV2, BrickV2

MAX_PARTS = 20
GRID_SIZE = MAX_PARTS * 2 + 1


@dataclass
class __Module:
    position: Vector3[np.int_]
    forward: Vector3[np.int_]
    up: Vector3[np.int_]
    chain_length: int
    module_reference: Module


def develop(
    genotype: multineat.Genome,
) -> BodyV2:
    """
    Develop a CPPNWIN genotype into a modular robot body.

    It is important that the genotype was created using a compatible function.

    :param genotype: The genotype to create the body from.
    :returns: The created body.
    """

    body_net = multineat.NeuralNetwork()
    genotype.BuildPhenotype(body_net)

    to_explore: Queue[__Module] = Queue()
    grid = np.zeros(
        shape=(GRID_SIZE, GRID_SIZE, GRID_SIZE),
        dtype=np.uint8,
    )

    body = BodyV2()

    v2_core = body.core_v2
    core_position = Vector3(
        [MAX_PARTS + 1, MAX_PARTS + 1, MAX_PARTS + 1], dtype=np.int_
    )

    for attachment_face in v2_core.attachment_faces.values():
        to_explore.put(
            __Module(
                core_position,
                Vector3([0, -1, 0], dtype=np.int_),
                Vector3([0, 0, 1], dtype=np.int_),
                0,
                attachment_face,
            )
        )
    grid[tuple(core_position)] = 1
    part_count = 1

    while not to_explore.empty():
        module = to_explore.get()
        attachment_dict = module.module_reference.attachment_points.items()
        for attachment_point_tuple in attachment_dict:
            if part_count < MAX_PARTS:
                child = __add_child(
                    body_net, module, attachment_point_tuple, grid
                )
                if child is not None:
                    to_explore.put(child)
                    part_count += 1
    return body


def softmax(x: np.ndarray) -> np.ndarray:
    """
    Compute softmax values for each sets of scores in x.

    :param x: The input array.
    :returns: The softmax array.
    """
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum(axis=0)


def __evaluate_cppn(
    body_net: multineat.NeuralNetwork,
    position: Vector3[np.int_],
    chain_length: int,
) -> tuple[Any, int]:
    """
    Get module type and orientation from a multineat CPPN network.

    :param body_net: The CPPN network.
    :param position: Position of the module.
    :param chain_length: Tree distance of the module from the core.
    :returns: (module type, rotation_index)
    """
    x, y, z = position

    assert isinstance(
        x, np.int_
    ), f"Error: The position is not of type int. Type: {type(x)}."

    # normalize position by grid size
    x /= GRID_SIZE
    y /= GRID_SIZE
    z /= GRID_SIZE
    chain_length /= MAX_PARTS

    # 1.0 is the bias input
    body_net.Input([1.0, x, y, z, chain_length])
    body_net.ActivateAllLayers()
    outputs = body_net.Output()

    # ========= Set up ========= #
    rng = np.random.default_rng()
    types = {0: None, 1: BrickV2, 2: ActiveHingeV2}
    idxs_1 = list(types.keys())
    idxs_2 = [3, 4]

    # ========= get module type from output probabilities ========= #
    type_probs = softmax(np.array(outputs)[idxs_1])
    # idx = rng.choice(idxs_1, p=type_probs)
    idx = np.argmax(type_probs)
    # [ ] Argmin ?
    module_type = types[idx]

    # ========= get rotation from output probabilities ========= #
    rotation_probs = softmax(np.array(outputs)[idxs_2])
    # rotation_index = rng.choice(idxs_2, p=rotation_probs)
    # [ ] Argmin ?
    rotation_index = np.argmax(rotation_probs)
    return module_type, rotation_index


def __add_child(
    body_net: multineat.NeuralNetwork,
    module: __Module,
    attachment_point_tuple: tuple[int, AttachmentPoint],
    grid: NDArray[np.uint8],
) -> __Module | None:
    attachment_index, attachment_point = attachment_point_tuple

    forward = __rotate(module.forward, module.up, attachment_point.orientation)
    position = __vec3_int(module.position + forward)
    chain_length = module.chain_length + 1

    new_pos = np.array(
        np.round(position + attachment_point.offset), dtype=np.int64
    )

    child_type, child_rotation = __evaluate_cppn(
        body_net, new_pos, chain_length
    )

    # if grid cell is occupied, don't make a child
    # else, set cell as occupied
    # ERROR this is MAJOR bug!
    #   The core has 4 faces with 8 attachment points each,
    #       however, all 8 share share the same "position + forward" !
    #   This means that the core will always attach to the first position
    #       when the cppn returns "not None" -> aka "top"
    if grid[tuple(position)] > 0:
        return None

    if child_type is None:
        return None

    angle = child_rotation * (np.pi / 2.0)
    child = child_type(angle)

    if not module.module_reference.can_set_child(child, attachment_index):
        return None

    up = __rotate(module.up, forward, Quaternion.from_eulers([angle, 0, 0]))
    module.module_reference.set_child(child, attachment_index)
    grid[tuple(position)] += 1

    return __Module(
        position,
        forward,
        up,
        chain_length,
        child,
    )


def __rotate(a: Vector3, b: Vector3, rotation: Quaternion) -> Vector3:
    """
    Rotates vector a a given angle around b.

    :param a: Vector a.
    :param b: Vector b.
    :param rotation: The quaternion for rotation.
    :returns: A copy of a, rotated.
    """
    cos_angle: int = int(round(np.cos(rotation.angle)))
    sin_angle: int = int(round(np.sin(rotation.angle)))

    vec: Vector3 = (
        a * cos_angle + sin_angle * b.cross(a) + (1 - cos_angle) * b.dot(a) * b
    )
    return vec


def __vec3_int(vector: Vector3) -> Vector3[np.int_]:
    """
    Cast a Vector3 object to an integer only Vector3.

    :param vector: The vector.
    :return: The integer vector.
    """
    x, y, z = (int(round(v)) for v in vector)
    return Vector3([x, y, z], dtype=np.int64)
