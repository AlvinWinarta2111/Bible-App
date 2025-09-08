import csv

file_path = "C:\\Users\\alvin\\VS_WS\\Bible\\data\\tb.csv"

kitab_codes = set()
with open(file_path, 'r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        code = row['kitab'].strip()
        kitab_codes.add(code)

print("Unique kitab codes in CSV:")
for code in sorted(kitab_codes):
    print(code)
