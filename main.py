from __future__ import annotations

from typing import Iterable

import yaml

from pathlib import Path

# TODO: detect cyclic dependencies
# TODO: redefinition of tasks.yaml and builds.yaml paths
# TODO: parsing input arguments


class Task:

    def __init__(self, name: str, dependencies: list[Task] = None) -> None:
        self.name: str = name
        self.dependencies: list[Task] = [] if dependencies is None else dependencies
        self.id: int | None = None

    def add_dependency(self, dependency: Task) -> None:
        self.dependencies.append(dependency)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            raise ValueError

        return self.name == other.name


class TasksIterator:

    def __init__(self, tasks: list[Task]) -> None:
        self._tasks: list[Task] = tasks
        self._i = 0

    def __next__(self) -> Task:
        if self._i < len(self._tasks):
            self._i += 1
            return self._tasks[self._i - 1]

        raise StopIteration


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

    def sort(self) -> None:
        val = 0

        for current_task in tasks:
            in_dependencies = False

            for task in tasks:
                if current_task == task:
                    continue

                if current_task in task.dependencies:
                    in_dependencies = True
                    break

            if not in_dependencies:
                self._sort_component(current_task, val)
                val += 1

    def _sort_component(self, current_task: Task, cur_id: int) -> None:
        if current_task.id is None or current_task.id < cur_id:
            current_task.id = cur_id

        for dependency in current_task.dependencies:
            self._sort_component(dependency, cur_id + 1)

    def __iter__(self) -> TasksIterator:
        return TasksIterator(self._tasks[:])


class Build:
    name: str
    tasks: list[str]


tasks_path: Path = Path("tasks.yaml")
builds_path: Path = Path("builds.yaml")


def parse_task(task: dict, tasks: Tasks) -> None:
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


def parse_tasks(tasks_path: Path) -> Tasks:
    tasks: Tasks = Tasks()

    with open(tasks_path, 'r') as file:
        tasks_data = yaml.safe_load(file)

        if "tasks" not in tasks_data:
            raise ValueError("No tasks found.")

        for task in tasks_data["tasks"]:
            task = parse_task(task, tasks)

    return tasks


if __name__ == "__main__":
    tasks: Tasks = parse_tasks(tasks_path)
    tasks.sort()
