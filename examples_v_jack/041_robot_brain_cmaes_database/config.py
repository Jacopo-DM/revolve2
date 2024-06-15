"""Configuration parameters for this example."""

from revolve2.ci_group.modular_robots_v2 import runner

DATABASE_FILE = "database.sqlite"
NUM_REPETITIONS = 1
NUM_SIMULATORS = 16
INITIAL_STD = 0.5
NUM_GENERATIONS = 50
BODY = runner()
