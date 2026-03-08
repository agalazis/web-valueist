#!/usr/bin/env python3
import logging
import web_valueist
from argparse import ArgumentParser
from typing import TypedDict, Unpack
from signal import signal, SIGTERM
logger = logging.getLogger(__name__)


class Args(TypedDict):
    url: str
    selector: str
    parser_name: web_valueist.Parser
    operator_name: web_valueist.Operator
    value: str
    quantifier: str


class CliArgs(Args):
    debug: bool
    json: bool


def _parse_args() -> CliArgs:
    import sys

    # Peek at arguments to determine if a quantifier is present
    # Skip script name (sys.argv[0]) and check 3rd positional argument (sys.argv[3])
    # Note: flags like --debug might be mixed in, but standard usage is positional first

    # A more robust way to peek at positional arguments ignoring flags
    positional_args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]

    has_quantifier = len(positional_args) >= 3 and positional_args[2].upper() in ["ANY", "EVERY"]

    parser = ArgumentParser(
        prog="web_valueist",
        description="""Fetches  the value from the web, compares 
        it with a given value and exits with zero exit code 
        if the condition is satisfied """,
        epilog="Did somebody say cron jobs? Have fun!",
    )

    _ = parser.add_argument("url")
    _ = parser.add_argument("parser_name")

    if has_quantifier:
        _ = parser.add_argument("quantifier")

    _ = parser.add_argument("selector")
    _ = parser.add_argument("operator_name")
    _ = parser.add_argument("value")

    _ = parser.add_argument("--debug", action="store_true")
    _ = parser.add_argument("--json", action="store_true")

    args = parser.parse_args().__dict__

    if not has_quantifier:
        args["quantifier"] = "ANY"
    else:
        args["quantifier"] = args["quantifier"].upper()

    return args


def _initialize_logger(debug: bool, **otherArgs: Unpack[Args]) -> Args:
    logging.basicConfig()
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)
    return otherArgs


def _initialize_cli():
    args = _parse_args()
    return _initialize_logger(**args)


def sigterm_handler(_, __):
    logger.error("termination requested, bye...\n")
    raise SystemExit(1)


def main():
    import json
    import sys
    args=_initialize_cli()
    json_output = args.pop("json")
    result = web_valueist.evaluate(**args)
    if json_output:
        print(json.dumps({"args": args, "result": result}))
    if result["success"]:
        sys.exit(0)
    sys.exit(1)


def __main__():
    signal(SIGTERM, sigterm_handler)

    try:
        main()
    except KeyboardInterrupt:
        logger.error("ok, bye...\n")
        exit(1)
    except web_valueist.ValueistException as e:
        logger.error(f"Error: {e}")
        exit(1)


if __name__ == "__main__":
    __main__()
