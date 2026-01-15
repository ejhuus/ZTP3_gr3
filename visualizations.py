"""
Funkcje do wizualizacji.
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def plot_city_trends(monthly_df: pd.DataFrame, years_to_plot: list[int], cities_to_plot: list[str]) -> None:
    trends_data = {}

    for year in years_to_plot:
        for city in cities_to_plot:
            if city in monthly_df.columns and year in monthly_df.index.get_level_values(0):
                
                data_series = monthly_df.loc[year, city]
                trends_data[(city, year)] = data_series
    # Rysowanie wykresu trendów
    fig, ax = plt.subplots(figsize=(12, 7))
    
    for (city, year), data in trends_data.items():
        # Miesiące na osi X
        months = range(1, 13)
        ax.plot(months, data.values, marker='o', linestyle='--', label=f'{city} {year}')
    
    # Ustawienia wykresu
    ax.set_title('Średnie miesięczne stężenie PM2.5 w Warszawie i Katowicach (2014 vs 2024)')
    ax.set_xlabel('Miesiąc')
    ax.set_ylabel('Średnie stężenie PM2.5 (µg/m³)')
    ax.set_xticks(months)
    ax.legend(title='Miasto i Rok')
    ax.grid(True)
    plt.tight_layout()
    
    plt.show()

def plot_city_heatmap(city_monthly_avg: pd.DataFrame, YEARS: list[int]) -> None:
    
    # Tworzymy FacetGrid, gdzie każdy panel to jedno miasto
    g = sns.FacetGrid(city_monthly_avg, col="City", col_wrap=4, height=4)
    
    # Mapujemy heatmapę na każdy panel
    g.map_dataframe(
        lambda data, color: sns.heatmap(
            data.pivot(index='Year', columns='Month', values='PM25_Value'),
            cmap='viridis'
        )
    )
    
    g.set_titles("{col_name}", size=14)
    g.set_axis_labels("Miesiąc", "Rok")
    
    # Dynamiczny tytuł wykorzystujący zmienną YEARS
    years_str = ", ".join(map(str, sorted(YEARS)))
    g.figure.suptitle(f'Heatmapy średnich miesięcznych stężeń PM2.5 dla miast ({years_str})', size=20, y=1.03)
    
    plt.show()

def plot_who_norm_barplot(plot_data_long: pd.DataFrame) -> None:
    
    plt.figure(figsize=(15, 8))
    sns.barplot(
        data=plot_data_long,
        x='Station_Label',
        y='Exceeding_Days',
        hue='Year',
        palette='viridis'
    )
    
    plt.title('Liczba dni z przekroczeniem normy PM2.5 (15 µg/m³) dla wybranych stacji')
    plt.xlabel('Stacja pomiarowa')
    plt.ylabel('Liczba dni z przekroczeniem normy')
    plt.xticks(rotation=45, ha='right')
    plt.legend(title='Rok')
    plt.grid(axis='y')  
    plt.tight_layout()
    
    plt.show()

def plot_voivod_exceeded(voivod_data: pd.DataFrame) -> None:
    """Generuje barplot pokazujący liczbę dni z przekroczeniem normy stężenia PM2.5
       dla każdego województwa

    Args:
        voivod_data (pd.DataFrame): dataframe ze zliczeniami dni z przekroczeniem normy PM2.5
    """
    
    voivod_data.T.plot(
        kind="bar",
        figsize=(16, 6),
        cmap="viridis"
    )

    plt.xlabel("Województwo")
    plt.ylabel("Liczba dni z przekroczeniem normy PM2.5")
    plt.title("Liczba dni w roku z przekroczeniem normy PM2.5 w każdym województwie")
    plt.xticks(rotation=45, ha="right")
    plt.legend(
        title="Rok",
        bbox_to_anchor=(1, 1),
        loc="upper left"
    )
    plt.tight_layout()
    plt.show()