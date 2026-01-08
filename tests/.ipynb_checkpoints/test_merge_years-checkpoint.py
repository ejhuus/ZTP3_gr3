import pandas as pd

from read_process import merge_years


def test_merge_years_keeps_only_common_station_codes():
    t1 = pd.Timestamp("2015-01-01 01:00")
    t2 = pd.Timestamp("2015-01-01 02:00")

    df_2015 = pd.DataFrame({"A": [1.0, 2.0], "B": [10.0, 20.0]}, index=[t1, t2])
    df_2018 = pd.DataFrame({"B": [30.0, 40.0], "C": [300.0, 400.0]}, index=[t1, t2])

    metadata = pd.DataFrame({"Kod stacji": ["B"], "Miejscowość": ["Kalisz"]})

    merged = merge_years({2015: df_2015, 2018: df_2018}, metadata)

    assert merged.columns.names == ["City", "Station_Code"]
    assert list(merged.columns) == [("Kalisz", "B")]
    assert merged.shape == (4, 1)
    assert merged.iloc[0, 0] == 10.0
    assert merged.iloc[2, 0] == 30.0


def test_merge_years_unknown_city_when_missing_in_metadata():
    t = pd.Timestamp("2015-01-01 01:00")
    df_2015 = pd.DataFrame({"X": [1.0]}, index=[t])
    df_2018 = pd.DataFrame({"X": [2.0]}, index=[t])
    metadata = pd.DataFrame({"Kod stacji": [], "Miejscowość": []})

    merged = merge_years({2015: df_2015, 2018: df_2018}, metadata)

    assert list(merged.columns) == [("Unknown", "X")]
