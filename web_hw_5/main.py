import aiohttp
import asyncio

from datetime import datetime, timedelta

CURRENCIES = ['EUR', 'USD']


def user_data():
    currency = input('Enter currency must be exchange: ')
    CURRENCIES.append(currency.upper())
    while True:
        change_date = datetime.strptime(input('Enter date for currency exchange(format[dd.mm.year], '
                                              'max 10 days ago):'), '%d.%m.%Y')
        if datetime.now() - change_date < timedelta(days=10):
            return change_date


def adding_result(data: dict) -> dict:
    result = {data.get('currency'): {'sale': data.get('saleRate'), 'purchase': data.get('purchaseRate')}}
    if result.get(data.get('currency')).get('sale'):
        return result
    else:
        return {data.get('currency'): {'sale': data.get('saleRateNB'), 'purchase': data.get('purchaseRateNB')}}


async def exchange_rate(change_date) -> dict:
    change_date = datetime.strftime(change_date, '%d.%m.%Y')

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f'https://api.privatbank.ua/p24api/exchange_rates?date={change_date}') as responce:
                if responce.status == 200:
                    result = await responce.json()
                else:
                    print(f'Error status: {responce.status}')
        except aiohttp.ClientConnectorError as er:
            print(f'Connection error: {er}')

        if result:
            exchange_result = {}
            currencies = result.get('exchangeRate')
            for currency_exchange in currencies:
                if currency_exchange.get('currency') in CURRENCIES:
                    if not exchange_result:
                        exchange_result = {result.get('date'): adding_result(currency_exchange)}
                    else:
                        exchange_result.update(adding_result(currency_exchange))
        return exchange_result


def main():
    need_data = user_data()
    res = asyncio.run(exchange_rate(need_data))
    return res


if __name__ == '__main__':
    print(main())