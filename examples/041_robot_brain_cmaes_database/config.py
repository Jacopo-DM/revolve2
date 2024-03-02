"""Configuration parameters for this example."""

from revolve2.ci_group.modular_robots_v2 import gecko_plus_v2

DATABASE_FILE = "database.sqlite"
NUM_REPETITIONS = 5
NUM_SIMULATORS = 16
INITIAL_STD = 0.5
NUM_GENERATIONS = 10
BODY = gecko_plus_v2()
