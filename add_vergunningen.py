import csv
from collections import defaultdict

# Eerst: lees alleen ACTIEVE gemeenten uit Halle-Vilvoorde (DT_VLDT_END = 31/12/9999)
hv_gemeenten = {}
with open('nis/refnis.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Filter op arrondissement Halle-Vilvoorde (23000) EN actieve gemeenten
        if row['CD_SUP_REFNIS'] == '23000' and row['DT_VLDT_END'] == '31/12/9999':
            cd_refnis = row['CD_REFNIS']
            tx_refnis_nl = row['TX_REFNIS_NL']
            hv_gemeenten[tx_refnis_nl] = cd_refnis

print(f"Gevonden {len(hv_gemeenten)} actieve gemeenten (deelgemeenten uitgefilterd)")

# Lees bouwvergunningen en groepeer per gemeente
vergunningen_data = defaultdict(lambda: {
    'MS_DWELLING_RES_NEW_2024': 0,
    'MS_DWELLING_RES_NEW_2025': 0,
    'MS_BUILDING_RES_RENOVATION_2024': 0,
    'MS_BUILDING_RES_RENOVATION_2025': 0
})

with open('vergunningen/bouwvergunningen.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        refnis = row['REFNIS']
        year = int(row['CD_YEAR'])
        period = int(row['CD_PERIOD'])
        
        # Filter eerste 8 maanden van 2024 en 2025
        if period >= 1 and period <= 8 and year in [2024, 2025]:
            # MS_DWELLING_RES_NEW
            if row['MS_DWELLING_RES_NEW']:
                value = float(row['MS_DWELLING_RES_NEW'])
                if year == 2024:
                    vergunningen_data[refnis]['MS_DWELLING_RES_NEW_2024'] += value
                else:
                    vergunningen_data[refnis]['MS_DWELLING_RES_NEW_2025'] += value
            
            # MS_BUILDING_RES_RENOVATION
            if row['MS_BUILDING_RES_RENOVATION']:
                value = float(row['MS_BUILDING_RES_RENOVATION'])
                if year == 2024:
                    vergunningen_data[refnis]['MS_BUILDING_RES_RENOVATION_2024'] += value
                else:
                    vergunningen_data[refnis]['MS_BUILDING_RES_RENOVATION_2025'] += value

# Lees de huidige halle-vilvoorde.csv en voeg vergunningen toe
# Maar alleen voor actieve gemeenten
output_data = []

with open('nis/halle-vilvoorde.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        gemeente_naam = row['TX_REFNIS_NL']
        
        # Skip inactieve gemeenten (deelgemeenten)
        if gemeente_naam not in hv_gemeenten:
            continue
            
        cd_refnis = hv_gemeenten[gemeente_naam]
        
        # Haal vergunningen data op voor deze gemeente
        verg_data = vergunningen_data.get(cd_refnis, {
            'MS_DWELLING_RES_NEW_2024': 0,
            'MS_DWELLING_RES_NEW_2025': 0,
            'MS_BUILDING_RES_RENOVATION_2024': 0,
            'MS_BUILDING_RES_RENOVATION_2025': 0
        })
        
        # Bereken % verschil
        # Voor MS_DWELLING_RES_NEW
        if verg_data['MS_DWELLING_RES_NEW_2024'] > 0:
            pct_dwelling_new = ((verg_data['MS_DWELLING_RES_NEW_2025'] - verg_data['MS_DWELLING_RES_NEW_2024']) / 
                               verg_data['MS_DWELLING_RES_NEW_2024'] * 100)
        else:
            pct_dwelling_new = None if verg_data['MS_DWELLING_RES_NEW_2025'] == 0 else float('inf')
        
        # Voor MS_BUILDING_RES_RENOVATION
        if verg_data['MS_BUILDING_RES_RENOVATION_2024'] > 0:
            pct_building_renovation = ((verg_data['MS_BUILDING_RES_RENOVATION_2025'] - verg_data['MS_BUILDING_RES_RENOVATION_2024']) / 
                                       verg_data['MS_BUILDING_RES_RENOVATION_2024'] * 100)
        else:
            pct_building_renovation = None if verg_data['MS_BUILDING_RES_RENOVATION_2025'] == 0 else float('inf')
        
        output_row = {
            'CD_REFNIS': cd_refnis,
            'CD_SUP_REFNIS': row['CD_SUP_REFNIS'],
            'TX_REFNIS_NL': row['TX_REFNIS_NL'],
            'Woningen_Nieuwbouw_2024_jan-aug': verg_data['MS_DWELLING_RES_NEW_2024'],
            'Woningen_Nieuwbouw_2025_jan-aug': verg_data['MS_DWELLING_RES_NEW_2025'],
            'Woningen_Nieuwbouw_pct_verschil': round(pct_dwelling_new, 2) if pct_dwelling_new is not None and pct_dwelling_new != float('inf') else '',
            'Gebouwen_Renovatie_2024_jan-aug': verg_data['MS_BUILDING_RES_RENOVATION_2024'],
            'Gebouwen_Renovatie_2025_jan-aug': verg_data['MS_BUILDING_RES_RENOVATION_2025'],
            'Gebouwen_Renovatie_pct_verschil': round(pct_building_renovation, 2) if pct_building_renovation is not None and pct_building_renovation != float('inf') else ''
        }
        
        output_data.append(output_row)

# Schrijf naar nieuw bestand
with open('nis/halle-vilvoorde.csv', 'w', encoding='utf-8', newline='') as f:
    fieldnames = [
        'CD_REFNIS',
        'CD_SUP_REFNIS', 
        'TX_REFNIS_NL',
        'Woningen_Nieuwbouw_2024_jan-aug',
        'Woningen_Nieuwbouw_2025_jan-aug',
        'Woningen_Nieuwbouw_pct_verschil',
        'Gebouwen_Renovatie_2024_jan-aug',
        'Gebouwen_Renovatie_2025_jan-aug',
        'Gebouwen_Renovatie_pct_verschil'
    ]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(output_data)

print(f"Vergunningen data toegevoegd aan nis/halle-vilvoorde.csv")
print(f"Totaal {len(output_data)} actieve gemeenten verwerkt")
print(f"{102 - len(output_data)} inactieve deelgemeenten verwijderd")
