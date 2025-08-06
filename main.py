import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
import os

from handlers import menu, tasks
from scheduler.scheduler import Scheduler
from db.database import init_db
from utils.lang import I18n

# Load config
env_path = os.getenv('DOTENV_PATH', None)
load_dotenv(env_path)
TOKEN = os.getenv('TOKEN')
DB_URL = os.getenv('DB_URL')
DEFAULT_LANG = os.getenv('DEFAULT_LANGUAGE', 'ru')

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    # Initialize DB
    await init_db(DB_URL)

    # Initialize bot
    bot = Bot(token=TOKEN)
    dp = Dispatcher(storage=MemoryStorage(), bot=bot)

    # Initialize i18n
    I18n.load(locales_dir='locales', default_lang=DEFAULT_LANG)

    # Register handlers
    menu.register(dp)
    tasks.register(dp)

    # Start scheduler
    sched = Scheduler(bot)
    await sched.load_jobs()

    logger.info("Bot started")
    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main())
