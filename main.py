import asyncio
from datetime import datetime, timedelta
import logging


from aiohttp import ClientSession, ClientConnectorError


async def request(url: str):
    async with ClientSession() as session:
        try:
            async with session.get(url) as resp:
                if resp.ok:
                    r = await resp.json()
                    return r
                logging.error(f"Error status: {resp.status} for {url}")
                return None
        except ClientConnectorError as err:
            logging.error(f"Connection error: {str(err)}")
            return None


def pb_handler(result):
    exc1 = result["exchangeRate"][8] # EURO
    exc2 = result["exchangeRate"][23] #USD
    return (f"EUR: buy: {exc1['purchaseRate']}, sale: {exc1['saleRate']} \n"
            f"USD: buy: {exc2['purchaseRate']}, sale: {exc2['saleRate']}")



async def get_exchange(url, handler):
    result = await request(url)
    if result:
        return handler(result)
    return "Failed to retrieve data"


if __name__ == '__main__':
    print('Hi, I can show you the currency exchange rates for the last few days, from 1 to 10')
    while True:
        number = input("Enter the desired number of days:")
        try:
            n = int(number)
            if 1 <= n <= 10:
                for i in range(n):
                    day = (datetime.now().date() - timedelta(i)).strftime("%d.%m.%Y")
                    print(day)
                    URL_PB = f"https://api.privatbank.ua/p24api/exchange_rates?json&date={day}"
                    result = asyncio.run(get_exchange(URL_PB, pb_handler))
                    print(result)
                break
            else:
                print("Incorrect value")
        except ValueError:
            print("Enter the number")

