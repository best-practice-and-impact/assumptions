from typing import List

import pytest

from assumptions import Log
from assumptions.log_items import Todo


@pytest.fixture(scope="function")
def basic_log():
    yield Log("assumptions_caveats_log", ".")


def test_log_type_validation():
    with pytest.raises(ValueError):
        Log("not_a_log_type", ".")


def test_invalid_output_dir():
    with pytest.raises(FileNotFoundError):
        Log("assumptions_caveats_log", "/definitely/not/a/real/dir/path")


def test_add_log_item_type(basic_log):
    basic_log.add_log_item_type(Todo)
    assert isinstance(basic_log.log_item_types[0], Todo)


def test_invalid_log_item_type(basic_log):
    with pytest.raises(TypeError):
        basic_log.add_log_item_type(List)
