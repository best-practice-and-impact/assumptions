import pytest

from assumptions.log_items import LogItem


def test_incomplete_subclass():
    class LazyLogItem(LogItem):
        pass

    with pytest.raises(
        TypeError,
        match="empty_message, parse, search_pattern, template_marker",
    ):
        instance = LazyLogItem()  # noqa: F841
