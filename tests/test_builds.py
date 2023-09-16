from tasks import Task
from builds import Builds, Build


def test_builds_created(builds: Builds):
    first: Build = builds.get_build("first")

    builds_names = ["first", "second"]

    for build in builds:
        builds_names.remove(build.name)

    assert builds_names == []
    assert first.get_tasks() == [Task(1), Task(3), Task(4)]

    second: Build = builds.get_build("second")

    assert second.get_tasks()[-1] == Task(8)
