from __future__ import annotations

from typing import Iterable

import yaml

from pathlib import Path

from utils import convert_dict_args_to_str


class Task:

    def __init__(self, name: str, dependencies: list[Task] = None) -> None:
        self.name: str = name
        self.id: int | None = None
        self.dependencies: list[Task] = []

        if dependencies:
            self.dependencies = dependencies

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

    def parse_tasks(self, tasks_path: Path) -> None:
        with open(tasks_path, 'r') as file:
            tasks_data = convert_dict_args_to_str(yaml.safe_load(file))

            if "tasks" not in tasks_data:
                raise ValueError("No tasks found.")

            for task in tasks_data["tasks"]:
                self._parse_task(task)

        self._detect_cyclic_dependencies()

    def _detect_cyclic_dependencies(self) -> None:
        cycle = True
        for task in self._tasks:
            if not task.dependencies:
                self._dfs(task, set(), set())
                cycle = False

        if cycle:
            raise ValueError("Cyclic dependencies are detected.")

    def _dfs(self, cur_task: Task, visited: set[str],
             cur_path: set[str]) -> None:
        if cur_task.name in cur_path:
            raise ValueError("Cyclic dependencies are detected.")

        visited.add(cur_task.name)
        cur_path.add(cur_task.name)

        for dependency in cur_task.dependencies:
            if dependency.name not in visited:
                self._dfs(dependency, visited, cur_path)

        cur_path.remove(cur_task.name)

    def _parse_task(self, task: dict) -> None:
        if "name" not in task:
            raise ValueError("All tasks should have name attribute.")

        name = task["name"]

        if "dependencies" not in task:
            raise ValueError(f"Task {name} is missing dependencies.")

        current_task = self.get_task(name)

        if current_task is None:
            current_task = Task(name)
            self.add_task(current_task)

        for dependency_name in task["dependencies"]:
            dependency_task = self.get_task(dependency_name)

            if dependency_task is None:
                dependency_task = Task(dependency_name)
                self.add_task(dependency_task)

            current_task.add_dependency(dependency_task)

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

        for current_task in self._tasks:
            if not current_task.dependencies:
                self._sort_component(current_task, val)
                val += 1

    def _sort_component(self, current_task: Task, cur_id: int) -> None:
        if current_task.id is None or current_task.id < cur_id:
            current_task.id = cur_id

        for task in self._tasks:
            if current_task in task.dependencies:
                self._sort_component(task, cur_id + 1)

    def __iter__(self) -> TasksIterator:
        return TasksIterator(self._tasks[:])
