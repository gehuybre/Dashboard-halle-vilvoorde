import pandas as pd

# Lees de bestanden
hv = pd.read_csv('nis/halle-vilvoorde.csv')
huishoudens = pd.read_csv('huishoudens/huishoudens.csv')

# Filter voor 2025 en 2040
hh_2025 = huishoudens[huishoudens['jaar'] == 2025].copy()
hh_2040 = huishoudens[huishoudens['jaar'] == 2040].copy()

# Pivot de data om kolommen te krijgen voor elke huishoudensgrootte
hh_2025_pivot = hh_2025.pivot(index='niscode', columns='aantal_huishoudleden', values='aantal')
hh_2025_pivot.columns = [f'hh_{col}_2025' for col in hh_2025_pivot.columns]

hh_2040_pivot = hh_2040.pivot(index='niscode', columns='aantal_huishoudleden', values='aantal')
hh_2040_pivot.columns = [f'hh_{col}_2040' for col in hh_2040_pivot.columns]

# Merge de data
hh_combined = hh_2025_pivot.join(hh_2040_pivot)

# Bereken absolute en percentage toename voor elke huishoudensgrootte
for grootte in ['1', '2', '3', '4+']:
    col_2025 = f'hh_{grootte}_2025'
    col_2040 = f'hh_{grootte}_2040'
    
    # Absolute toename
    hh_combined[f'hh_{grootte}_abs_toename'] = hh_combined[col_2040] - hh_combined[col_2025]
    
    # Percentage toename
    hh_combined[f'hh_{grootte}_pct_toename'] = ((hh_combined[col_2040] - hh_combined[col_2025]) / hh_combined[col_2025] * 100).round(2)

# Selecteer alleen de kolommen die we nodig hebben (percentage en absolute toename)
toename_cols = []
for grootte in ['1', '2', '3', '4+']:
    toename_cols.append(f'hh_{grootte}_pct_toename')
for grootte in ['1', '2', '3', '4+']:
    toename_cols.append(f'hh_{grootte}_abs_toename')

hh_toename = hh_combined[toename_cols].copy()

# Reset index om niscode als kolom te krijgen
hh_toename = hh_toename.reset_index()

# Merge met halle-vilvoorde.csv op basis van CD_REFNIS (niscode)
result = hv.merge(hh_toename, left_on='CD_REFNIS', right_on='niscode', how='left')

# Verwijder de niscode kolom (duplicaat van CD_REFNIS)
result = result.drop('niscode', axis=1)

# Sla het resultaat op
result.to_csv('nis/halle-vilvoorde.csv', index=False)

print("Huishoudens data succesvol toegevoegd aan nis/halle-vilvoorde.csv")
print(f"\nToegevoegde kolommen:")
for col in toename_cols:
    print(f"  - {col}")
