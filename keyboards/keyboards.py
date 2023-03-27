from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from lexicon.lexicon import NAME_BUTTON


# ------- Создаем игровую клавиатуру без использования билдера -------

# Создаем кнопки игровой клавиатуры
button_name: KeyboardButton = KeyboardButton(text=NAME_BUTTON['name'])
button_description: KeyboardButton = KeyboardButton(text=NAME_BUTTON['description'])
button_data: KeyboardButton = KeyboardButton(text=NAME_BUTTON['data'])
button_data_beginning: KeyboardButton = KeyboardButton(text=NAME_BUTTON["data_beginning"])
button_data_ending: KeyboardButton = KeyboardButton(text=NAME_BUTTON["data_ending"])
button_count_pobeditel: KeyboardButton = KeyboardButton(text=NAME_BUTTON["count_pobeditel"])
button_photo: KeyboardButton = KeyboardButton(text=NAME_BUTTON["photo"])
button_complete: KeyboardButton = KeyboardButton(text=NAME_BUTTON["complete"])
button_back: KeyboardButton = KeyboardButton(text=NAME_BUTTON["back"])
button_yes: KeyboardButton = KeyboardButton(text=NAME_BUTTON["yes"])
button_send: KeyboardButton = KeyboardButton(text=NAME_BUTTON["send_konkurs"])
button_konkurs_False: InlineKeyboardButton = InlineKeyboardButton(
                                                    text="Участвую!(0)",
                                                    callback_data="button_konkurs_False")
button_konkurs_True: InlineKeyboardButton = InlineKeyboardButton(
                                                    text="Ты уже участник!",
                                                    callback_data="button_konkurs_True")


# Создаем игровую клавиатуру с кнопками
klaviatura: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
                                    keyboard=[[button_name, button_description],
                                              [button_data, button_photo],
                                              [button_count_pobeditel],
                                              [button_complete]],
                                    resize_keyboard=True)

klaviatura_yes_no: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
                                                keyboard=[[button_yes, button_back]],
                                                        resize_keyboard=True)

klaviatura_data: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
                                        keyboard=[[button_data_beginning, button_data_ending],
                                        [button_back]],
                                        resize_keyboard=True)


klaviatura_send_konkurs: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
                                                    keyboard=[[button_send],
                                                              [button_back]],
                                                        resize_keyboard=True)


keyboard_konkurs_False: InlineKeyboardMarkup = InlineKeyboardMarkup(
                                            inline_keyboard=[[button_konkurs_False]])
keyboard_konkurs_True: InlineKeyboardMarkup = InlineKeyboardMarkup(
                                            inline_keyboard=[[button_konkurs_True]])

async def button_ex(text: str) -> InlineKeyboardMarkup:
 #   markup = InlineKeyboardMarkup(inline_keyboard=[])
    button = InlineKeyboardButton(text=text, callback_data="button_konkurs_False")
    markup = InlineKeyboardMarkup(inline_keyboard=[[button]])
#   button = InlineKeyboardButton(text=text, callback_data="update_button")
#    markup.inline_keyboard.append([button])
    return markup
