import os
import re
import sys
import glob
import datetime
from pathlib import Path
import pkg_resources

from assumptions.log_items import LogItem


class FileReadError(Exception):
    pass


class Log:
    """
    Carries out file search and carried out marker replacement in templates.
    """

    def __init__(self, log_file_path: str):
        self.assumptions = []
        self.caveats = []
        self.log_file_path = Path(log_file_path)
        if not self.log_file_path.parent.exists():
            raise FileNotFoundError(
                f"Output directory does not exist: {self.log_file.parent}")

        self.log_items = []

    def add_log_item(self, log_item: LogItem):
        """
        Add a parser to the log. Parsers provide the regex pattern for searching
        for items, the marker for insertion into templates and a handler method
        for parsing items before inserting them into the template.
        """
        if not issubclass(log_item, LogItem):
            print(type(log_item))
            raise TypeError(
                "Log item must be a subclass of `assumptions.LogItem`")
        self.log_items.append(log_item)

    def find_items(self, relative_search_path: str):
        """
        Recursive directory search for each parser's ``search_pattern``.
        Captures relative path to file.
        """
        if len(self.log_items) == 0:
            raise ValueError("No parsers have been added to the Log.")

        current_dir = Path(os.getcwd())
        search_path = (current_dir / relative_search_path).resolve()
        print(f"Searching for items under: {search_path}")

        for path in [p for p in search_path.glob("**/*") if p.is_file()]:
            try:
                with path.open("r") as f:
                    file_contents = f.read()
            except:
                raise FileReadError(f"File could not be read: {path}")

            for log_item in self.log_items:
                for item in re.findall(log_item.search_pattern, file_contents, re.MULTILINE | re.IGNORECASE):
                    log_item.matched_items.append(
                        (path.relative_to(search_path.parent).as_posix(), item)
                    )

    def write_log(self, template: str):
        """
        Write log to ``log_file_path``.
        Inserts parsed items into markers in the specified template file.
        """
        for log_item in self.log_items:
            log_item.parse_items()

        if template is None:
            # Default from package
            template = pkg_resources.resource_filename(
                "assumptions", "templates/assumptions_caveats_log.md"
            )
        with open(template, "r") as f:
            template_content = f.read()

        if "{ date }" in template_content:
            template_content.replace(
                "{ date }",
                datetime.datetime.today().strftime(r"Y%/%m/%d")
            )

        for log_item in self.log_items:
            items = log_item.parsed_items
            if len(items) == 0:
                print(
                    f"Warning: No {log_item.__class__.__name__} items found.")
                items = [log_item.empty_message]

            template_content.replace(
                log_item.template_marker,
                "\n".join(items)
            )

        if self.log_file_path.exists():
            with open(self.log_file_path, "r") as f:
                old_template_content = f.read()

            # Check if output has changed, other than dates
            if old_template_content.replace(r"Y%/%m/%d", "") == template_content.replace(r"Y%/%m/%d", ""):
                print("Warning: No change to log items, log not updated.")
                return False

        print(f"Writing log to: {self.log_file_path}")
        with open(self.log_file_path, "w") as f:
            f.write(template_content)
        return True
