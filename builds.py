from tasks import Task, Tasks

import yaml

from pathlib import Path


class Build:

    def __init__(self, name: str, tasks: list[Task] = None) -> None:
        self.name: str = name
        self.tasks: Tasks = Tasks()

        if tasks is not None:
            self.tasks = Tasks(tasks)

    def get_tasks(self) -> list[Task]:
        return list(sorted(self.tasks, key=lambda task: task.id))

    def add_task(self, task: Task) -> None:
        self.tasks.add_task(task)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            raise ValueError

        return self.name == other.name


class BuildsIterator:

    def __init__(self, builds: list[Build]) -> None:
        self._builds: list[Build] = builds
        self._i = 0

    def __next__(self) -> Build:
        if self._i < len(self._builds):
            self._i += 1
            return self._builds[self._i - 1]

        raise StopIteration


class Builds:

    def __init__(self, builds: list[Build] = None) -> None:
        self._builds: list[Build] = []

        if builds is not None:
            for build in builds:
                self.add_build(build)

    def get_build(self, name: str) -> Build | None:
        for build in self._builds:
            if build.name == name:
                return build

    def parse_builds(self, builds_path: Path, tasks: Tasks) -> None:
        with open(builds_path, 'r') as file:
            builds_data = yaml.safe_load(file)

            if "builds" not in builds_data:
                raise ValueError("No builds found.")

            for build in builds_data["builds"]:
                self._parse_build(build, tasks)

    def _parse_build(self, build: dict, tasks: Tasks) -> None:
        if "name" not in build:
            raise ValueError("All builds should have name attribute.")

        name = build["name"]

        if "tasks" not in build:
            raise ValueError(f"Build {name} does not have tasks.")

        current_build = Build(name)

        for task in build["tasks"]:
            task_obj = tasks.get_task(task)

            if task_obj is None:
                error_msg = f"Task {task} was not mentioned intasks file."
                raise ValueError(error_msg)

            current_build.add_task(task_obj)

        self.add_build(current_build)

    def add_build(self, build: Build) -> None:
        self._builds.append(build)

    def __iter__(self) -> BuildsIterator:
        return BuildsIterator(self._builds[:])
