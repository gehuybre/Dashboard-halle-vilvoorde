import csv

# Lees refnis.csv en filter gemeenten uit Halle-Vilvoorde (CD_SUP_REFNIS = 23000)
output_data = []

with open('nis/refnis.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Filter op arrondissement Halle-Vilvoorde (23000)
        if row['CD_SUP_REFNIS'] == '23000':
            output_data.append({
                'CD_SUP_REFNIS': row['CD_SUP_REFNIS'],
                'TX_REFNIS_NL': row['TX_REFNIS_NL']
            })

print(f"Gevonden {len(output_data)} gemeenten/deelgemeenten in Halle-Vilvoorde")

# Schrijf naar nieuw bestand
with open('nis/halle-vilvoorde.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['CD_SUP_REFNIS', 'TX_REFNIS_NL'])
    writer.writeheader()
    writer.writerows(output_data)

print(f"Resultaat geschreven naar nis/halle-vilvoorde.csv")
