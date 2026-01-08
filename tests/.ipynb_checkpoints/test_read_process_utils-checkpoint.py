import pandas as pd

from read_process import atomize_dict, update_codes


def test_atomize_dict_splits_codes():
    mapper = {"A1, A2": "B", "C": "D"}
    out = atomize_dict(mapper)
    assert out == {"A1": "B", "A2": "B", "C": "D"}


def test_atomize_dict_strips_spaces():
    mapper = {" A1 ,A2 ": "B"}
    out = atomize_dict(mapper)
    assert out == {"A1": "B", "A2": "B"}


def test_update_codes_maps_columns():
    df = pd.DataFrame({"old": [1, 2], "keep": [3, 4]})
    out = update_codes(df, {"old": "new"})
    assert list(out.columns) == ["new", "keep"]


def test_update_codes_keeps_unmapped_columns():
    df = pd.DataFrame({"a": [1]})
    out = update_codes(df, {})
    assert list(out.columns) == ["a"]
