import requests


def get_currencies(currency_codes: list | None = None) -> dict:
    url = "https://www.cbr-xml-daily.ru/daily_json.js"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверка на ошибки HTTP
        data = response.json()
        currencies = {}

        if "Valute" in data:
            if not currency_codes:
                currency_codes: list = list(data["Valute"].keys())

            for code in currency_codes:
                if code in data["Valute"]:
                    currencies[code] = data["Valute"][code]
                else:
                    currencies[code] = f"Код валюты '{code}' не найден."
        return currencies

    except requests.exceptions.RequestException as error:
            raise requests.exceptions.RequestException(f'Ошибка подключения к API ЦБ Российской Федерации: {error}')

# print(get_currencies(1233))