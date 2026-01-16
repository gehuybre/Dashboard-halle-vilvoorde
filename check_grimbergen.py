# T1 = Aantal GEBOUWEN (huidige data)
t1_r1 = 3831
t1_r2 = 3085
t1_r3 = 3732
t1_r4 = 1153

# T8 = Aantal WOONGELEGENHEDEN (wat het zou moeten zijn)
t8_r1 = 4082
t8_r2 = 3147
t8_r3 = 3752
t8_r4 = 6104

print('HUIDIG (T1 - Aantal gebouwen):')
print(f'  R1: {t1_r1:>6}, R2: {t1_r2:>6}, R3: {t1_r3:>6}, R4: {t1_r4:>6}')
print(f'  Huizen totaal (R1+R2+R3): {t1_r1+t1_r2+t1_r3:>6}')
print(f'  Flatgebouwen (R4):        {t1_r4:>6}')
print()
print('GEWENST (T8 - Aantal woongelegenheden):')
print(f'  R1: {t8_r1:>6}, R2: {t8_r2:>6}, R3: {t8_r3:>6}, R4: {t8_r4:>6}')
print(f'  Huizen totaal (R1+R2+R3): {t8_r1+t8_r2+t8_r3:>6}')
print(f'  Appartementen (R4):       {t8_r4:>6}')
print()
print('VERSCHIL:')
print(f'  Huizen:       {(t8_r1+t8_r2+t8_r3) - (t1_r1+t1_r2+t1_r3):>6} (+{((t8_r1+t8_r2+t8_r3)/(t1_r1+t1_r2+t1_r3)-1)*100:.1f}%)')
print(f'  Appartementen: {t8_r4 - t1_r4:>6} (+{(t8_r4/t1_r4-1)*100:.1f}%)')
print()
print('Note: Bij woongelegenheden tel je APPARTEMENTEN ipv flatGEBOUWEN!')
