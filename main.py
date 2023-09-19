from __future__ import annotations

from docopt import docopt

from tasks import Tasks
from builds import Builds
from resolver import Resolver

from utils import validate_cli_args, get_paths

from docopt_message import doc


if __name__ == "__main__":
    args = validate_cli_args(docopt(doc))
    tasks_path, builds_path = get_paths(args)

    tasks: Tasks = Tasks()
    tasks.parse_tasks(tasks_path)
    tasks.sort()
    builds: Builds = Builds()
    builds.parse_builds(builds_path, tasks)

    resolver: Resolver = Resolver(args, tasks, builds)
    resolver.answer_user()
