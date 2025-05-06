from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def start_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Добавить чек", callback_data="add_receipt")],
        [InlineKeyboardButton(text="📥 Экспорт Всего", callback_data="export_all")],
    ])

def skip_back_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅ Назад", callback_data="back"),
         InlineKeyboardButton(text="Пропустить ➡", callback_data="skip")],
    ])

def company_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="EDT Services", callback_data="EDT Services")],
        [InlineKeyboardButton(text="EDT Pharma", callback_data="EDT Pharma")],
        [InlineKeyboardButton(text="EDT Immo 1", callback_data="EDT Immo 1")],
        [InlineKeyboardButton(text="EDT Immobilien", callback_data="EDT Immobilien")],
        [InlineKeyboardButton(text="Свободно", callback_data="Свободно")],
        [InlineKeyboardButton(text="⬅ Назад", callback_data="back")],
    ])

def confirm_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm"),
         InlineKeyboardButton(text="❌ Отменить", callback_data="cancel")],
        [InlineKeyboardButton(text="⬅ Назад", callback_data="back")],
    ])
