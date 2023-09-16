from __future__ import annotations

from pathlib import Path

from tasks import Tasks
from builds import Builds

# TODO: detect cyclic dependencies
# TODO: redefinition of tasks.yaml and builds.yaml paths
# TODO: parsing input arguments


tasks_path: Path = Path("test_tasks.yaml")
builds_path: Path = Path("test_builds.yaml")


if __name__ == "__main__":
    tasks: Tasks = Tasks()
    tasks.parse_tasks(tasks_path)
    tasks.sort()
    builds: Builds = Builds()
    builds.parse_builds(builds_path, tasks)
