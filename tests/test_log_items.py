import pytest

from assumptions.log_items import LogItem


def test_incomplete_subclass():
    """Test that subclass fails if abstract properties not implemented."""

    class LazyLogItem(LogItem):
        pass

    with pytest.raises(
        TypeError,
        match="empty_message, parse, search_patterns, template_marker",
    ):
        instance = LazyLogItem()  # noqa: F841
