import csv
from collections import defaultdict

# Lees de building stock data en filter voor 2025 en de 3 huizentypen + appartementen
# We willen alleen T8 (Aantal woongelegenheden) en gebouwtypen R1, R2, R3, R4
gebouwen_data = defaultdict(lambda: {
    'R1': 0,  # Huizen in gesloten bebouwing
    'R2': 0,  # Huizen in halfopen bebouwing
    'R3': 0,  # Huizen in open bebouwing, hoeven en kastelen
    'R4': 0   # Appartementen in buildings en flatgebouwen
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
        
        # Filter: 2025, T8 (Aantal woongelegenheden), en gebouwtypen R1-R4
        if year == '2025' and stat_type == 'T8' and building_type in ['R1', 'R2', 'R3', 'R4']:
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
        appartementen = geb_data['R4']
        
        # Maak nieuwe row met gebouwenpark data - kopieer alle bestaande kolommen
        output_row = row.copy()
        
        # Verwijder oude Flatgebouwen_2025 kolom als die bestaat
        if 'Flatgebouwen_2025' in output_row:
            del output_row['Flatgebouwen_2025']
        
        # Update/voeg gebouwenpark kolommen toe
        output_row['Huizen_totaal_2025'] = totaal_huizen
        output_row['Appartementen_2025'] = appartementen
        
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
    print(f"{row['TX_REFNIS_NL']:30} Huizen: {row['Huizen_totaal_2025']:>6}  Appartementen: {row['Appartementen_2025']:>5}")

