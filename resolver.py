from tasks import Tasks
from builds import Builds


class Resolver:

    def __init__(self, args: dict, tasks: Tasks, builds: Builds) -> None:
        self._args: dict = args
        self._tasks: Tasks = tasks
        self._builds: Builds = builds

    def answer_user(self) -> None:
        if self._args["list"]:
            self._list_command(self._args["<list_arg>"])
        elif self._args["get"]:
            self._get_command(self._args["<get_primary_arg>"],
                              self._args["<get_secondary_arg>"])

    def _list_command(self, list_type: str) -> None:
        if list_type == "tasks":
            self._list_tasks()
        elif list_type == "builds":
            self._list_builds()

    def _list_builds(self) -> None:
        print("List of available builds:")
        for build in self._builds:
            print(f" * {build.name}")

    def _list_tasks(self) -> None:
        print("List of available tasks:")
        for task in self._tasks:
            print(f" * {task.name}")

    def _get_command(self, get_type: str, arg: str) -> None:
        if get_type == "task":
            self._get_task_command(arg)
        elif get_type == "build":
            self._get_build_command(arg)

    def _get_build_command(self, build_name: str) -> None:
        build = self._builds.get_build(build_name)

        if build is None:
            raise ValueError(f"Build '{build_name}' not found.")

        print("Build info:")
        print(f" * name: {build_name}")

        tasks = ", ".join([task.name for task in build.tasks])

        print(f" * tasks: {tasks}")

    def _get_task_command(self, task_name: str) -> None:
        task = self._tasks.get_task(task_name)

        if task is None:
            raise ValueError(f"Task '{task_name}' not found.")

        print("Task info:")
        print(f" * name: {task.name}")

        if not task.dependencies:
            print(" * dependencies: None")
            return

        dependencies = ", ".join([dep.name for dep in task.dependencies])

        print(f" * dependencies: {dependencies}")
