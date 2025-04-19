import requests
import pandas as pd
import json

# Pobranie danych z API World Bank (rok 1939–2023)
url = (
    "http://api.worldbank.org/v2/country/PL/indicator/SP.DYN.TFRT.IN"
    "?date=1939:2023&format=json&per_page=10000"
)
resp = requests.get(url)
data = resp.json()[1]

# Przetworzenie na DataFrame
df = pd.DataFrame(data)[['date','value']]
df.columns = ['Year','FertilityRate']
df['Year'] = df['Year'].astype(int)
df['FertilityRate'] = df['FertilityRate'].astype(float, errors='ignore')
# Wypełnienie braków dla lat <1960
all_years = pd.DataFrame({'Year': list(range(1939, 2024))})
df = all_years.merge(df, on='Year', how='left')

# Czyszczenie danych - usunięcie wierszy bez wartości FertilityRate
df = df.dropna(subset=['FertilityRate'])
print(f"Liczba wierszy po usunięciu braków danych: {len(df)}")

# Przygotowanie danych do formatu JSON
json_data = []
for _, row in df.iterrows():
    json_data.append({
        "year": int(row['Year']),
        "tfr": float(row['FertilityRate'])
    })

# Zapis do JSON
json_path = 'fertility_poland_1939_2023.json'
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(json_data, f, indent=2)
print(f"Zapisano dane do pliku: {json_path}")
