#!/usr/bin/env python
import argparse

from assumptions.log import _BUILTIN_ITEM_TYPES
from assumptions.log import Log


def cli():
    """Assumptions command line interface entry point."""
    # Parse args
    parser = argparse.ArgumentParser(
        description="Generate an assumptions and caveats log from code comments.",
        epilog="Your assumptions and caveats documented.",
    )
    parser.add_argument(
        "-l",
        "--log-type",
        type=str,
        default="assumptions_caveats_log",
        help="type of log to produce. Default is the" " assumptions and caveats log.",
    )
    parser.add_argument(
        "-o",
        "--outfile",
        type=str,
        default=None,
        help="output Markdown (`.md`) file path. Default is " "'LOG_TYPE.md'.",
    )
    parser.add_argument(
        "-p",
        "--path",
        type=str,
        default="",
        help="relative path to directory to seach for"
        " assumptions and caveats under. Default is current"
        " directory.",
    )
    parser.add_argument(
        "-e",
        "--extension",
        type=str,
        default="",
        help="file extension to search for. Searches all file"
        " extensions by default.",
    )
    parser.add_argument(
        "-t",
        "--template",
        type=str,
        default=None,
        help="path to custom log template. Overrides template" " from log argument.",
    )
    parser.add_argument(
        "-d",
        "--dry-run",
        action="store_true",
        help="when flag is passed, no output log is generated.",
    )
    args = parser.parse_args()

    outfile = args.outfile or f"{args.log_type}.md"

    # Generate log
    log = Log(args.log_type, outfile)

    item_types = _BUILTIN_ITEM_TYPES.get(args.log_type)
    if item_types is None:
        raise ValueError(
            f"{args.log_type} is not a build in log type. Try one of: {','.join(_BUILTIN_ITEM_TYPES.keys())}",
        )

    for item_type_class in item_types:
        log.add_log_item_type(item_type_class)

    log.find_items(args.path, args.extension)
    updated = log.write_log(args.template, args.dry_run)
    if args.log_type == "assumptions_caveats_log":
        if not updated:
            print("\nNUDGE: Have you updated your assumptions and caveats?")
        else:
            print("\nAssumptions and caveats documented.")


if __name__ == "__main__":
    cli()
