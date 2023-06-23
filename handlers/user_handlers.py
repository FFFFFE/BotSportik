from copy import deepcopy
from aiogram import Router
from aiogram.filters import Command, CommandStart, StateFilter, Text
from database.database import user_dict_template, users_db
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from keyboards.keyboards import exercise_kb, repeats_kb, main_kb, train_kb_before, train_kb_after, redact_kb, progress_kb
from lexicon.lexicon_ru import LEXICON_RU
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.state import default_state
from datetime import datetime
import time

router: Router = Router()
storage: MemoryStorage = MemoryStorage()


# Cоздаем класс, наследуемый от StatesGroup, для группы состояний нашей FSM
class FSMProgramChoice(StatesGroup):
    # Создаем экземпляры класса State, последовательно перечисляя возможные состояния,
    # в которых будет находиться бот в разные моменты взаимодействия с пользователем
    exercise_choice_state = State()       # Состояние ожидания выбора упражнения
    repeat_choice_state = State()         # Состояние ожидания выбора повторений
    menu_state = State()                  # Состояние главного меню
    train_state = State()                 # Состояние тренировки
    redact_state = State()                # Состояние редактирования упражнений
    progress_state = State()              # Состояние просмотра прогресса занятий


# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message, state: FSMProgramChoice):
    await message.answer(text=LEXICON_RU['MENU']['/start'])

    # Если пользователя ещё не было в БД, то добавляет его туда
    if message.from_user.id not in users_db:
        users_db[message.from_user.id] = deepcopy(user_dict_template)
        time.sleep(2)

    await message.answer(text=LEXICON_RU['MENU']['start_continuous'], reply_markup=exercise_kb)

    # Устанавливаем состояние ожидания выбора упражнения
    await state.set_state(FSMProgramChoice.exercise_choice_state)


# Этот хэндлер срабатывает на выбор отжиманий
@router.callback_query(StateFilter(FSMProgramChoice.exercise_choice_state), Text(text=['pushups_btn_pressed']))
async def process_pushups(callback: CallbackQuery, state: FSMProgramChoice):
    if 'pushups' not in users_db[callback.from_user.id]['exercises']:
        # await callback.message.answer(text=LEXICON_RU['EXERCISES']['choice_pushups'])
        await callback.answer(text=LEXICON_RU['EXERCISES']['choice_pushups'])
        users_db[callback.from_user.id]['exercises']['pushups'] = -1
        time.sleep(1)
        await callback.message.edit_text(text=LEXICON_RU['EXERCISES']['repeats_choice'], reply_markup=repeats_kb)

        # Сохраняем информацию о выбранном упражнении в контексте state
        await state.update_data(chosen_exercise='pushups')

        # Устанавливаем состояние ожидания выбора повторений
        await state.set_state(FSMProgramChoice.repeat_choice_state)
    else:
        await callback.answer(text=LEXICON_RU['EXERCISES']['pushups_error'])


# Этот хэндлер срабатывает на выбор приседаний
@router.callback_query(StateFilter(FSMProgramChoice.exercise_choice_state), Text(text=['situps_btn_pressed']))
async def process_pushups(callback: CallbackQuery, state: FSMProgramChoice):
    if 'situps' not in users_db[callback.from_user.id]['exercises']:
        # await callback.message.answer(text=LEXICON_RU['EXERCISES']['choice_pushups'])
        await callback.answer(text=LEXICON_RU['EXERCISES']['choice_situps'])
        users_db[callback.from_user.id]['exercises']['situps'] = -1
        time.sleep(1)
        await callback.message.edit_text(text=LEXICON_RU['EXERCISES']['repeats_choice'], reply_markup=repeats_kb)

        # Сохраняем информацию о выбранном упражнении в контексте state
        await state.update_data(chosen_exercise='situps')

        # Устанавливаем состояние ожидания выбора повторений
        await state.set_state(FSMProgramChoice.repeat_choice_state)
    else:
        await callback.answer(text=LEXICON_RU['EXERCISES']['situps_error'])


# Общий хэндлер для выбора количества повторений
@router.callback_query(StateFilter(FSMProgramChoice.repeat_choice_state),
                       lambda c: c.data and c.data.startswith('repeat_'))
async def repeats_choice(callback: CallbackQuery, state: FSMProgramChoice):
    # Извлекаем количество повторений из словаря
    count = LEXICON_RU['REPEATS'][callback.data]

    if count is None:
        # Если текст сообщения не найден в словаре, значит, пользователь ввел что-то неправильное.
        # Можно отправить сообщение с ошибкой и выйти из обработчика.
        await callback.message.answer(LEXICON_RU['MESSAGES']['msg_wrong_repeats'])
        return

    await callback.answer(text=LEXICON_RU['REPEATS'][f'choice_cnt_{count}'])
    time.sleep(1)

    # В ответ на выбор числа повторений отправляем текст и клаву
    await callback.message.edit_text(text=LEXICON_RU['MAIN_MENU']['menu_intro'], reply_markup=main_kb)

    # Извлекаем информацию из контекста state
    user_data = await state.get_data()
    chosen_exercise = user_data.get('chosen_exercise')
    await state.update_data(chosen_exercise=None)

    # Устанавливаем количество упражнений
    users_db[callback.from_user.id]['exercises'][chosen_exercise] = count

    # Устанавливаем состояние главного меню
    await state.set_state(FSMProgramChoice.menu_state)

    # Подтверждаем обработку callback query
    await callback.answer()


# Хэндлер, срабатывающий на нажатие кнопки "Тренироваться" в главном меню
@router.callback_query(StateFilter(FSMProgramChoice.menu_state), Text(text=['choice_train_pressed']))
async def train_button_press(callback: CallbackQuery, state: FSMProgramChoice):
    user_id = callback.from_user.id
    curr_date = datetime.today().strftime('%Y-%m-%d')  # Дату в будущем использовать как у пользователя а не мою локальную
    exercises_string: str = "\n".join(map(str, users_db[user_id]['exercises'].items()))

    # Если текущей даты нет в истории, то сегодня тренировки не было
    if curr_date not in users_db[user_id]['train_history']:
        await callback.message.edit_text(text=LEXICON_RU['MESSAGES']['msg_train_state'] + exercises_string,
                                         reply_markup=train_kb_before)
    else:
        await callback.message.edit_text(text=LEXICON_RU['MESSAGES']['msg_train_complete'], reply_markup=train_kb_after)

    # Устанавливаем состояние тренировки
    await state.set_state(FSMProgramChoice.train_state)


# Хэндлер срабатывающий на нажатие кнопки "Упражнение выполнил"
@router.callback_query(StateFilter(FSMProgramChoice.train_state), Text(text=['train_done_pressed']))
async def train_done_button_press(callback: CallbackQuery):
    user_id = callback.from_user.id
    curr_date = datetime.today().strftime('%Y-%m-%d')  # Дату в будущем использовать как у пользователя а не мою локальную
    exercises_string: str = "\n".join(map(str, users_db[user_id]['exercises'].items()))

    await callback.message.edit_text(text=LEXICON_RU['MESSAGES']['msg_train_complete'], reply_markup=train_kb_after)

    # Если текущей даты нет в истории, то сегодня тренировки не было. Сохраним её
    if curr_date not in users_db[user_id]['train_history']:
        # Здесь в дальнейшем переписать код и присваивать ключу curr_date так, чтобы различать сделанное от несделанного
        users_db[user_id]['train_history'][curr_date] = exercises_string


# Хэндлер, срабатывающий на нажатие кнопки "Редактировать упражнения" в главном меню
@router.callback_query(StateFilter(FSMProgramChoice.menu_state), Text(text=['choice_redact_pressed']))
async def redact_button_press(callback: CallbackQuery, state: FSMProgramChoice):
    if callback.message.text != LEXICON_RU['MESSAGES']['msg_redact_state']:
        await callback.message.edit_text(text=LEXICON_RU['MESSAGES']['msg_redact_state'], reply_markup=redact_kb)

        # Устанавливаем состояние тренировки
        await state.set_state(FSMProgramChoice.redact_state)


# Хэндлер, срабатывающий на нажатие кнопки "Добавить новое упражнение" в разделе "Редактировать упражнения"
@router.callback_query(StateFilter(FSMProgramChoice.redact_state), Text(text=['redact_new_exercise_pressed']))
async def redact_button_press(callback: CallbackQuery, state: FSMProgramChoice):
    await callback.message.edit_text(text=LEXICON_RU['MENU']['start_continuous'], reply_markup=exercise_kb)

    # Устанавливаем состояние ожидания выбора упражнения
    await state.set_state(FSMProgramChoice.exercise_choice_state)


# Хэндлер, срабатывающий на нажатие кнопки "Прогресс занятий" в главном меню
@router.callback_query(StateFilter(FSMProgramChoice.menu_state), Text(text=['choice_progress_pressed']))
async def process_button_press(callback: CallbackQuery, state: FSMProgramChoice):
    user_id = callback.from_user.id
    history = users_db[user_id]['train_history']
    if callback.message.text != LEXICON_RU['MESSAGES']['msg_progress_state'] + str(history):
        await callback.message.edit_text(text=LEXICON_RU['MESSAGES']['msg_progress_state'] + str(history),
                                         reply_markup=progress_kb)

        # Устанавливаем состояние тренировки
        await state.set_state(FSMProgramChoice.progress_state)


# Хэндлер, срабатывающий на нажатие кнопки "Вернуться в главное меню"
# В режиме "тренироваться" либо в режиме "редактировать упражнения" либо в разделе "прогресс занятий"
@router.callback_query(StateFilter(FSMProgramChoice.redact_state), Text(text=['redact_return_pressed']))
@router.callback_query(StateFilter(FSMProgramChoice.train_state), Text(text=['train_return_pressed']))
@router.callback_query(StateFilter(FSMProgramChoice.progress_state), Text(text=['progress_return_pressed']))
async def process_buttons_press(callback: CallbackQuery, state: FSMProgramChoice):
    if callback.message.text != LEXICON_RU['MAIN_MENU']['menu_intro']:
        await callback.message.edit_text(text=LEXICON_RU['MAIN_MENU']['menu_intro'], reply_markup=main_kb)

        # Устанавливаем состояние тренировки
        await state.set_state(FSMProgramChoice.menu_state)