import argparse
import os
import yaml
import keyboard
from datetime import datetime

_RESET_LINE = "\r\033[K\x1B[37m"
_COLOR_GREEN = "\x1B[32m"
_COLOR_WARN = "\x1B[93m"
_COLOR_WHITE = "\x1B[37m"


start_time = datetime.now()


def print_header(header: str):
    print(header)


def print_status(run_number: int, status: str):
    print(
        f"{_RESET_LINE}Run #{run_number:02} ❯ {_COLOR_GREEN}{status}{_COLOR_WHITE} ",
        end="",
    )


def print_paused():
    print(
        f"{_RESET_LINE}❯ {_COLOR_WARN}Paused (press ctrl+c again to exit or ctrl+n to resume){_COLOR_WHITE} ",
        end="",
    )


def print_end(number_of_runs: int):
    print("\n")
    print(f"Number of runs: {number_of_runs}")
    print(f"Uptime: {datetime.now() - start_time}")
    print()


def detect_interrupt():
    return keyboard.is_pressed("ctrl+c")


def detect_resume():
    return keyboard.is_pressed("ctrl+n")


def parse_args() -> dict:
    args = _parser.parse_args()
    settings_file = args.__dict__.pop("settings")

    if settings_file:
        config = _config_from_file(settings_file)
    elif os.path.isfile("settings.yaml"):
        config = _config_from_file("settings.yaml")
    else:
        config = {}

    for k, v in args.__dict__.items():
        if v is None:
            continue
        config.update({k: v})

    return config


def _config_from_file(file: str):
    with open(file) as f:
        settings = yaml.safe_load(f)

    return {**settings}


_parser = argparse.ArgumentParser(description="#vadio fishing bot")


class _IsYamlFile(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if not os.path.isfile(values) and not os.path.basename(values) == ".yaml":
            parser.error(f"Invalid settings file. Got: {values}.")
        setattr(namespace, self.dest, values)


_parser.add_argument(
    "-s",
    "--settings",
    action=_IsYamlFile,
    nargs="?",
    help="settings file path",
)

_parser.add_argument(
    "-c",
    "--cast-time",
    type=float,
    nargs="?",
    help="casting time in seconds (default=1.0)",
)

_parser.add_argument(
    "-b",
    "--equip-bait",
    type=bool,
    nargs="?",
    help="equip bait before casting line (default=False)",
)

_parser.add_argument(
    "-m",
    "--equip-bait-max-retries",
    type=int,
    nargs="?",
    help="max retries for equiping bait (default=3)",
)

_parser.add_argument(
    "-f",
    "--free-cam-key",
    type=bool,
    nargs="?",
    help="free cam keybind (default='alt')",
)

_parser.add_argument(
    "-r",
    "--repair-tool",
    type=bool,
    nargs="?",
    help="repair tool (default='true')",
)

_parser.add_argument(
    "-e",
    "--repair-tool-every",
    type=int,
    nargs="?",
    help="repair tool every n runs (default=30)",
)
