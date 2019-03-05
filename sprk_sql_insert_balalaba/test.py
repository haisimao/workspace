import re


comp_name = 'S.A. LA NACION (CUIT 30-50008962-4)'
print(re.sub(r'\(.*\)', '', comp_name), comp_name)
print(comp_name)
comp_name = re.sub(r'\(.*\)', '', comp_name)
print(comp_name)
comp_name = comp_name.replace('2', '')
comp_name = comp_name.strip('. 123456789')
comp_name.strip()
print(comp_name)

if ' INC' in comp_name:
    comp_name = comp_name.split(' INC')[0] + ' INC'
print(comp_name)
