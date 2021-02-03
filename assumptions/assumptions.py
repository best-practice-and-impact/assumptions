#!/usr/bin/env python
import os
import re
import sys
import glob
from pathlib import Path

ASSUMPTIONS_PATTERN = (
    # Get indentation level and Assumption title
    r"^([ \t]*)# ?Assumption: ?(.+)\n"
    # Short or long from RAG ratings
    r"^\1# ?Q(?:uality)?: ?(.+)\n"
    r"^\1# ?I(?:mpact)?: ?(.+)\n"
    # Lazily match everything following, till there's a line that doesn't start
    # with the same indent and comment
    r"(\1#(?:.|\n)*?)^(?!\1#)"

)

class AssumptionsLog:
    def __init__(self, log_file_path):
        self.assumptions = []
        self.caveats = []
        self.log_file_path = Path(log_file_path)
        if not self.log_file_path.parent.exists():
            raise FileNotFoundError(f"Path does not exist: {self.log_file.parent}")

    def find_assumptions(self, relative_search_path):
        """
        Recursive directory search for assumptions in code comments.
        Captures relative path to file, assumption title, RAG ratings and details.
        """
        current_dir = Path(os.getcwd())
        search_path = (current_dir / relative_search_path).resolve()
        print(f"Searching for assumptions under: {search_path}")

        for path in [p for p in search_path.glob("**/*") if p.is_file()]:
            with path.open("r") as f:
                for a in re.findall(ASSUMPTIONS_PATTERN, f.read(), re.MULTILINE | re.IGNORECASE):
                    self.assumptions.append((path.relative_to(search_path.parent).as_posix(), a))

    def write_log(self):
        """Write assumptions log to path specified when class instance created."""
        print(f"Writing assumptions log to: {self.log_file_path}")
        print(self.assumptions)
        if len(self.assumptions) < 1:
            print("Warning: No assumptions in log.")
        if len(self.caveats) < 1:
            print("Warning: No caveats in log.")

if __name__ == "__main__":
    # TODO: Replace with an actual arg parser
    try:
        outfile = sys.argv[1]
    except IndexError:
        outfile = "assumptions_log.md"
    
    try:
        search_path = sys.argv[2]
    except IndexError:
        search_path = ""

    log = AssumptionsLog(outfile)
    assumptions = log.find_assumptions(search_path)
    log.write_log()
    