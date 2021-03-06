import datetime
import os
import re
from pathlib import Path

import pkg_resources

from assumptions.log_items import Assumption
from assumptions.log_items import Caveat
from assumptions.log_items import LogItem
from assumptions.log_items import Todo


class LogError(Exception):
    pass

class LogFindError(Exception):
    pass


_BUILTIN_ITEM_TYPES = {
    "assumptions_caveats_log": [Assumption, Caveat],
    "todo_list": [Todo],
}


class Log:
    """
    Searches files for log items and writes them to an output log using a
    template.

    Methods
    -------
    add_log_item_type(log_item)
        add a ``LogItem`` class, for use when searching for log items.
    find_items(relative_search_path='', extension='')
        recursively search files under the specificed path for log items.
        Current directory and all file extensions by default.
    write_log(template_path=None, encoding: str='utf-8')
        write an output log file, inserting discovered log items into the
        provided template. Uses the built-in template for the choses log type
        by default.
    """

    def __init__(
        self,
        log_type: str = "assumptions_caveats_log",
        log_file_path: str = "assumptions_caveats_log.md",
    ):
        self._log_file_path = Path(log_file_path)
        if not self._log_file_path.parent.exists():
            raise FileNotFoundError(
                f"Output directory does not exist: {self._log_file_path.parent}",
            )

        self._log_item_types = []

        if log_type not in _BUILTIN_ITEM_TYPES.keys():
            msg = (
                f"{log_type} is not a valid log type."
                f" Choose from {', '.join(_BUILTIN_ITEM_TYPES.keys())}."
            )
            raise ValueError(msg)

        self._builtin_template = pkg_resources.resource_filename(
            "assumptions",
            f"templates/{log_type}.md",
        )

    def add_log_item_type(self, log_item: LogItem):
        """
        Add a ``LogItem`` to the log. These parsers provide the regex pattern for searching
        for items, the marker for insertion into templates and a handler method
        for parsing items before inserting them into the template.

        Parameters
        ----------
        log_item
            log items to search for and include in output log.
        """
        if not issubclass(log_item, LogItem):
            raise TypeError(
                "Log item must be a subclass of `assumptions.LogItem`",
            )
        self._log_item_types.append(log_item())

    def find_items(self, relative_search_path: str = "", extension: str = ""):
        """
        Recursive directory search for each ``log_item`` ``search_pattern``.
        Optionally searches a specific file extension.
        Captures relative path to file containing item and item content.

        Parameters
        ----------
        relative_search_path
            relative path to directory that should be searched for log items.
        extension
            file extension to reduce search to specific file types (e.g. '.py').
        """
        if len(self._log_item_types) == 0:
            raise LogError("No `log_items` have been added to the Log.")

        current_dir = Path(os.getcwd())
        search_path = (current_dir / relative_search_path).resolve()
        print(f"Searching for log items under: {search_path}")

        for path in [p for p in search_path.glob("**/*" + extension) if p.is_file()]:
            try:
                with path.open("r") as f:
                    file_contents = f.read()
            except UnicodeDecodeError:
                print(f"File could not be read, skipping: {path}")

            for log_item in self._log_item_types:
                log_item.find_items(
                    file_contents,
                    path.relative_to(search_path.parent).as_posix(),
                )

    def write_log(self, template_path: str = None, encoding: str = "utf-8"):
        """
        Write log to instance ``log_file_path``. Inserts matched log items into
        markers in the specified template file.

        Paramters
        ---------
        template_path
            path to the output log template (any plain text file).
        encoding
            encoding used to read and write template and output log.
        """
        if template_path is None:
            # Default is assumptions and caveats from package
            template_path = self._builtin_template
        with open(template_path, "r", encoding=encoding) as f:
            template_content = f.read()

        if "{ current_date }" in template_content:
            template_content = template_content.replace(
                "{ current_date }",
                datetime.datetime.today().strftime(r"%d/%m/%Y"),
            )

        for log_item_type in self._log_item_types:
            log_item_type.parse_items()
            items = log_item_type.parsed_items

            if len(items) == 0:
                print(f"Warning: No {log_item_type.__class__.__name__} items found.")
                items = [log_item_type.empty_message]

            template_content = template_content.replace(
                log_item_type.template_marker,
                "\n".join(items).strip(),
            )

        if self._log_file_path.exists():
            print("Log exists, checking for changes...")
            with open(self._log_file_path, "r", encoding=encoding) as f:
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

        print(f"Writing log to: {self._log_file_path}")
        with open(self._log_file_path, "w", encoding=encoding) as f:
            f.write(template_content)
        return True
