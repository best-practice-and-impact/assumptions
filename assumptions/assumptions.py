#!/usr/bin/env python
import os
import re
import sys
import glob
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
    r"(\1#(?:.|\n)*?)^(?!\1#)"
)

class AssumptionsLog:
    
    def __init__(self, log_file_path: str):
        self.assumptions = []
        self.caveats = []
        self.log_file_path = Path(log_file_path)
        if not self.log_file_path.parent.exists():
            raise FileNotFoundError(f"Output directory does not exist: {self.log_file.parent}")

    def find_assumptions(self, relative_search_path: str):
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
                assumptions_content += (
                    "\n".join(
                        f"### Assumption {idx + 1}: {assumption[1]}",
                        "",
                        f"* **Quality**: {assumption[2]}",
                        f"* **Impact**: {assumption[3]}",
                        "",
                        f"{assumption[4]}",
                        ""
                        )
                )
        if len(self.caveats) < 1:
            print("Warning: No caveats in log.")
            caveats_content = "Currently no caveats in this analysis."
        else:
            caveats_content = ""

        with open(template, "r") as f:
            template_content = f.read()
        
        template_content = template_content.replace(
            "{ assumptions }",
            assumptions_content)

        template_content = template_content.replace(
            "{ caveats }",
            caveats_content)
        
        print(f"Writing assumptions log to: {self.log_file_path}")
        with open(self.log_file_path, "w") as f:
            f.write(template_content)


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
    log.write_log(
        pkg_resources.resource_filename("assumptions", "templates/default.md")
        )

    