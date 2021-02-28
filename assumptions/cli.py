#!/usr/bin/env python
import argparse

from assumptions.log import Log
from assumptions.log_items import Assumption, Caveat



def cli():
    """Command line interface entry point."""
    parser = argparse.ArgumentParser(
        description="Generate an assumptions and caveats log from code comments.",
        epilog="Your assumptions and caveats documented."
    )
    parser.add_argument("-o", "--outfile", type=str,
                        default="assumptions_caveats_log.md",
                        help="output Markdown (`.md`) file path. Default is "
                        "'./assumptions_caveats_log.md'."
                        )
    parser.add_argument("-p", "--path", type=str, default="",
                        help="relative path to directory to seach for"
                        " assumptions and caveats under. Default is current"
                        " directory."
                        )
    parser.add_argument("-t", "--template", type=str, default=None,
                        help="path to a template assumptions log."
                        )
    parser.add_argument("-e", "--extension", type=str, default="",
                        help="file extension to search for. Searches all file"
                        " extensions by default."
                        )
    args = parser.parse_args()

    log = Log(args.outfile)
    log.add_log_item_type(Assumption)
    log.add_log_item_type(Caveat)
    log.find_items(args.path, args.extension)

    if not log.write_log(args.template):
        print("\nNUDGE: Have you updated your assumptions and caveats?")
    else:
        print("\nAssumptions and caveats documented.")


if __name__ == "__main__":
    cli()
