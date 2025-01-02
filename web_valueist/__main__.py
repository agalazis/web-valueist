#!/usr/bin/env python3
import logging
import web_valueist
from argparse import ArgumentParser
from typing import TypedDict, Unpack
from sys import stderr
from signal import signal, SIGTERM

logger = logging.getLogger(__name__)


class Args(TypedDict):
    url: str
    selector: str
    parser_name: web_valueist.Parser
    operator_name: web_valueist.Operator
    value: str


class CliArgs(Args):
    debug: bool


def _parse_args() -> CliArgs:
    parser = ArgumentParser(
        prog="web_valueist",
        description="""Fetches  the value from the web, compares 
        it with a given value and exits with zero exit code 
        if the condition is satisfied """,
        epilog="Did somebody say cron jobs? Have fun!",
    )
    _ = parser.add_argument("url")
    _ = parser.add_argument("parser_name")
    _ = parser.add_argument("selector")
    _ = parser.add_argument("operator_name")
    _ = parser.add_argument("value")
    _ = parser.add_argument("--debug", action="store_true")

    args = parser.parse_args().__dict__

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
    args=_initialize_cli()
    if web_valueist.evaluate(**args):
        logger.info("Success: Condition satisfied")
        exit(0)
    logger.error("Failure: Condition not satisfied")
    exit(1)


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
