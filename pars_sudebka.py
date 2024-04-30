import disnake
import asyncio
from disnake import Webhook, Embed
import aiohttp
from bs4 import BeautifulSoup
import datetime
import json


def save_seen_comps_to_file(seen_comps):
    with open('seen_comps.json', 'w', encoding='utf-8') as f:
        json.dump(list(seen_comps), f, ensure_ascii=False)


def load_seen_comps_from_file():
    try:
        with open('seen_comps.json', 'r', encoding='utf-8') as f:
            return set(json.load(f))
    except FileNotFoundError:
        return set()


async def foo(isk, ss, session):
    webhook = Webhook.from_url(
        'webhook-url', #url ссылка на вебхук
        session=session)
    embed = disnake.Embed(
        title=f'{isk}',
        description="Нужно обработать за 40 часов. Ссылка выше.\nЕсли вы берёте иск, отпишите или поставьте реакцию.\nПосле взятия иска галку.",
        color=0x2F3136,
        url=f'{ss}',
        timestamp=datetime.datetime.now(),
    )
    embed.set_thumbnail(
        url="https://lh7-us.googleusercontent.com/zoza4WDSgR0HKdwEqSV0zrK0gB7wjTT2aIX4aj_KyZDLVlGkUPNNl9oJPJWKOFIPF_7iywOcKLnRyEbE-izfH_PwfV5TQE7Jnczdjshp2WhgPvo9Pk00lZ8Q7R-i5wNZ8X-E0QprduumjIBlgR9CAGA")
    embed.set_footer(
        text="by x1she",
        icon_url="https://lh7-us.googleusercontent.com/zoza4WDSgR0HKdwEqSV0zrK0gB7wjTT2aIX4aj_KyZDLVlGkUPNNl9oJPJWKOFIPF_7iywOcKLnRyEbE-izfH_PwfV5TQE7Jnczdjshp2WhgPvo9Pk00lZ8Q7R-i5wNZ8X-E0QprduumjIBlgR9CAGA",
    )

    await webhook.send('<@&1119326877757227059> <@&1119326877740441674>', embed=embed)


async def main_loop():
    seen_comps = load_seen_comps_from_file()
# cookies и headers с сайта - https://curlconverter.com/ (как получить curl есть много гайдов)
    cookies = {
    'R3ACTLB': '8f70d2b3e40b57e28c9c29d4f2929a30',
    'xf_csrf': 'ngZbVJHmIS0Qqm3v',
    '_ga_319PFF93QY': 'GS1.1.1714512853.1.1.1714512957.0.0.0',
    '_ga': 'GA1.1.1217501711.1714512853',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'DNT': '1',
    'Sec-GPC': '1',
    'Connection': 'keep-alive',
    # 'Cookie': 'R3ACTLB=8f70d2b3e40b57e28c9c29d4f2929a30; xf_csrf=ngZbVJHmIS0Qqm3v; _ga_319PFF93QY=GS1.1.1714512853.1.1.1714512957.0.0.0; _ga=GA1.1.1217501711.1714512853',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'If-Modified-Since': 'Tue, 30 Apr 2024 21:36:22 GMT',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
}

    while True:
        async with aiohttp.ClientSession(cookies=cookies, headers=headers) as session:
            response = await session.get('https://forum.majestic-rp.ru/forums/okruzhnoj-sud.781/')
            soup = BeautifulSoup(await response.text(), 'html.parser')
            items1 = soup.find('div', class_='structItemContainer-group js-threadList')
            items = items1.findAll('div', class_='structItem-title')

            for item in items:
                title = item.find('a', class_='').get_text(strip=True)
                link = 'https://forum.majestic-rp.ru' + item.find('a', class_='').get('href')
                if link not in seen_comps:
                    seen_comps.add(link)
                    save_seen_comps_to_file(seen_comps)
                    await foo(title, link, session)

        await asyncio.sleep(7200) # Перепроверка страницы раз в 7200 секунд


asyncio.run(main_loop())
