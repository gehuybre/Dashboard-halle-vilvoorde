import pandas as pd

# Lees de bestanden
hv = pd.read_csv('nis/halle-vilvoorde.csv')
verg = pd.read_csv('vergunningen/bouwvergunningen.csv')

# Definieer de periodes
# Laatste 36 maanden: september 2022 - augustus 2025
# Vorige 36 maanden: september 2019 - augustus 2022

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
            # Laatste jaar: tot end_maand (maar exclude periode 0)
            result.append(year_data[(year_data['CD_PERIOD'] <= end_maand) & (year_data['CD_PERIOD'] > 0)])
        else:
            # Tussenliggende jaren: alle maanden
            result.append(year_data[year_data['CD_PERIOD'] > 0])  # Exclude period 0 (totaal)
    
    return pd.concat(result) if result else pd.DataFrame()

# Filter voor de twee periodes
periode_recent = filter_periode(verg, 2022, 9, 2025, 8)  # sept 2022 - aug 2025
periode_vorig = filter_periode(verg, 2019, 9, 2022, 8)   # sept 2019 - aug 2022

# Filter alleen voor Vlaams-Brabant gemeenten (23xxx codes)
hv_codes = hv['CD_REFNIS'].unique()

periode_recent_hv = periode_recent[periode_recent['REFNIS'].isin(hv_codes)]
periode_vorig_hv = periode_vorig[periode_vorig['REFNIS'].isin(hv_codes)]

# Bereken totalen per gemeente voor nieuwbouw woningen
recent_totaal = periode_recent_hv.groupby('REFNIS').agg({
    'MS_DWELLING_RES_NEW': 'sum',
    'MS_BUILDING_RES_RENOVATION': 'sum'
}).reset_index()

vorig_totaal = periode_vorig_hv.groupby('REFNIS').agg({
    'MS_DWELLING_RES_NEW': 'sum',
    'MS_BUILDING_RES_RENOVATION': 'sum'
}).reset_index()

# Merge de twee periodes
vergelijking = recent_totaal.merge(
    vorig_totaal, 
    on='REFNIS', 
    suffixes=('_recent', '_vorig'),
    how='outer'
).fillna(0)

# Bereken percentages
vergelijking['Woningen_Nieuwbouw_pct_36m'] = (
    (vergelijking['MS_DWELLING_RES_NEW_recent'] - vergelijking['MS_DWELLING_RES_NEW_vorig']) / 
    vergelijking['MS_DWELLING_RES_NEW_vorig'] * 100
).round(2)

vergelijking['Gebouwen_Renovatie_pct_36m'] = (
    (vergelijking['MS_BUILDING_RES_RENOVATION_recent'] - vergelijking['MS_BUILDING_RES_RENOVATION_vorig']) / 
    vergelijking['MS_BUILDING_RES_RENOVATION_vorig'] * 100
).round(2)

# Vervang inf waarden (bij deling door 0) door NaN
vergelijking = vergelijking.replace([float('inf'), float('-inf')], float('nan'))

# Selecteer de kolommen die we willen toevoegen
nieuwe_kolommen = vergelijking[['REFNIS', 
                                'MS_DWELLING_RES_NEW_vorig',
                                'MS_DWELLING_RES_NEW_recent',
                                'Woningen_Nieuwbouw_pct_36m',
                                'MS_BUILDING_RES_RENOVATION_vorig',
                                'MS_BUILDING_RES_RENOVATION_recent',
                                'Gebouwen_Renovatie_pct_36m']].copy()

nieuwe_kolommen.columns = ['CD_REFNIS',
                           'Woningen_Nieuwbouw_2019sep-2022aug',
                           'Woningen_Nieuwbouw_2022sep-2025aug',
                           'Woningen_Nieuwbouw_pct_verschil_36m',
                           'Gebouwen_Renovatie_2019sep-2022aug',
                           'Gebouwen_Renovatie_2022sep-2025aug',
                           'Gebouwen_Renovatie_pct_verschil_36m']

# Verwijder de oude kolommen uit hv
kolommen_te_verwijderen = [col for col in hv.columns if 
                          'Woningen_Nieuwbouw' in col or 
                          'Gebouwen_Renovatie' in col]

hv_cleaned = hv.drop(columns=kolommen_te_verwijderen)

# Merge met de nieuwe data
result = hv_cleaned.merge(nieuwe_kolommen, on='CD_REFNIS', how='left')

# Sla het resultaat op
result.to_csv('nis/halle-vilvoorde.csv', index=False)

print("Vergunningencijfers succesvol bijgewerkt met 36-maanden vergelijking!")
print(f"\nPeriode recent: september 2022 - augustus 2025")
print(f"Periode vorig: september 2019 - augustus 2022")
print(f"\nToegevoegde kolommen:")
print("  - Woningen_Nieuwbouw_2019sep-2022aug")
print("  - Woningen_Nieuwbouw_2022sep-2025aug")
print("  - Woningen_Nieuwbouw_pct_verschil_36m")
print("  - Gebouwen_Renovatie_2019sep-2022aug")
print("  - Gebouwen_Renovatie_2022sep-2025aug")
print("  - Gebouwen_Renovatie_pct_verschil_36m")

# Toon een preview van de nieuwe data
print("\nVoorbeeld (eerste 5 gemeenten):")
print(result[['TX_REFNIS_NL', 
              'Woningen_Nieuwbouw_2019sep-2022aug',
              'Woningen_Nieuwbouw_2022sep-2025aug',
              'Woningen_Nieuwbouw_pct_verschil_36m']].head())
