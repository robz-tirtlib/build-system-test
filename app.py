from __future__ import annotations

from typing import Iterable, Iterator

import yaml

from pathlib import Path

# TODO: redefinition of tasks.yaml and builds.yaml paths
# TODO: parsing input arguments


class Task:

    def __init__(self, name: str, dependencies: list[Task] = None) -> None:
        self.name: str = name
        self.dependencies: list[Task] = [] if dependencies is None else dependencies

    def add_dependency(self, dependency: Task) -> None:
        self.dependencies.append(dependency)


class Tasks:

    def __init__(self, tasks: Iterable[Task] = None) -> None:
        self._tasks: list[Task] = []

        if tasks is not None:
            self.add_tasks(tasks)

    def add_tasks(self, tasks: Iterable[Task]) -> None:
        for task in tasks:
            self._tasks.append(task)

    def add_task(self, task: Task) -> None:
        self._tasks.append(task)

    def get_task(self, name: str) -> Task | None:
        for task in self._tasks:
            if task.name == name:
                return task

    def __iter__(self) -> Iterator:
        self._i = 0
        self._tasks_frozen = self._tasks[:]
        return self

    def __next__(self) -> Task:
        if self._i < len(self._tasks_frozen):
            self._i += 1
            return self._tasks_frozen[self._i - 1]

        raise StopIteration


class Build:
    name: str
    tasks: list[str]


tasks_path: Path = Path("tasks.yaml")
builds_path: Path = Path("builds.yaml")


def parse_task(task: dict, tasks: Tasks) -> Task:
    if "name" not in task:
        raise ValueError("All tasks should have name attribute.")

    name = task["name"]

    if "dependencies" not in task:
        raise ValueError(f"Task {name} is missing dependencies.")

    current_task = tasks.get_task(name)

    if current_task is None:
        current_task = Task(name)
        tasks.add_task(current_task)

    for dependency_name in task["dependencies"]:
        dependency_task = tasks.get_task(dependency_name)

        if dependency_task is None:
            dependency_task = Task(dependency_name)
            tasks.add_task(dependency_task)

        current_task.add_dependency(dependency_task)

    return current_task


def parse_tasks(tasks_path: Path) -> Tasks:
    tasks: Tasks = Tasks()

    with open(tasks_path, 'r') as file:
        tasks_data = yaml.safe_load(file)

        if "tasks" not in tasks_data:
            raise ValueError("No tasks found.")

        for task in tasks_data["tasks"]:
            task = parse_task(task, tasks)
            tasks.add_task(task)

    return tasks


tasks: Tasks = parse_tasks(tasks_path)

for task in tasks:
    print(task.n)
