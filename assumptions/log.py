import datetime
import os
import re
from pathlib import Path

import pkg_resources

from assumptions.log_items import LogItem


class FileReadError(Exception):
    pass


class Log:
    """
    Carries out file search and carried out marker replacement in templates.
    """

    def __init__(self, log_type: str, log_file_path: str):
        self.assumptions = []
        self.caveats = []
        self.log_file_path = Path(log_file_path)
        if not self.log_file_path.parent.exists():
            raise FileNotFoundError(
                f"Output directory does not exist: {self.log_file.parent}",
            )

        self.log_item_types = []

        self.builtin_template = pkg_resources.resource_filename(
            "assumptions",
            f"templates/{log_type}.md",
        )

    def add_log_item_type(self, log_item: LogItem):
        """
        Add a ``LogItem`` to the log. These parsers provide the regex pattern for searching
        for items, the marker for insertion into templates and a handler method
        for parsing items before inserting them into the template.
        """
        if not issubclass(log_item, LogItem):
            raise TypeError(
                "Log item must be a subclass of `assumptions.LogItem`",
            )
        self.log_item_types.append(log_item())

    def find_items(self, relative_search_path: str, extension: str):
        """
        Recursive directory search for each ``log_item`` ``search_pattern``.
        Optionally searches a specific file extension.
        Captures relative path to file containing item and item content.
        """
        if len(self.log_item_types) == 0:
            raise ValueError("No `log_items` have been added to the Log.")

        current_dir = Path(os.getcwd())
        search_path = (current_dir / relative_search_path).resolve()
        print(f"Searching for log items under: {search_path}")

        for path in [p for p in search_path.glob("**/*" + extension) if p.is_file()]:
            try:
                with path.open("r") as f:
                    file_contents = f.read()
            except FileReadError:
                print(f"File could not be read, skipping: {path}")

            for log_item in self.log_item_types:
                for item in re.findall(
                    log_item.search_pattern,
                    file_contents,
                    re.MULTILINE | re.IGNORECASE,
                ):
                    log_item.add_matched_item(
                        (path.relative_to(search_path.parent).as_posix(), item),
                    )

    def write_log(self, template: str):
        """
        Write log to instance ``log_file_path``.
        Inserts matched items into markers in the specified template file.
        """
        if template is None:
            # Default is assumptions and caveats from package
            template = self.builtin_template
        with open(template, "r") as f:
            template_content = f.read()

        if "{ current_date }" in template_content:
            template_content = template_content.replace(
                "{ current_date }",
                datetime.datetime.today().strftime(r"%d/%m/%Y"),
            )

        for log_item_type in self.log_item_types:
            log_item_type.parse_items()
            items = log_item_type.parsed_items

            if len(items) == 0:
                print(f"Warning: No {log_item_type.__class__.__name__} items found.")
                items = [log_item_type.empty_message]

            template_content = template_content.replace(
                log_item_type.template_marker,
                "\n".join(items).strip(),
            )

        if self.log_file_path.exists():
            print("Log exists, checking for changes...")
            with open(self.log_file_path, "r") as f:
                old_template_content = f.read()

            # Check if output has changed, other than dates
            date_format = r"[0-9]{2}/[0-9]{2}/[0-9]{4}"
            if re.sub(date_format, "", old_template_content) == re.sub(
                date_format,
                "",
                template_content,
            ):
                print("No change to log items, log not updated.")
                return False

        print(f"Writing log to: {self.log_file_path}")
        with open(self.log_file_path, "w") as f:
            f.write(template_content)
        return True
