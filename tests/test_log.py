from typing import List

import pytest

from assumptions.log import Log
from assumptions.log import LogError
from assumptions.log_items import Assumption
from assumptions.log_items import Caveat
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


@pytest.mark.parametrize("log_item_class", [Todo, Assumption, Caveat])
def test_add_log_item_type(basic_log, log_item_class):
    basic_log.add_log_item_type(log_item_class)
    assert isinstance(basic_log._log_item_types[0], log_item_class)


def test_invalid_log_item_type(basic_log):
    with pytest.raises(TypeError):
        basic_log.add_log_item_type(List)


def test_find_with_no_types(basic_log):
    with pytest.raises(LogError):
        basic_log.find_items()
