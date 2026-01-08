import pandas as pd

from calculations import group_monthly_cities


def test_group_monthly_cities_monthly_means_and_city_average():
    idx = pd.to_datetime(
        [
            "2015-01-01 01:00",
            "2015-01-01 02:00",
            "2015-02-01 01:00",
            "2015-02-01 02:00",
        ]
    )

    # Kolumny są MultiIndex: (City, Station_Code)
    cols = pd.MultiIndex.from_tuples(
        [("City1", "S1"), ("City1", "S2"), ("City2", "S3")],
        names=["City", "Station_Code"],
    )

    df = pd.DataFrame(
        [
            [1.0, 3.0, 10.0],
            [1.0, 3.0, 10.0],
            [2.0, 4.0, 20.0],
            [2.0, 4.0, 20.0],
        ],
        index=idx,
        columns=cols,
    )

    out = group_monthly_cities(df)

    assert list(out.columns) == ["City1", "City2"]
    assert out.loc[(2015, 1), "City1"] == 2.0
    assert out.loc[(2015, 2), "City1"] == 3.0
    assert out.loc[(2015, 1), "City2"] == 10.0
    assert out.loc[(2015, 2), "City2"] == 20.0


def test_group_monthly_cities_ignores_nans_in_mean():
    idx = pd.to_datetime(["2015-01-01 01:00", "2015-01-01 02:00"])

    cols = pd.MultiIndex.from_tuples(
        [("City1", "S1"), ("City1", "S2")],
        names=["City", "Station_Code"],
    )

    df = pd.DataFrame([[1.0, None], [1.0, None]], index=idx, columns=cols)
    out = group_monthly_cities(df)

    assert out.loc[(2015, 1), "City1"] == 1.0
