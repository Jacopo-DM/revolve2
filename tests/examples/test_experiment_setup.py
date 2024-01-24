import os

from ..conftest import EXAMPLES_DIR, assert_command_succeeds


def test_experiment_setup() -> None:
    """Test 007_experiment_setup example can complete."""
    exp_dir = os.path.join(EXAMPLES_DIR, "007_experiment_setup")
    assert_command_succeeds(["python", os.path.join(exp_dir, "main.py")])
