"""
Funkcje do grupowania, liczenia średnich itp.
"""

import pandas as pd
import numpy as np

def group_monthly_cities(final_df: pd.DataFrame) -> pd.DataFrame:
    
    monthly = (final_df.groupby([final_df.index.year, final_df.index.month], axis=0).mean())
    monthly_cities = monthly.groupby(level='City', axis=1).mean()
    
    return monthly_cities
