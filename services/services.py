import random
import asyncio
from aiogram import Bot
from config_data.config import load_config, Config
from aiogram.types import Message
import datetime
from keyboards.keyboards import keyboard_konkurs_False
import pickle


config: Config = load_config()

admins = config.tg_bot.admin_ids

bot: Bot = Bot(config.tg_bot.token, parse_mode="HTML")

# Функция, определяющая администратора
async def admin(message: Message):
    return message.from_user.id in admins



def pobeditel(players_spisok:list, players:dict):
    a = random.choice(players_spisok)
    return players[a]


async def time_all(time:dict, photo:str, text:str, admins:list, time_end:dict):
    task_1 = asyncio.create_task(otpravka_konkurs(time, photo, text, admins))
    task_2 = asyncio.create_task(otpravka_pobeditel_vrem(time_end, admins))
    with open("bylevo.txt", "w") as f:
        f.write("True")

    await task_1
    await task_2

async def otpravka_konkurs(time:dict, photo:str, text:str, admins:list):
    while True:
        data = datetime.datetime.now()
        if (data.year == int(time["year"])
            and data.month == int(time["month"])
            and data.day == int(time["day"])
            and data.hour == int(time["hours"])
            and data.minute == int(time["minute"])):
            await bot.send_photo(chat_id=-1000000000000, photo=photo, caption=text, reply_markup=keyboard_konkurs_False)
            break
        await asyncio.sleep(2)

async def otpravka_pobeditel_vrem(time:dict, admins:list):
    while True:
        await asyncio.sleep(10)
        data = datetime.datetime.now()
        if (data.year == int(time["year"])
            and data.month == int(time["month"])
            and data.day == int(time["day"])
            and data.hour == int(time["hours"])
            and data.minute == int(time["minute"])):
            players_id: list
            players: dict
            pobeditels = []
            with open("players_id.txt", "rb") as f:
                players_id = pickle.load(f)
            with open("players.txt", "rb") as f:
                players = pickle.load(f)
            with open("count_pobeditel.txt", "r") as f:
                count_pobeditel = f.readline()
            text_pobeditels = ""
            for i in range(1, int(count_pobeditel)+1):
                a = random.choice(players_id)
                players_id.remove(a)
                pobeditels += [a]
                text_pobeditels += "[" + str(i) + "." + players[a]["first_name"] + "]"+ "(tg://user?id=" + str(players[a]["id"]) + ")\n"
            if len(pobeditels) == 1:
                await bot.send_message(chat_id=-1000000000000,
                                        parse_mode= "Markdown",
                                        text="Розыгрыш закончился! Победителем стал:\n" + text_pobeditels)
            else:
                await bot.send_message(chat_id=-1000000000000,
                                        parse_mode= "Markdown",
                                        text="Розыгрыш закончился! Победителями стали:\n" + text_pobeditels)
            for i in pobeditels:
                await bot.send_message(chat_id=players[i]["id"], text="Поздравляем, ты победитель розыгрыша!!\nСкоро с вами свяжется администратор")
            with open("bylevo.txt", "w") as f:
                f.write("False")
            break
        await asyncio.sleep(5)
