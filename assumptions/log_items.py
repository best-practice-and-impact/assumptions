import re
from abc import ABC
from abc import abstractmethod
from pathlib import Path


class _AbstractLogItem(ABC):
    """
    Log Item class interface, defining the attributes required by any LogItem subclass.

    Methods
    -------
    parse(idx, file_path, item)
        Parse a single log item, to produce the desired string representation in the output log.
    """

    @property
    @abstractmethod
    def search_pattern(self):
        """The regex pattern used to search for the item."""
        pass

    @property
    @abstractmethod
    def template_marker(self):
        """
        The marker used for insertion into a template. Built-in items use
        curly braces (e.g. ``{ assumptions }``).
        """
        pass

    @property
    @abstractmethod
    def empty_message(self):
        """
        The text to be inserted into the log when no items are found. For
        example, 'No pokemon references found in this analysis.'.
        """
        pass

    @abstractmethod
    def parse(self, idx, file_path, item):
        """
        Parse a log item into output string for writting to output log. Should
        return the output for a single log item, where each item is a match
        on the item's ``search_pattern``.

        Parameters
        ----------
        idx
            The index of the item in the list of captured items
        file_path
            The relative path to the file where the item is found
        item
            An item matched using ``search_pattern``. A string, or tuple of strings,
            depending on number of groups captured in ``search_pattern``.

        Returns
        -------
        str
            String representation of item, for use in output log file.
        """
        pass


class LogItem(_AbstractLogItem):
    """
    Log Item class interface, defining the attributes required by any LogItem subclass.

    Attributes
    ----------
    matched_items
        list of log item matches that have been found.
    parsed_items
        list of parsed log items, which can be inserted into log outputs.

    Methods
    -------
    find_items(text, path)
        search for and store log items from text.
    parse_items()
        parse matched log items into strings.
    """

    def __init__(self):
        self.matched_items = []
        self.parsed_items = []

    def find_items(self, text: str, path: Path):
        """
        Search for log items in text. Stores matched items and their file
        paths in ``parsed_items``.

        Parameters
        ----------
        text
            a string of text to be searched for log items.
        path
            path to file containing text, for use in parsing.
        """
        for item in re.findall(
            self.search_pattern,
            text,
            re.MULTILINE | re.IGNORECASE,
        ):
            self.matched_items.append((path, item))

    def parse_items(self):
        """
        Parse each matched item into a string, ready to be inserted into output
        content.
        """
        self.parsed_items += [
            self.parse(idx, filepath, item)
            for idx, (filepath, item) in enumerate(self.matched_items)
        ]
        self.matched_items = []


class Assumption(LogItem):
    """
    Matches and parses assumptions from hash code comments.
    """

    search_pattern = (
        # Get indentation level and Assumption title
        r"^([ \t]*)# ?Assumption: ?(.+)\n"
        # Short or long from RAG ratings
        r"^\1# ?Q(?:uality)?: ?(.+)\n"
        r"^\1# ?I(?:mpact)?: ?(.+)\n"
        # Lazily match everything following, till there's a line that doesn't
        # start with the same indent and comment
        r"(\1# ?(?:.|\n)*?)^(?!\1#)"
    )

    template_marker = "{ assumptions }"
    empty_message = "Currently no assumptions in this analysis.\n"

    def parse(self, idx, file_path, item):
        detailed_description = re.sub(
            # Remove indentation and comment hash from detailed description
            f"\n?{item[0]}#",
            "",
            item[4],
        )
        detailed_description = re.sub(
            # Reduce whitespace to single spaces and strip
            "[ ]{2,}",
            " ",
            detailed_description.strip(),
        )

        assumptions_content = "\n".join(
            [
                f"### Assumption {idx + 1}: {item[1]}",
                "",
                # Relative path to file
                f"* Location: `{file_path}`",
                f"* **Quality**: {item[2]}",
                f"* **Impact**: {item[3]}",
                "",
                f"{detailed_description}",
                "",
            ],
        )
        return assumptions_content


class Caveat(LogItem):
    """
    Matches and parses caveats from hash code comments.
    """

    search_pattern = (
        # Get indentation level and Caveat title
        r"^([ \t]*)# ?Caveat: ?(.+)\n"
        # Lazily match everything following, till there's a line that doesn't start
        # with the same indent and comment
        # Long description is optional, as caveats might be one liners
        r"(\1# ?(?:.|\n)*?)?^(?!\1#)"
    )

    template_marker = "{ caveats }"
    empty_message = "Currently no caveats in this analysis.\n"

    def parse(self, idx, file_path, item):
        detailed_description = re.sub(
            # Remove indentation and comment hash from detailed description
            f"\n?{item[0]}#",
            "",
            item[2],
        )
        detailed_description = re.sub(
            # Reduce whitespace to single spaces and strip
            "[ ]{2,}",
            " ",
            detailed_description.strip(),
        )

        caveat_content = "\n".join(
            [
                f"### Caveat {idx + 1}: {item[1]}",
                "",
                # Relative path to file
                f"Location: `{file_path}`",
                "",
                f"{detailed_description}",
                "",
            ],
        )
        return caveat_content


class Todo(LogItem):
    """
    Matches and parses todos from hash code comments.
    """

    search_pattern = (
        # Get indentation level
        r"^([ \t]*)# ?TODO: (.+)\n?"
        # Lazily match everything following, till there's a line that doesn't start
        # with the same indent and comment
        # Long description is optional, as todos are often one liners
        r"(\1# ?(?:.|\n)*?)?^(?!\1#)"
    )

    template_marker = "{ todos }"
    empty_message = "Great, there's nothing to do!\n"

    def parse(self, idx, file_path, item):
        todo_item = item[1] + re.sub(
            # Remove indentation and comment hash from todo item
            f"\n?{item[0]}#",
            "",
            item[2],
        )
        todo_item = re.sub(
            # Reduce whitespace to single spaces and strip
            "[ ]{2,}",
            " ",
            todo_item.strip(),
        )

        return f"- [ ] {todo_item}"
