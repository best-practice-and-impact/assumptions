#!/usr/bin/env python
import os
import re
import sys
import glob

ASSUMPTIONS_PATTERN = (
    "^# Assumption:\W?(.+$)\n"
    "# Q(?:uality)?:\W?(.+$)\n"  # Allow Q and I short forms
    "# I(?:mpact)?:\W?(.+$)\n"
    "((?:.|\n)*?)^[^#]"  # Lazily match everything following, till there's a line that doesn't start with a comment
)

# ^[ \t]*# Assumption: ?(.+)\n^[ \t]*# Q(?:uality)?: ?(.+)\n^[ \t]*# I(?:mpact)?: ?(.+)\n((?:.|\n)*?)\n^[^#]
# Backreference might help with indents?

def find_assumptions(search_path):
    """Recursive search for assumptions in code comments."""
    assumptions = []
    current_dir = os.getcwd()
    for file in [f for f in glob.glob(current_dir + search_path + "/**", recursive=True) if os.path.isfile(f)]:
        with open(file, "r") as f:
            file_assumptions = re.findall(ASSUMPTIONS_PATTERN, f.read(), re.MULTILINE | re.IGNORECASE)
            for a in file_assumptions:
                assumptions.append(
                    (file[len(current_dir):].replace("\\","/"),  # Only get subdirs
                    a)
                    )

    return assumptions

def write_log(assumptions, outfile):
    pass

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

    print(f"Searching for assumptions under: {search_path}")
    assumptions = find_assumptions(search_path)
    print(assumptions)
    if len(assumptions) == 0:
        print("No assumptions were found.")

    print(f"Writing assumptions log to: {outfile}")
    write_log(assumptions, outfile)
    