from aiogram.fsm.state import StatesGroup, State

class ReceiptStates(StatesGroup):
    waiting_for_photo = State()
    waiting_for_amount = State()
    waiting_for_comment = State()
    waiting_for_company = State()
    confirm = State()
