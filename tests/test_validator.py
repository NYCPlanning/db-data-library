from pathlib import Path

import yaml

from library.validator import Validator

v = Validator(f"{Path(__file__).parent}/data/test_none.yml")


def test_tree_structure():
    assert v.tree_is_valid


def test_dataset_name_matches():
    assert v.dataset_name_matches


def test_has_only_one_source():
    assert v.has_only_one_source


def test_file_is_valid():
    assert v()
