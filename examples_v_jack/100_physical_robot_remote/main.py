"""An example on how to remote control a physical modular robot."""

import logging

from revolve2.experimentation.logging import setup_logging
from revolve2.experimentation.rng import make_rng_time_seed
from revolve2.modular_robot import ModularRobot
from revolve2.modular_robot.body import RightAngles
from revolve2.modular_robot.body.base import ActiveHinge
from revolve2.modular_robot.body.v1 import ActiveHingeV1, BodyV1, BrickV1
from revolve2.modular_robot.brain.cpg import BrainCpgNetworkNeighborRandom
from revolve2.modular_robot_physical import Config, UUIDKey
from revolve2.modular_robot_physical.remote import run_remote


def make_body() -> (
    tuple[BodyV1, tuple[ActiveHinge, ActiveHinge, ActiveHinge, ActiveHinge]]
):
    """
    Create a body for the robot.

    :returns: The created body and a tuple of all ActiveHinge objects for mapping later on.
    """
    # A modular robot body follows a 'tree' structure.
    # The 'Body' class automatically creates a center 'core'.
    # From here, other modular can be attached.
    # Modules can be attached in a rotated fashion.
    # This can be any angle, although the original design takes into account only multiples of 90 degrees.
    body = BodyV1()
    body.core_v1.left = ActiveHingeV1(RightAngles.DEG_0)
    body.core_v1.left.attachment = ActiveHingeV1(RightAngles.DEG_0)
    body.core_v1.left.attachment.attachment = BrickV1(RightAngles.DEG_0)
    body.core_v1.right = ActiveHingeV1(RightAngles.DEG_0)
    body.core_v1.right.attachment = ActiveHingeV1(RightAngles.DEG_0)
    body.core_v1.right.attachment.attachment = BrickV1(RightAngles.DEG_0)

    """Here we collect all ActiveHinges, to map them later onto the physical robot."""
    active_hinges = (
        body.core_v1.left,
        body.core_v1.left.attachment,
        body.core_v1.right,
        body.core_v1.right.attachment,
    )
    return body, active_hinges


def on_prepared() -> None:
    """Do things when the robot is prepared and ready to start the controller."""
    logging.info("Done. Press enter to start the brain.")
    input()


def main() -> None:
    """Remote control a physical modular robot."""
    # Set up logging.
    setup_logging(file_name="log.txt")
    rng = make_rng_time_seed()
    # Create a modular robot, similar to what was done in the 000_simulate_single_robot example. Of course, you can replace this with your own robot, such as one you have optimized using an evolutionary algorithm.
    body, hinges = make_body()
    brain = BrainCpgNetworkNeighborRandom(body=body, rng=rng)
    robot = ModularRobot(body, brain)

    """
    Some important notes to understand:
    - Hinge mappings are specific to each robot, so they have to be created new for each type of body.
    - The pin`s id`s can be found on th physical robots HAT.
    - The order of the pin`s is crucial for a correct translation into the physical robot.
    - Each ActiveHinge needs one corresponding pin to be able to move.
    - If the mapping is faulty check the simulators behavior versus the physical behavior and adjust the mapping iteratively.

    For a concrete implementation look at the following example of mapping the robots`s hinges:
    """
    hinge_1, hinge_2, hinge_3, hinge_4 = hinges
    hinge_mapping = {
        UUIDKey(hinge_1): 21,
        UUIDKey(hinge_2): 26,
        UUIDKey(hinge_3): 20,
        UUIDKey(hinge_4): 21,
    }

    """
    A configuration consists of the follow parameters:
    - modular_robot: The ModularRobot object, exactly as you would use it in simulation.
    - hinge_mapping: This maps active hinges to GPIO pins on the physical modular robot core.
    - run_duration: How long to run the robot for in seconds.
    - control_frequency: Frequency at which to call the brain control functions in seconds. If you also ran the robot in simulation, this must match your setting there.
    - initial_hinge_positions: Initial positions for the active hinges. In Revolve2 the simulator defaults to 0.0.
    - inverse_servos: Sometimes servos on the physical robot are mounted backwards by accident. Here you inverse specific servos in software. Example: {13: True} would inverse the servo connected to GPIO pin 13.
    """
    config = Config(
        modular_robot=robot,
        hinge_mapping=hinge_mapping,
        run_duration=30,
        control_frequency=20,
        initial_hinge_positions={
            UUIDKey(active_hinge): 0.0 for active_hinge in hinges
        },
        inverse_servos={},
    )

    """
    Create a Remote for the physical modular robot.
    Make sure to target the correct hardware type and fill in the correct IP and credentials.
    The debug flag is turned on. If the remote complains it cannot keep up, turning off debugging might improve performance.
    """
    logging.info("Initializing robot..")
    run_remote(
        config=config,
        hostname="localhost",  # "Set the robot IP here.
        debug=True,
        on_prepared=on_prepared,
    )


if __name__ == "__main__":
    main()
