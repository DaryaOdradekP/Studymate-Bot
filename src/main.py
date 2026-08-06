import asyncio

from src.bot import bot, dp

from src.database.init_db import init_db

async def main():
    print("Bot is starting...")
    init_db()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
