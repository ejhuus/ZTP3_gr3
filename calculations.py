"""
Funkcje do grupowania, liczenia średnich itp.
"""

import pandas as pd
import numpy as np

def group_monthly_cities(final_df: pd.DataFrame) -> pd.DataFrame:

    monthly = final_df.groupby([final_df.index.year, final_df.index.month]).mean()
    monthly_cities = monthly.T.groupby(level='City').mean().T

    return monthly_cities
