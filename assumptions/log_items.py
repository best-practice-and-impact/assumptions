from abc import ABC, abstractmethod
import re


class LogItem(ABC):

    def __init__(self):
        self.matched_items = []
        self.parsed_items = []

    def parse_items(self):
        self.parsed_items += [handler(item) for item in self.matched_items]
        self.matched_items = []

    @property
    @abstractmethod
    def search_pattern(self):
        """The regex pattern used to search for the item."""
        pass

    @property
    @abstractmethod
    def template_marker(self):
        """The marker used for insertion into a template."""
        pass

    @abstractmethod
    def parser(self, idx, file_path, item):
        """
        The function used to handle matches from the search pattern.
        Should return the output for a single item, where each item is a match
        on the ``search_pattern``.

        Parameters
        ----------

        idx
            The index of the item in the list of captured items
        file
            The relative path to the file where the item is found
        item
            The item matching the search pattern

        """
        pass


class Assumption(LogItem):

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

    def parser(self, idx, file_path, item):
        detailed_description = re.sub(
            # Remove indentation and comment hash from detailed description
            f"\n?{item[0]}#",
            "",
            item[4]
        )
        detailed_description = re.sub(
            # Reduce whitespace to single spaces and strip
            "[ ]{2,}", " ", detailed_description.strip())

        assumptions_content = (
            "\n".join([
                f"### Assumption {idx + 1}: {item[1]}",
                "",
                # Relative path to file
                f"* Location: `{file_path}`",
                f"* **Quality**: {item[2]}",
                f"* **Impact**: {item[3]}",
                "",
                f"{detailed_description}",
                "",
                ""
            ])
        )
        return assumptions_content


class Caveat(LogItem):

    search_pattern = (
        # Get indentation level and Caveat title
        r"^([ \t]*)# ?Caveat: ?(.+)\n"
        # Lazily match everything following, till there's a line that doesn't start
        # with the same indent and comment
        r"(\1# ?(?:.|\n)*?)^(?!\1#)"
    )

    template_marker = "{ caveats }"

    def parser(self, idx, file_path, item):
        detailed_description = re.sub(
            # Remove indentation and comment hash from detailed description
            f"\n?{item[0]}#",
            "",
            item[2]
        )
        detailed_description = re.sub(
            # Reduce whitespace to single spaces and strip
            "[ ]{2,}", " ", detailed_description.strip())

        caveat_content = (
            "\n".join([
                f"### Caveat {idx + 1}: {item[1]}",
                "",
                # Relative path to file
                f"Location: `{file_path}`",
                "",
                f"{detailed_description}",
                "",
                ""
            ])
        )
        return caveat_content


class Todo(LogItem):

    search_pattern = (
        # Get indentation level
        r"^([ \t]*)# ?TODO: ?"
        # Lazily match everything following, till there's a line that doesn't start
        # with the same indent and comment
        r"((.+)\n\1# ?(?:.|\n)*?)^(?!\1#)"
    )

    template_marker = "{ todos }"

    def parser(self, idx, file_path, item):
        todo_item = re.sub(
            # Remove indentation and comment hash from todo item
            f"\n?{item[0]}#",
            "",
            item[1]
        )
        todo_item = re.sub(
            # Reduce whitespace to single spaces and strip
            "[ ]{2,}", " ", todo_item.strip())

        return f"- [ ] {todo_item}"
