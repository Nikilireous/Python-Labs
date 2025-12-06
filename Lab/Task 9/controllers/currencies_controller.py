import requests
from models import Currency


def get_all_currencies() -> list[Currency]:
    url = "https://www.cbr-xml-daily.ru/daily_json.js"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверка на ошибки HTTP
        data = response.json()

        currencies_info: list = list(data["Valute"].values())
        all_currencies = [Currency(valute_id=valute['ID'],
                                   num_code=valute['NumCode'],
                                   char_code=valute['CharCode'],
                                   name=valute['Name'],
                                   value=valute['Value'],
                                   nominal=valute['Nominal']) for valute in currencies_info]
        return all_currencies

    except requests.exceptions.RequestException as error:
            raise requests.exceptions.RequestException(f'Ошибка подключения к API ЦБ Российской Федерации: {error}')
    except KeyError as error:
        raise requests.exceptions.RequestException(f'Ошибка подключения к API ЦБ Российской Федерации: {error}')

def update_currency(currency: Currency) -> Currency:
    url = "https://www.cbr-xml-daily.ru/daily_json.js"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверка на ошибки HTTP
        data = response.json()

        new_info: dict = data["Valute"][currency.char_code]
        currency.value = new_info['Value']
        currency.nominal = new_info['Nominal']

        return currency

    except requests.exceptions.RequestException as error:
            raise requests.exceptions.RequestException(f'Ошибка подключения к API ЦБ Российской Федерации: {error}')
    except KeyError as error:
        raise requests.exceptions.RequestException(f'Ошибка подключения к API ЦБ Российской Федерации: {error}')
