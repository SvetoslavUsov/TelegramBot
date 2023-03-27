import asyncio
import pickle
from aiogram import Router, F, Bot
from aiogram.filters import Command, CommandStart, Text
from aiogram.types import (Message, ContentType, ReplyKeyboardRemove,
                            CallbackQuery)
from lexicon.lexicon import LEXICON_COMMAND, NAME_BUTTON
from services.services import (admin, time_all)
from keyboards.keyboards import (klaviatura, klaviatura_data,
                                klaviatura_send_konkurs,
                                button_ex)
from config_data.config import load_config, Config
from services.services_konkurs import proverka_bylevo

time_end: dict = {}
config: Config = load_config()

bot: Bot = Bot(config.tg_bot.token, parse_mode="HTML")

admins = config.tg_bot.admin_ids

player: dict = {}
players_id: list = []
count = 0

# Инициализируем роутер уровня модуля
router: Router = Router()

condition: dict[str: bool]= {
                "name" : False,
                "description": False,
                "data_beginning": False,
                "data_ending": False,
                "photo": False,
                "count_pobeditel": False}

maket_konkurs: dict[str:] = {
                        "name" : "Вы не задали заголовок",
                "description": "Вы не задали описание",
                "data_beginning": "Вы не задали начало розыгрыша",
                "data_ending": "Вы не задали окончание розыгрыша",
                "photo": "Вы не задали фотографию розыгрыша",
                "count_pobeditel": "Вы не задали количество победителей"
                }


# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart(), admin)
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_COMMAND["/start"])

# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands='help'), admin)
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_COMMAND['/help'])

# Этот хэндлер срабатывает на команду /raffle
@router.message(Command(commands='raffle'), admin)
async def process_konkurs_command(message: Message):
    await message.answer(text=LEXICON_COMMAND['/raffle'], reply_markup=klaviatura)


@router.message(Text(text=[NAME_BUTTON["count_pobeditel"]]), admin)
async def process_button_count_pobeditel(message: Message):
    await message.answer(text="Напишите сколько вы хотите побидителей", reply_markup=klaviatura)
    condition["count_pobeditel"] = True



# Этот хэндлер срабатывает на кнопку name
@router.message(Text(text=[NAME_BUTTON["name"]]), admin)
async def process_button_name(message: Message):
    await message.answer(text="Напишите заголовок для розыгрыша", reply_markup=klaviatura)
    condition["name"] = True

# Этот хэндлер срабатывает на кнопку description
@router.message(Text(text=[NAME_BUTTON["description"]]), admin)
async def process_button_description(message: Message):
    await message.answer(text="Напишите описание для розыгрыша", reply_markup=klaviatura)
    condition["description"] = True

    # Этот хэндлер срабатывает на кнопку data
@router.message(Text(text=[NAME_BUTTON["data"]]), admin)
async def process_button_data(message: Message):
    await message.answer(text="Выберите дату", reply_markup=klaviatura_data)

    # Этот хэндлер срабатывает на кнопку data_beginning
@router.message(Text(text=[NAME_BUTTON["data_beginning"]]), admin)
async def process_button_data_beginning(message: Message):
    await message.answer(text="Напишите дату начала розыгрыша в виде: 01.01.2024 12:00", reply_markup=klaviatura_data)
    condition["data_beginning"] = True

    # Этот хэндлер срабатывает на кнопку data_ending
@router.message(Text(text=[NAME_BUTTON["data_ending"]]), admin)
async def process_button_data_ending(message: Message):
    await message.answer(text="Напишите дату окончания розыгрыша в виде: 01.01.2024 12:00", reply_markup=klaviatura_data)
    condition["data_ending"] = True

    # Этот хэндлер срабатывает на кнопку photo
@router.message(Text(text=[NAME_BUTTON["photo"]]), admin)
async def process_button_photo(message: Message):
    await message.answer(text="Отправьте фотографию для розыгрыша", reply_markup=klaviatura)
    condition["photo"] = True


    # Этот хэндлер срабатывает на кнопку compete
@router.message(Text(text=[NAME_BUTTON["complete"]]), admin)
async def process_button_complete(message: Message):
    text = "<b>" + maket_konkurs['name'] + "</b>" + "\n\n" + maket_konkurs["description"] +"\n\n<b>Окончание конкурса: " + maket_konkurs["data_ending"] + "</b>"
    if (maket_konkurs["data_ending"] == "Вы не задали окончание розыгрыша"
        or maket_konkurs["description"] == "Вы не задали описание"
        or maket_konkurs["name"] == "Вы не задали заголовок"
        or maket_konkurs["data_beginning"] == "Вы не задали начало розыгрыша"
        or maket_konkurs["photo"] == "Вы не задали фотографию розыгрыша"
        or maket_konkurs["count_pobeditel"] == "Вы не задали количество победителей"):
        await message.answer(text="Вы не дописали розыгрыш!", reply_markup=klaviatura)
    else:
        await message.answer(text="Розыгрыш отправится в чат и начнётся: " + maket_konkurs["data_beginning"])
        await message.answer(text="Количество победителей будет: " + maket_konkurs["count_pobeditel"])
        await message.answer(text="Вот макет розыгрыша:")
        await bot.send_photo(message.chat.id, maket_konkurs["photo"], caption=text, reply_markup=klaviatura_send_konkurs)

@router.message(Text(text=[NAME_BUTTON["back"]]), admin)
async def process_button_back(message: Message):
    await message.answer(text="Заполните данные для розыгрыша и нажмите кнопку завершить", reply_markup=klaviatura)

@router.message(Text(text=[NAME_BUTTON["send_konkurs"]]), admin)
async def process_button_send(message: Message):
    await message.answer(text="Розыгрыш отправится в нужное время", reply_markup=ReplyKeyboardRemove)
    text = "<b>" + maket_konkurs['name'] + "</b>" + "\n\n" + maket_konkurs["description"] +"\n\n<b>Окончание розыгрыша: " + maket_konkurs["data_ending"] + "</b>"
    a = maket_konkurs["data_beginning"]
    a = a.split()
    a1 = a[0].split(".")
    a2 = a[1].split(":")
    b = maket_konkurs["data_ending"]
    b = b.split()
    b1 = b[0].split(".")
    b2 = b[1].split(":")
    time = {
        "year": a1[2],
        "month": a1[1],
        "day": a1[0],
        "hours": a2[0],
        "minute": a2[1]
        }
    time_end = {
        "year": b1[2],
        "month": b1[1],
        "day": b1[0],
        "hours": b2[0],
        "minute": b2[1]
    }
    with open("time.txt", "wb") as f:
        pickle.dump(time_end, f)

    photo_text = maket_konkurs["photo"]
    text1 = "Участвую!" + "(" + str(0) + ")"
    players_id.clear()
    open('players_id.txt', 'w').close()
    open('players.txt', 'w').close()
    a = asyncio.create_task(time_all(time, photo_text, text, admins, time_end))
    await a
    condition["name"] = False
    maket_konkurs["name"] = "Вы не задали заголовок"
    condition["description"] = False
    maket_konkurs["description"] = "Вы не задали описание"
    condition["data_beginning"] = False
    maket_konkurs["data_beginning"] = "Вы не задали начало розыгрыша"
    condition["data_ending"] = False
    maket_konkurs["data_ending"] = "Вы не задали окончание розыгрыша"
    condition["photo"] = False
    maket_konkurs["photo"] = "Вы не задали фотографию розыгрыша"
    condition["count_pobeditel"] = False
    maket_konkurs["count_pobeditel"] = "Вы не задали количество победителей"


@router.callback_query(Text(text="button_konkurs_False"), proverka_bylevo)
async def process_button_konkurs_False(callback: CallbackQuery):
    if not proverka_bylevo:
        await callback.message.edit_reply_markup()
    if callback.from_user.id not in players_id and proverka_bylevo:
        player[callback.from_user.id] = {
            "username": callback.from_user.username,
            "first_name": callback.from_user.first_name,
            "last_name": callback.from_user.last_name,
            "id": callback.from_user.id
        }
        players_id.append(callback.from_user.id)
        print(players_id)
        await callback.answer(text="Поздравляем! Вы теперь участвуете в розыгрыше! Удачи!",
                                show_alert=True)
        text1 = "Участвую!" + "(" + str(len(players_id)) + ")"
        await callback.message.edit_reply_markup(reply_markup=await button_ex(text=text1))
        await asyncio.sleep(2)
        open('players_id.txt', 'w').close()
        open('players.txt', 'w').close()
        with open("players.txt", "wb") as f:
            pickle.dump(player, f)
        with open("players_id.txt", "wb") as f:
            pickle.dump(players_id, f)
    else:
        if proverka_bylevo:
            await callback.answer(text="Вы уже являетесь участником данного розыгрыша!",
                                show_alert=True)
    await callback.answer()


@router.message(lambda x:condition["count_pobeditel"], admin, F.content_type == ContentType.TEXT)
async def process_maket_count_pobeditel(message: Message):
    maket_konkurs["count_pobeditel"] = message.text
    condition["count_pobeditel"] = False
    open("count_pobeditel.txt", "w").close()
    with open("count_pobeditel.txt", "w") as f:
        f.write(message.text)
    await message.answer(text="Количество победителей записано")

@router.message(lambda x :condition["name"], admin, F.content_type == ContentType.TEXT)
async def process_maket_name(message: Message):
    maket_konkurs["name"] = message.text
    condition["name"] = False
    await message.answer(text="Заголовок записан")

@router.message(lambda x:condition["description"], admin, F.content_type == ContentType.TEXT)
async def process_maket_description(message: Message):
    maket_konkurs["description"] = message.text
    condition["description"] = False
    await message.answer(text="Описание записано")

@router.message(lambda x:condition["data_beginning"], admin, F.content_type == ContentType.TEXT)
async def process_maket_data_beginning(message: Message):
    maket_konkurs["data_beginning"] = message.text
    condition["data_beginning"] = False
    await message.answer(text="Дата начала записана")

@router.message(lambda x:condition["data_ending"], admin, F.content_type == ContentType.TEXT)
async def process_maket_data_ending(message: Message):
    maket_konkurs["data_ending"] = message.text
    condition["data_ending"]
    await message.answer(text="Дата окончания записана")

@router.message(lambda x:condition["photo"], admin, F.content_type == ContentType.PHOTO)
async def process_maket_photo(message: Message):
    maket_konkurs["photo"] = message.photo[0].file_id
    await message.answer(text="Фото запомнилось")