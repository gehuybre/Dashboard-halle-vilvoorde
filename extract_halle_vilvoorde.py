import csv

# Lees refnis.csv om alle gemeenten van Halle-Vilvoorde te vinden
halle_vilvoorde_codes = set()

with open('nis/refnis.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        # LVL_REFNIS 4 = gemeente niveau, CD_SUP_REFNIS = 23000 is Halle-Vilvoorde
        if row['CD_SUP_REFNIS'] == '23000':
            halle_vilvoorde_codes.add(row['CD_REFNIS'])

print(f"Gevonden {len(halle_vilvoorde_codes)} gemeenten in Halle-Vilvoorde")

# Lees fusies-2025.csv en filter de gemeenten
halle_vilvoorde_fusies = []

with open('nis/fusies-2025.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f, delimiter='\t')
    for row in reader:
        fuserende = row['Fuserende gemeenten,'].strip()
        nieuwe = row['Nieuwe gemeenten'].strip()
        
        # Zoek NIS codes in de fuserende gemeenten
        import re
        codes = re.findall(r'\((\d+)\)', fuserende + nieuwe)
        
        # Check of een van de codes in Halle-Vilvoorde zit
        if any(code in halle_vilvoorde_codes for code in codes):
            halle_vilvoorde_fusies.append(row)
            print(f"Gevonden: {fuserende} -> {nieuwe}")

print(f"\nTotaal {len(halle_vilvoorde_fusies)} fusies gevonden in Halle-Vilvoorde")

# Schrijf resultaat naar nieuw bestand met CD_SUP_REFNIS en TX_REFNIS_NL
# We moeten de gemeentenamen en codes matchen met refnis.csv
output_data = []

for fusie in halle_vilvoorde_fusies:
    fuserende = fusie['Fuserende gemeenten,'].strip()
    nieuwe = fusie['Nieuwe gemeenten'].strip()
    
    import re
    codes = re.findall(r'\((\d+)\)', fuserende + nieuwe)
    
    # Voor elke code, zoek de TX_REFNIS_NL op
    for code in codes:
        if code in halle_vilvoorde_codes:
            # Zoek in refnis.csv
            with open('nis/refnis.csv', 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['CD_REFNIS'] == code and row['DT_VLDT_END'] == '31/12/9999':
                        output_data.append({
                            'CD_SUP_REFNIS': row['CD_SUP_REFNIS'],
                            'TX_REFNIS_NL': row['TX_REFNIS_NL']
                        })
                        break

# Schrijf naar nieuw bestand
with open('nis/halle-vilvoorde-fusies.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['CD_SUP_REFNIS', 'TX_REFNIS_NL'])
    writer.writeheader()
    writer.writerows(output_data)

print(f"\nResultaat geschreven naar nis/halle-vilvoorde-fusies.csv ({len(output_data)} rijen)")
