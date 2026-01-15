import csv
from collections import defaultdict

# Lees de building stock data en filter voor 2025 en de 3 huizentypen + flatgebouwen
# We willen alleen T1 (Aantal gebouwen) en gebouwtypen R1, R2, R3, R4
gebouwen_data = defaultdict(lambda: {
    'R1': 0,  # Huizen in gesloten bebouwing
    'R2': 0,  # Huizen in halfopen bebouwing
    'R3': 0,  # Huizen in open bebouwing, hoeven en kastelen
    'R4': 0   # Buildings en flatgebouwen met appartementen
})

print("Lezen van building stock data...")
with open('gebouwenpark/building_stock_open_data.txt', 'r', encoding='latin-1') as f:
    for line in f:
        parts = line.strip().split('|')
        if len(parts) < 12:
            continue
        
        year = parts[0]
        cd_refnis = parts[1]
        stat_type = parts[5]
        building_type = parts[8]
        value = parts[11]
        
        # Filter: 2025, T1 (Aantal gebouwen), en gebouwtypen R1-R4
        if year == '2025' and stat_type == 'T1' and building_type in ['R1', 'R2', 'R3', 'R4']:
            try:
                gebouwen_data[cd_refnis][building_type] = int(value)
            except ValueError:
                pass

print(f"Gevonden data voor {len(gebouwen_data)} gemeenten")

# Lees halle-vilvoorde.csv en voeg gebouwenpark data toe
output_data = []

with open('nis/halle-vilvoorde.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        cd_refnis = row['CD_REFNIS']
        
        # Haal gebouwenpark data op voor deze gemeente
        geb_data = gebouwen_data.get(cd_refnis, {
            'R1': 0, 'R2': 0, 'R3': 0, 'R4': 0
        })
        
        # Bereken totaal huizen (R1 + R2 + R3)
        totaal_huizen = geb_data['R1'] + geb_data['R2'] + geb_data['R3']
        flatgebouwen = geb_data['R4']
        
        # Maak nieuwe row met gebouwenpark data
        output_row = {
            'CD_REFNIS': row['CD_REFNIS'],
            'CD_SUP_REFNIS': row['CD_SUP_REFNIS'],
            'TX_REFNIS_NL': row['TX_REFNIS_NL'],
            'Woningen_Nieuwbouw_2024_jan-aug': row['Woningen_Nieuwbouw_2024_jan-aug'],
            'Woningen_Nieuwbouw_2025_jan-aug': row['Woningen_Nieuwbouw_2025_jan-aug'],
            'Woningen_Nieuwbouw_pct_verschil': row['Woningen_Nieuwbouw_pct_verschil'],
            'Gebouwen_Renovatie_2024_jan-aug': row['Gebouwen_Renovatie_2024_jan-aug'],
            'Gebouwen_Renovatie_2025_jan-aug': row['Gebouwen_Renovatie_2025_jan-aug'],
            'Gebouwen_Renovatie_pct_verschil': row['Gebouwen_Renovatie_pct_verschil'],
            'Huizen_totaal_2025': totaal_huizen,
            'Flatgebouwen_2025': flatgebouwen
        }
        
        output_data.append(output_row)

# Schrijf terug naar bestand
with open('nis/halle-vilvoorde.csv', 'w', encoding='utf-8', newline='') as f:
    if output_data:
        fieldnames = list(output_data[0].keys())
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_data)

print(f"Gebouwenpark data toegevoegd aan nis/halle-vilvoorde.csv")
print(f"Totaal {len(output_data)} gemeenten verwerkt")

# Toon enkele voorbeelden
print("\nVoorbeelden:")
for row in output_data[:5]:
    print(f"{row['TX_REFNIS_NL']:30} Huizen: {row['Huizen_totaal_2025']:>6}  Flatgebouwen: {row['Flatgebouwen_2025']:>5}")

