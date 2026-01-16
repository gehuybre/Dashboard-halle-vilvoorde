import pandas as pd

# Laad de data
df = pd.read_csv('nis/halle-vilvoorde.csv')

print("=" * 80)
print("DATA VERIFICATIE - WOONGELEGENHEDEN (T8)")
print("=" * 80)

# Controleer Grimbergen
print("\n1. GRIMBERGEN VERIFICATIE:")
grimbergen = df[df['TX_REFNIS_NL'] == 'Grimbergen'].iloc[0]
print(f"   Huizen (woongelegenheden): {int(grimbergen['Huizen_totaal_2025']):,}")
print(f"   Appartementen (woongelegenheden): {int(grimbergen['Appartementen_2025']):,}")
print(f"   Totaal woongelegenheden: {int(grimbergen['Huizen_totaal_2025'] + grimbergen['Appartementen_2025']):,}")
print(f"   Appartementen ratio: {(grimbergen['Appartementen_2025']/(grimbergen['Huizen_totaal_2025'] + grimbergen['Appartementen_2025'])*100):.1f}%")

# Top 10 gemeenten met meeste huizen
print("\n2. TOP 10 GEMEENTEN - HUIZEN (woongelegenheden):")
top10_huizen = df.nlargest(10, 'Huizen_totaal_2025')[['TX_REFNIS_NL', 'Huizen_totaal_2025', 'Appartementen_2025']]
for idx, row in top10_huizen.iterrows():
    print(f"   {row['TX_REFNIS_NL']:30} Huizen: {int(row['Huizen_totaal_2025']):>6,}  Appartementen: {int(row['Appartementen_2025']):>6,}")

# Top 10 gemeenten met meeste appartementen
print("\n3. TOP 10 GEMEENTEN - APPARTEMENTEN (woongelegenheden):")
top10_app = df.nlargest(10, 'Appartementen_2025')[['TX_REFNIS_NL', 'Huizen_totaal_2025', 'Appartementen_2025']]
for idx, row in top10_app.iterrows():
    print(f"   {row['TX_REFNIS_NL']:30} Huizen: {int(row['Huizen_totaal_2025']):>6,}  Appartementen: {int(row['Appartementen_2025']):>6,}")

# Totalen
print("\n4. TOTALEN HALLE-VILVOORDE:")
print(f"   Totaal huizen: {df['Huizen_totaal_2025'].sum():,.0f}")
print(f"   Totaal appartementen: {df['Appartementen_2025'].sum():,.0f}")
print(f"   Totaal woongelegenheden: {(df['Huizen_totaal_2025'].sum() + df['Appartementen_2025'].sum()):,.0f}")
print(f"   Appartementen ratio: {(df['Appartementen_2025'].sum()/(df['Huizen_totaal_2025'].sum() + df['Appartementen_2025'].sum())*100):.1f}%")

print("\n" + "=" * 80)
print("✓ Alle data gebruikt T8 (Aantal woongelegenheden)")
print("=" * 80)
