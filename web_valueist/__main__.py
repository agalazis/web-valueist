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
    parser = ArgumentParser(
        prog="web_valueist",
        description="""Fetches  the value from the web, compares 
        it with a given value and exits with zero exit code 
        if the condition is satisfied """,
        epilog="Did somebody say cron jobs? Have fun!",
    )
    # Use parse_known_args or manually handle the quantifier
    # The requirement says ANY/EVERY should precede selector
    # Current: url parser_name selector operator_name value
    # Desired: url parser_name [quantifier] selector operator_name value

    # We'll stick to positional arguments and manually adjust if 6 arguments are provided
    # or if the 3rd argument is ANY/EVERY.

    _ = parser.add_argument("url")
    _ = parser.add_argument("parser_name")
    _ = parser.add_argument("selector_or_quantifier")
    _ = parser.add_argument("operator_or_selector")
    _ = parser.add_argument("value_or_operator")
    _ = parser.add_argument("maybe_value", nargs="?")

    _ = parser.add_argument("--debug", action="store_true")
    _ = parser.add_argument("--json", action="store_true")

    parsed_args, unknown = parser.parse_known_args()
    args = parsed_args.__dict__

    # Handle quantifier logic
    if args["selector_or_quantifier"].upper() in ["ANY", "EVERY"]:
        args["quantifier"] = args["selector_or_quantifier"].upper()
        args["selector"] = args["operator_or_selector"]
        args["operator_name"] = args["value_or_operator"]
        args["value"] = args["maybe_value"]
        if args["value"] is None:
             parser.error("the following arguments are required: value")
    else:
        args["quantifier"] = "ANY"
        args["selector"] = args["selector_or_quantifier"]
        args["operator_name"] = args["operator_or_selector"]
        args["value"] = args["value_or_operator"]
        if args["maybe_value"] is not None:
             # If we have a 6th argument but 3rd wasn't a quantifier, it might be an error or we shift
             # But let's stick to the requirement
             pass

    # Clean up temporary keys
    del args["selector_or_quantifier"]
    del args["operator_or_selector"]
    del args["value_or_operator"]
    del args["maybe_value"]

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
