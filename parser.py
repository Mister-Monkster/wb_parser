import asyncio
from typing import Optional

import requests

async def get_response_json(article: str) -> dict:
    response = requests.get(f"https://card.wb.ru/cards/v2/detail?appType=1&curr=rub&dest=123585553&hide_dtype=13&spp=30&ab_testing=false&lang=ru&nm={article}")
    response_json = response.json()
    return response_json


async def parse_wb_json(data: dict) -> dict | None:
    try:
        name = data.get('data')['products'][0]['name']
        basic_price = str(data.get('data')['products'][0]['sizes'][0]['price']["basic"] // 100) + ' ₽'
        current_price = str(data.get('data')['products'][0]['sizes'][0]['price']["product"] // 100) + ' ₽'
        return {"name":name,
         "basic_price": basic_price,
         "current_price": current_price}
    except IndexError:
        return None


async def get_wb_info(article: str) -> Optional[dict]:
    response_json = await get_response_json(article)
    res = await parse_wb_json(response_json)
    return res


"""Тестовые данные"""

print(asyncio.run(get_wb_info("2"))) # -> None

print(asyncio.run(get_wb_info("260908299"))) # -> Cмартфон Apple iPhone 16 Pro Золотистый/Desert 256 ГБ

print(asyncio.run(get_wb_info("237916921"))) # -> Видеокарта GeForce RTX 3060

print(asyncio.run(get_wb_info("177228710"))) # -> Искусственные растения, цветы в горшке декор для интерьера



