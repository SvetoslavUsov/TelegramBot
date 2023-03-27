from aiogram import Bot
from aiogram.types import BotCommand

from lexicon.lexicon import LEXICON_COMMAND1


# Функция для настройки кнопки Menu бота

async def set_main_menu(bot: Bot):
    main_menu_commands = [BotCommand(
                                command=command,
                                description=description
                          ) for command,
                                description in LEXICON_COMMAND1.items()]
    await bot.set_my_commands(main_menu_commands)