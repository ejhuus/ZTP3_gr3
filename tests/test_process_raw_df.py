import pandas as pd
import pytest

from read_process import process_raw_df


def test_process_raw_df_parses_numbers_and_shifts_midnight_and_interpolates():
    raw = pd.DataFrame(
        [
            ["preamble", None, None],
            ["Data", "Kod stacji", "WpKaliSawick"],
            ["2017-12-31 23:00:00", "x", "1,5"],
            ["2018-01-01 00:00:00", "x", ""],
            ["2018-01-01 01:00:00", "x", "2,5"],
        ]
    )

    out = process_raw_df(raw, 2018)

    assert list(out.columns) == ["WpKaliSawick"]

    # 00:00 jest traktowane jako poprzedni dzień.
    shifted = pd.Timestamp("2017-12-31 23:59:59")
    assert shifted in out.index

    assert out.loc[pd.Timestamp("2017-12-31 23:00:00"), "WpKaliSawick"] == 1.5
    assert out.loc[pd.Timestamp("2018-01-01 01:00:00"), "WpKaliSawick"] == 2.5

    assert out.loc[shifted, "WpKaliSawick"] == pytest.approx(2.0, abs=1e-3)


def test_process_raw_df_filters_years_and_drops_station_code_column():
    raw = pd.DataFrame(
        [
            ["Data", "Kod stacji", "A"],
            ["2016-01-01 01:00:00", "x", "1"],
            ["2017-12-31 23:00:00", "x", "2"],
            ["2018-01-01 01:00:00", "x", "3"],
        ]
    )

    out = process_raw_df(raw, 2018)

    assert "Kod stacji" not in out.columns
    assert out.index.min().year == 2017
    assert out.index.max().year == 2018
