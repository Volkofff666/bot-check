import asyncio
from aiogram import Bot, Dispatcher
from handlers import router
from database import create_db

TOKEN = "8131287723:AAEQ89w2ou1B-OLj0rQc8vGWTRaPqjQ4I1E"

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(router)

    await create_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
