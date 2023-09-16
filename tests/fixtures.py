import pytest

from tasks import Tasks
from builds import Builds
from conftest import TEST_TASKS_PATH, TEST_BUILDS_PATH


@pytest.fixture
def tasks():
    _tasks: Tasks = Tasks()
    _tasks.parse_tasks(TEST_TASKS_PATH)
    _tasks.sort()
    yield _tasks


@pytest.fixture
def builds(tasks: Tasks):
    _builds: Builds = Builds()
    _builds.parse_builds(TEST_BUILDS_PATH, tasks)
    yield _builds
