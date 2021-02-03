#!/usr/bin/env python
import os
import re
import sys
import glob
import argparse
from pathlib import Path
import pkg_resources

ASSUMPTIONS_PATTERN = (
    # Get indentation level and Assumption title
    r"^([ \t]*)# ?Assumption: ?(.+)\n"
    # Short or long from RAG ratings
    r"^\1# ?Q(?:uality)?: ?(.+)\n"
    r"^\1# ?I(?:mpact)?: ?(.+)\n"
    # Lazily match everything following, till there's a line that doesn't start
    # with the same indent and comment
    r"(\1# ?(?:.|\n)*?)^(?!\1#)"
)


class FileReadError(Exception):
    pass


class AssumptionsLog:
    """
    Stores assumptions log output path and assumptions and caveats that are
    collected from code comments.
    """

    def __init__(self, log_file_path: str):
        self.assumptions = []
        self.caveats = []
        self.log_file_path = Path(log_file_path)
        if not self.log_file_path.parent.exists():
            raise FileNotFoundError(
                f"Output directory does not exist: {self.log_file.parent}")

    def find_assumptions(self, relative_search_path: str):
        """
        Recursive directory search for assumptions in code comments.
        Captures relative path to file, assumption title, RAG ratings and details.
        """
        current_dir = Path(os.getcwd())
        search_path = (current_dir / relative_search_path).resolve()
        print(f"Searching for assumptions under: {search_path}")

        for path in [p for p in search_path.glob("**/*") if p.is_file()]:
            try:
                with path.open("r") as f:
                    for a in re.findall(ASSUMPTIONS_PATTERN, f.read(), re.MULTILINE | re.IGNORECASE):
                        self.assumptions.append(
                            (path.relative_to(search_path.parent).as_posix(), a))
            except:
                raise FileReadError(f"File could not be read: {path}")

    def write_log(self, template: str):
        """
        Write assumptions and caveats log to `log_file_path`.
        Inserts assumptions and caveats into `{ assumptions }` and 
        `{ caveats }` placeholders in the specified template file.
        """
        if len(self.assumptions) < 1:
            print("Warning: No assumptions in log.")
            assumptions_content = "Currently no assumptions in this analysis."
        else:
            assumptions_content = ""
            for idx, assumption in enumerate(self.assumptions):
                detailed_description = re.sub(
                    # Remove indentation and comment hash
                    f"\n?{assumption[1][0]}#",
                    "",
                    assumption[1][4]
                )
                detailed_description = re.sub(
                    "[ ]{2,}", " ", detailed_description.strip())
                assumptions_content += (
                    "\n".join([
                        f"### Assumption {idx + 1}: {assumption[1][1]}",
                        "",
                        # Relative path to file
                        f"* Location: `{assumption[0]}`",
                        f"* **Quality**: {assumption[1][2]}",
                        f"* **Impact**: {assumption[1][3]}",
                        "",
                        f"{detailed_description}",
                        "",
                        ""
                    ])
                )
        if len(self.caveats) < 1:
            print("Warning: No caveats in log.")
            caveats_content = "Currently no caveats in this analysis."
        else:
            # TODO: implement caveats pattern and logging
            caveats_content = ""

        if template is None:
            # Default from package
            template = pkg_resources.resource_filename(
                "assumptions", "templates/default.md"
            )
        with open(template, "r") as f:
            template_content = f.read()

        # Could move these conversion mappings to classes for exensibility
        template_content = template_content.replace(
            "{ assumptions }",
            assumptions_content
        )

        template_content = template_content.replace(
            "{ caveats }",
            caveats_content
        )

        print(f"Writing assumptions log to: {self.log_file_path}")
        with open(self.log_file_path, "w") as f:
            f.write(template_content)


def cli():
    """Command line entry point."""
    parser = argparse.ArgumentParser(
        description="Generate an assumption and caveat log from code comments.",
        epilog="Your assumptions documented."
    )
    parser.add_argument("-o", "--outfile", type=str,
                        default="assumptions_log.md",
                        help="output Markdown (`.md`) file path. Default is "
                        "'./assumptions_log.md'."
                        )
    parser.add_argument("-p", "--path", type=str, default="",
                        help="relative path to directory to seach for"
                        " assumptions and caveats under. Default is current"
                        " directory."
                        )
    parser.add_argument("-t", "--template", type=str, default=None,
                        help="path to a template assumptions log."
                        )
    args = parser.parse_args()

    log = AssumptionsLog(args.outfile)
    log.find_assumptions(args.path)
    log.write_log(args.template)


if __name__ == "__main__":
    cli()
