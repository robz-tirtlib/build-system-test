from pathlib import Path


def convert_dict_args_to_str(data: dict) -> dict:
    for key, val in data.items():
        if isinstance(val, (int, float)):
            data[key] = str(val)

        if isinstance(val, list):
            convert_list_args_to_str(val)

    return data


def convert_list_args_to_str(data: list) -> None:
    for i, item in enumerate(data):
        if isinstance(item, list):
            convert_list_args_to_str(item)

        if isinstance(item, (int, float)):
            data[i] = str(item)

        if isinstance(item, dict):
            convert_dict_args_to_str(item)


def validate_cli_args(args: dict) -> dict:
    if args["<list_arg>"]:
        if args["<list_arg>"] not in ["tasks", "builds"]:
            raise ValueError(
                "Command 'list' accepts only these arguments: tasks, builds.")

    if args["<get_primary_arg>"]:
        if args["<get_primary_arg>"] not in ["build", "task"]:
            raise ValueError(
                "Argument of 'get' command could only be 'build' or 'task'.")

    tasks_path = Path(args["--tasks-path"])

    if not tasks_path.exists():
        raise ValueError("Incorrect path to tasks.yaml file.")

    builds_path = Path(args["--builds-path"])

    if not builds_path.exists():
        raise ValueError("Incorrect path to builds.yaml file.")

    return args


def get_paths(args: dict) -> tuple[Path]:
    return Path(args["--tasks-path"]), Path(args["--builds-path"])
