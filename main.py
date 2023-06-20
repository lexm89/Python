from time import sleep

import requests
from aiogram import Bot, Dispatcher, executor, types
from bs4 import BeautifulSoup

from config import admin
from config import token

bot = Bot(token=token)
dp = Dispatcher(bot)

headres = {
    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'

}


@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer(f"Добро пожаловать. Заходте в наш чат https://t.me/speczapchasti_chat")


@dp.message_handler(commands="sel")
async def boart_new(message: types.Message):
    if message.from_user.id == admin:
        await bot.send_message(message.from_user.id, 'Вы авторизовались как администратор')
        await message.delete()

        get_url = []
        url = "https://xn--80aatggg1adtkd7c1e.xn--p1ai/select/?sCat=kuplyu-zapchasti"
        response = requests.get(url, headers=headres)
        print(response.status_code)

        src = response.text
        soup = BeautifulSoup(src, "lxml")
        elem = soup.find_all("td", id="safecrowtd", class_="text-left")

        for i in elem[2:]:
            link = i.find("a").get("href")
            get_url.append(link)

        for kard in sorted(get_url):
            url = kard
            response = requests.get(url, headers=headres)
            sleep(3)

            src = response.text
            soup = BeautifulSoup(src, "lxml")

            marka = soup.find("li", id="cp_marka").text
            card = soup.find("div", id="hypercontext").text.replace("\n", "")
            kontact = soup.find("li", id="cp_telef").find("a").get("href")

            await message.answer(f"{marka}\n"
                                 f" {card}\n"
                                 f" {kontact}")
    else:
        await message.answer(f"Я тебя не понимаю.")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
