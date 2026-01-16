import pandas as pd

verg = pd.read_csv('vergunningen/bouwvergunningen.csv')
hv = pd.read_csv('nis/halle-vilvoorde.csv')

def filter_periode(df, start_jaar, start_maand, end_jaar, end_maand):
    """Filter data voor een specifieke periode"""
    result = []
    
    for year in range(start_jaar, end_jaar + 1):
        year_data = df[df['CD_YEAR'] == year].copy()
        
        if year == start_jaar and year == end_jaar:
            # Alles in hetzelfde jaar
            result.append(year_data[(year_data['CD_PERIOD'] >= start_maand) & 
                                   (year_data['CD_PERIOD'] <= end_maand)])
        elif year == start_jaar:
            # Eerste jaar: vanaf start_maand
            result.append(year_data[year_data['CD_PERIOD'] >= start_maand])
        elif year == end_jaar:
            # Laatste jaar: tot end_maand
            result.append(year_data[year_data['CD_PERIOD'] <= end_maand])
        else:
            # Tussenliggende jaren: alle maanden
            result.append(year_data[year_data['CD_PERIOD'] > 0])  # Exclude period 0 (totaal)
    
    return pd.concat(result) if result else pd.DataFrame()

# Filter voor Asse
asse_code = 23002
asse_data = verg[verg['REFNIS'] == asse_code].copy()

periode_vorig = filter_periode(asse_data, 2019, 9, 2022, 8)
print('Periode 2019-09 tot 2022-08 met filter_periode functie:')
print(f'Aantal rijen: {len(periode_vorig)}')
print()

# Check welke jaren en periodes
for year in [2019, 2020, 2021, 2022]:
    year_data = periode_vorig[periode_vorig['CD_YEAR'] == year]
    if not year_data.empty:
        periods = sorted(year_data['CD_PERIOD'].unique())
        total = year_data['MS_DWELLING_RES_NEW'].sum()
        print(f'{year}: periodes {periods}, totaal: {total:.0f}')

print()
print(f'Totaal woningen: {periode_vorig["MS_DWELLING_RES_NEW"].sum():.0f}')

# Check wat er in de huidige hv staat
asse_hv = hv[hv['TX_REFNIS_NL'] == 'Asse']
print(f'\nIn halle-vilvoorde.csv staat voor Asse:')
print(f'Woningen_Nieuwbouw_2019sep-2022aug: {asse_hv["Woningen_Nieuwbouw_2019sep-2022aug"].values[0]:.0f}')
