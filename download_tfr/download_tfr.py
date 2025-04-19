import requests
import pandas as pd

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

# Zapis do CSV
csv_path = 'fertility_poland_1939_2023.csv'
df.to_csv(csv_path, index=False, float_format='%.2f')
print(f"Zapisano dane do pliku: {csv_path}")
