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


def _detect_optional_arguments(config: dict[str, dict]):
    import sys
    positional_args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]
    results = {}
    for name, attr in config.items():
        pos = attr["position"]
        possible_values = attr["possible_values"]
        results[name] = (
            len(positional_args) > pos and positional_args[pos].upper() in possible_values
        )
    return results


def _parse_args() -> CliArgs:
    optional_args = _detect_optional_arguments(
        {"quantifier": {"position": 2, "possible_values": ["ANY", "EVERY"]}}
    )
    has_quantifier = optional_args.get("quantifier")

    parser = ArgumentParser(
        prog="web_valueist",
        usage="web_valueist [-h] [--debug] [--json] url parser_name [quantifier] selector operator_name value",
        description="""Fetches  the value from the web, compares 
        it with a given value and exits with zero exit code 
        if the condition is satisfied """,
        epilog="Did somebody say cron jobs? Have fun!",
    )

    _ = parser.add_argument("url", help="The URL to fetch")
    _ = parser.add_argument(
        "parser_name", help="The name of the parser to use (e.g., int, str, bool, float)"
    )

    if has_quantifier:
        _ = parser.add_argument(
            "quantifier", help="Quantifier for multiple matches (ANY or EVERY)"
        )

    _ = parser.add_argument("selector", help="The CSS selector to find the value")
    _ = parser.add_argument(
        "operator_name",
        help="The operator to use for comparison (e.g., gt, lt, eq, ne, !=)",
    )
    _ = parser.add_argument("value", help="The reference value to compare against")

    _ = parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    _ = parser.add_argument(
        "--json", action="store_true", help="Output input and result as JSON"
    )

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
