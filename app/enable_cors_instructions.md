# Instrukcja włączenia CORS w aplikacji Flask

## Co to jest CORS?

CORS (Cross-Origin Resource Sharing) to mechanizm bezpieczeństwa przeglądarek, który blokuje żądania HTTP z jednej domeny (origin) do innej. Jest to istotne, gdy frontend (np. strona HTML otwarta bezpośrednio z dysku) próbuje komunikować się z API na innym serwerze.

## Zmiany, które zostały wprowadzone

1. Dodano pakiet `flask-cors` do `requirements.txt`
2. Zmodyfikowano plik `app.py`, aby włączyć CORS dla wszystkich źródeł

## Jak uruchomić serwer z włączonym CORS

1. Zainstaluj nową zależność:
```bash
pip install flask-cors
```

2. Upewnij się, że plik `app.py` zawiera następujące zmiany:
```python
from flask import Flask, request, jsonify
from flask_cors import CORS  # Nowy import
from models.forecaster import TBATSForecaster
from utils.data_handler import preprocess_data, postprocess_results

app = Flask(__name__)
# Włączenie CORS dla wszystkich źródeł
CORS(app, resources={r"/*": {"origins": "*"}})
```

3. Uruchom serwer:
```bash
python app.py
```

4. Serwer będzie dostępny pod adresem `http://localhost:5000` i będzie akceptował żądania z dowolnego źródła, w tym z plików HTML otwartych bezpośrednio z dysku.

## Testowanie

Aby przetestować, czy CORS działa poprawnie:

1. Otwórz plik `presentation_chart/index.html` bezpośrednio w przeglądarce
2. Otwórz konsolę deweloperską (F12 lub Ctrl+Shift+I)
3. Sprawdź, czy nie ma błędów CORS
4. Wykres powinien załadować dane z API zamiast używać danych lokalnych

## Uwagi dotyczące bezpieczeństwa

Włączenie CORS dla wszystkich źródeł (`"origins": "*"`) jest odpowiednie do celów rozwojowych, ale w środowisku produkcyjnym należy rozważyć ograniczenie dostępu tylko do zaufanych domen.

Aby ograniczyć CORS do konkretnych domen, zmień konfigurację:

```python
CORS(app, resources={r"/*": {"origins": "https://twojadomena.com"}})
```

lub dla wielu domen:

```python
CORS(app, resources={r"/*": {"origins": ["https://domena1.com", "https://domena2.com"]}})