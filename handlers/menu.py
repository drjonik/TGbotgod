from aiogram import Router, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils.lang import _

router = Router()

def get_main_menu(user_lang: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton(text=_('View Tasks', user_lang), callback_data='view'),
        InlineKeyboardButton(text=_('Add Task', user_lang), callback_data='add'),
    )
    kb.add(
        InlineKeyboardButton(text=_('Settings', user_lang), callback_data='settings'),
    )
    return kb

@router.message(commands=['start', 'menu'])
async def start_menu(message: types.Message):
    user_lang = I18n.get_user_lang(message.from_user.id)
    text = _('Welcome! I am your personal secretary.', user_lang)
    await message.answer(text, reply_markup=get_main_menu(user_lang))

def register(dp):
    dp.include_router(router)
