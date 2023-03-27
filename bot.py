import asyncio
from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from handlers import user_handlers
from keyboards.set_menu import set_main_menu

# Загружаем конфиг в переменную config
config: Config = load_config()

super_admins = config.tg_bot.admin_ids
# Функция конфигурирования и запуска бота
async def main():


    # Инициализируем бот и диспетчер
    bot: Bot = Bot(token=config.tg_bot.token)
    dp: Dispatcher = Dispatcher()

    # Регистриуем роутеры в диспетчере
    dp.include_router(user_handlers.router)
    #dp.include_router(other_handlers.router)

    await set_main_menu(bot)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())