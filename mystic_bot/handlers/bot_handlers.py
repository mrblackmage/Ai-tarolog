from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from services.ai_service import AIService

router = Router()
ai_service = AIService()

# Машина состояний для раскладов
class TarotState(StatesGroup):
    waiting_for_question = State()
    waiting_for_spread_type = State()

class AstrologyState(StatesGroup):
    waiting_for_birth_date = State()
    waiting_for_birth_time = State()
    waiting_for_birth_place = State()
    waiting_for_question = State()

class RuneState(StatesGroup):
    waiting_for_question = State()
    waiting_for_spread_type = State()


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    """Команда /start - приветствие"""
    await message.answer(
        "🔮 Добро пожаловать в мистический бот!\n\n"
        "Я ваш персональный таролог, астролог и рунолог.\n\n"
        "📜 Доступные команды:\n"
        "/tarot - Расклад Таро\n"
        "/astrology - Астрологическая консультация\n"
        "/runes - Рунический расклад\n"
        "/help - Помощь\n\n"
        "Задайте свой вопрос или выберите команду!"
    )


@router.message(Command("help"))
async def cmd_help(message: types.Message):
    """Команда /help - справка"""
    await message.answer(
        "📖 Справка по использованию бота:\n\n"
        "🎴 **Таро** (/tarot):\n"
        "- Задайте вопрос\n"
        "- Выберите тип расклада (одна карта, три карты, кельтский крест)\n\n"
        "⭐ **Астрология** (/astrology):\n"
        "- Введите дату рождения\n"
        "- Введите время рождения\n"
        "- Введите место рождения\n"
        "- Задайте вопрос\n\n"
        "ᚠ **Руны** (/runes):\n"
        "- Задайте вопрос\n"
        "- Выберите тип расклада (одна руна, три руны, расклад Одина)\n\n"
        "💡 Советы:\n"
        "- Формулируйте вопросы четко\n"
        "- Настройтесь на серьезный лад\n"
        "- Помните: карты показывают тенденции, а не приговор"
    )


# ========== ТАРО ==========

@router.message(Command("tarot"))
async def cmd_tarot(message: types.Message, state: FSMContext):
    """Начало сеанса Таро"""
    await state.set_state(TarotState.waiting_for_question)
    await message.answer(
        "🎴 **Расклад Таро**\n\n"
        "Задайте свой вопрос картам.\n"
        "Это может быть вопрос о любви, карьере, финансах или любой другой.\n\n"
        "Напишите ваш вопрос:"
    )


@router.message(TarotState.waiting_for_question)
async def process_tarot_question(message: types.Message, state: FSMContext):
    """Обработка вопроса для Таро"""
    await state.update_data(question=message.text)
    await state.set_state(TarotState.waiting_for_spread_type)
    
    await message.answer(
        "Выберите тип расклада:\n\n"
        "1️⃣ - Одна карта (быстрый ответ)\n"
        "3️⃣ - Три карты (прошлое/настоящее/будущее)\n"
        "🔟 - Кельтский крест (полный анализ ситуации)\n\n"
        "Напишите цифру или название расклада:"
    )


@router.message(TarotState.waiting_for_spread_type)
async def process_tarot_spread(message: types.Message, state: FSMContext):
    """Обработка типа расклада Таро"""
    data = await state.get_data()
    question = data.get("question")
    
    spread_map = {
        "1": "single",
        "одна карта": "single",
        "3": "three",
        "три карты": "three",
        "🔟": "celtic_cross",
        "кельтский крест": "celtic_cross"
    }
    
    spread_type = spread_map.get(message.text.lower(), "single")
    
    await message.answer("🔮 Карты Таро анализируют вашу ситуацию...")
    
    try:
        reading = ai_service.get_tarot_reading(question, spread_type)
        await message.answer(f"🎴 **Ваш расклад:**\n\n{reading}")
    except Exception as e:
        await message.answer(f"Произошла ошибка при получении расклада: {str(e)}")
    
    await state.clear()


# ========== АСТРОЛОГИЯ ==========

@router.message(Command("astrology"))
async def cmd_astrology(message: types.Message, state: FSMContext):
    """Начало астрологической консультации"""
    await state.set_state(AstrologyState.waiting_for_birth_date)
    await message.answer(
        "⭐ **Астрологическая консультация**\n\n"
        "Для составления натальной карты мне нужна информация о вашем рождении.\n\n"
        "Введите дату рождения в формате ДД.ММ.ГГГГ (например, 15.05.1990):"
    )


@router.message(AstrologyState.waiting_for_birth_date)
async def process_birth_date(message: types.Message, state: FSMContext):
    """Обработка даты рождения"""
    await state.update_data(birth_date=message.text)
    await state.set_state(AstrologyState.waiting_for_birth_time)
    await message.answer(
        "Введите время рождения в формате ЧЧ:ММ (например, 14:30).\n"
        "Если время неизвестно, напишите 'не знаю':"
    )


@router.message(AstrologyState.waiting_for_birth_time)
async def process_birth_time(message: types.Message, state: FSMContext):
    """Обработка времени рождения"""
    await state.update_data(birth_time=message.text)
    await state.set_state(AstrologyState.waiting_for_birth_place)
    await message.answer(
        "Введите место рождения (город, страна):\n"
        "Например: Москва, Россия"
    )


@router.message(AstrologyState.waiting_for_birth_place)
async def process_birth_place(message: types.Message, state: FSMContext):
    """Обработка места рождения"""
    await state.update_data(birth_place=message.text)
    await state.set_state(AstrologyState.waiting_for_question)
    await message.answer(
        "Теперь задайте ваш вопрос астрологу:\n"
        "Это может быть вопрос о совместимости, карьере, финансовом прогнозе и т.д."
    )


@router.message(AstrologyState.waiting_for_question)
async def process_astrology_question(message: types.Message, state: FSMContext):
    """Обработка вопроса для астролога"""
    data = await state.get_data()
    
    await message.answer("⭐ Астрологи изучают вашу натальную карту...")
    
    try:
        reading = ai_service.get_astrology_reading(
            birth_date=data.get("birth_date"),
            birth_time=data.get("birth_time"),
            birth_place=data.get("birth_place"),
            question=message.text
        )
        await message.answer(f"⭐ **Ваш астрологический прогноз:**\n\n{reading}")
    except Exception as e:
        await message.answer(f"Произошла ошибка при получении прогноза: {str(e)}")
    
    await state.clear()


# ========== РУНЫ ==========

@router.message(Command("runes"))
async def cmd_runes(message: types.Message, state: FSMContext):
    """Начало рунического расклада"""
    await state.set_state(RuneState.waiting_for_question)
    await message.answer(
        "ᚠ **Рунический расклад**\n\n"
        "Древние руны готовы дать вам совет.\n"
        "Задайте свой вопрос:"
    )


@router.message(RuneState.waiting_for_question)
async def process_rune_question(message: types.Message, state: FSMContext):
    """Обработка вопроса для рун"""
    await state.update_data(question=message.text)
    await state.set_state(RuneState.waiting_for_spread_type)
    
    await message.answer(
        "Выберите тип рунического расклада:\n\n"
        "1️⃣ - Одна руна (совет дня/быстрый ответ)\n"
        "3️⃣ - Три руны (ситуация/препятствие/совет)\n"
        "ᛟ - Расклад Одина (глубокий анализ)\n\n"
        "Напишите цифру или название расклада:"
    )


@router.message(RuneState.waiting_for_spread_type)
async def process_rune_spread(message: types.Message, state: FSMContext):
    """Обработка типа рунического расклада"""
    data = await state.get_data()
    question = data.get("question")
    
    spread_map = {
        "1": "single",
        "одна руна": "single",
        "3": "three_runes",
        "три руны": "three_runes",
        "ᛟ": "odin",
        "расклад одина": "odin"
    }
    
    spread_type = spread_map.get(message.text.lower(), "single")
    
    await message.answer("ᚠ Руны вибрируют, открывая тайны...")
    
    try:
        reading = ai_service.get_rune_reading(question, spread_type)
        await message.answer(f"ᚠ **Ваш рунический расклад:**\n\n{reading}")
    except Exception as e:
        await message.answer(f"Произошла ошибка при получении расклада: {str(e)}")
    
    await state.clear()


# ========== ОБРАБОТКА ОБЫЧНЫХ СООБЩЕНИЙ ==========

@router.message()
async def handle_message(message: types.Message):
    """Обработка обычных сообщений как общая консультация"""
    try:
        response = ai_service.get_general_consultation(message.text)
        await message.answer(response)
    except Exception as e:
        await message.answer(
            "Произошла ошибка при обработке вашего запроса.\n"
            "Попробуйте использовать команды /tarot, /astrology или /runes для конкретного расклада."
        )
