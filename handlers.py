from aiogram import Router, F, types
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from states import ReceiptStates
from keyboards import start_kb, skip_back_kb, company_kb, confirm_kb
from database import save_receipt, export_to_excel

router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer("Добро пожаловать!", reply_markup=start_kb())

@router.callback_query(F.data == "add_receipt")
async def add_receipt(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ReceiptStates.waiting_for_photo)
    await callback.message.answer("Отправьте фото или PDF чека:")

@router.message(ReceiptStates.waiting_for_photo, F.content_type.in_({"photo", "document"}))
async def process_photo(message: types.Message, state: FSMContext):
    file_id = message.photo[-1].file_id if message.photo else message.document.file_id
    await state.update_data(photo_id=file_id)
    await state.set_state(ReceiptStates.waiting_for_amount)
    await message.answer("Введите сумму в евро:", reply_markup=skip_back_kb())

@router.message(ReceiptStates.waiting_for_amount)
async def process_amount(message: types.Message, state: FSMContext):
    if not message.text.replace(",", ".").replace(".", "").isdigit():
        await message.answer("Пожалуйста, введите корректное число.")
        return
    await state.update_data(amount=message.text.replace(",", "."))
    await state.set_state(ReceiptStates.waiting_for_comment)
    await message.answer("Введите комментарий (или нажмите пропустить):", reply_markup=skip_back_kb())

@router.message(ReceiptStates.waiting_for_comment)
async def process_comment(message: types.Message, state: FSMContext):
    await state.update_data(comment=message.text)
    await state.set_state(ReceiptStates.waiting_for_company)
    await message.answer("Выберите фирму:", reply_markup=company_kb())

@router.callback_query(ReceiptStates.waiting_for_comment, F.data == "skip")
async def skip_comment(callback: CallbackQuery, state: FSMContext):
    await state.update_data(comment="-")
    await state.set_state(ReceiptStates.waiting_for_company)
    await callback.message.answer("Выберите фирму:", reply_markup=company_kb())

@router.callback_query(ReceiptStates.waiting_for_company)
async def select_company(callback: CallbackQuery, state: FSMContext):
    await state.update_data(company=callback.data)
    data = await state.get_data()

    await callback.message.answer_photo(
        photo=data['photo_id'],
        caption=f"Сумма: {data['amount']} €\nКомментарий: {data['comment']}\nКомпания: {data['company']}",
        reply_markup=confirm_kb()
    )
    await state.set_state(ReceiptStates.confirm)

@router.callback_query(ReceiptStates.confirm, F.data == "confirm")
async def confirm_receipt(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    save_receipt(
        user_id=callback.from_user.id,
        photo_id=data['photo_id'],
        amount=data['amount'],
        comment=data['comment'],
        company=data['company']
    )
    await callback.message.answer("✅ Чек сохранён!", reply_markup=start_kb())
    await state.clear()

@router.callback_query(ReceiptStates.confirm, F.data == "cancel")
async def cancel_receipt(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("❌ Отменено.", reply_markup=start_kb())
    await state.clear()

@router.callback_query(F.data == "export_all")
async def export_all(callback: CallbackQuery):
    path = export_to_excel()
    await callback.message.answer_document(types.FSInputFile(path))
