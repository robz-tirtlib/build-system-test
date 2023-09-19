from pathlib import Path

test_data_prefix = Path("tests", "data")

TEST_TASKS_PATH = test_data_prefix / Path("test_tasks.yaml")
TEST_CYCLIC_TASKS_PATH = test_data_prefix / Path("test_cycle_tasks.yaml")
TEST_BUILDS_PATH = test_data_prefix / Path("test_builds.yaml")

from tests.fixtures import tasks, builds  # noqa
