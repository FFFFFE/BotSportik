from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

from lexicon.lexicon_ru import LEXICON_RU

# # Создаем кнопки для выбора упражнения
# btn_pushups: KeyboardButton = KeyboardButton(text=LEXICON_RU['EXERCISES']['pushups'])
# btn_situps: KeyboardButton = KeyboardButton(text=LEXICON_RU['EXERCISES']['situps'])
#
# # Создаем игровую клавиатуру для выбора упражнения
# exercise_kb: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[btn_pushups, btn_situps]],
#                                                        resize_keyboard=True)

# Создаем кнопки для выбора упражнения
btn_pushups: InlineKeyboardButton = InlineKeyboardButton(text=LEXICON_RU['EXERCISES']['pushups'],
                                                         callback_data='pushups_btn_pressed')
btn_situps: InlineKeyboardButton = InlineKeyboardButton(text=LEXICON_RU['EXERCISES']['situps'],
                                                        callback_data='situps_btn_pressed')
# Создаем игровую клавиатуру для выбора упражнения
exercise_kb: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[[btn_pushups, btn_situps]],
                                                         resize_keyboard=True)


# Создаем кнопки для выбора количества повторений
btn_cnt_5: InlineKeyboardButton = InlineKeyboardButton(text=LEXICON_RU['REPEATS']['exercise_cnt_5'],
                                                       callback_data='repeat_5')
btn_cnt_10: InlineKeyboardButton = InlineKeyboardButton(text=LEXICON_RU['REPEATS']['exercise_cnt_10'],
                                                        callback_data='repeat_10')
# Создаем клавиатуру для выбора количества повторений
repeats_kb: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[[btn_cnt_5, btn_cnt_10]], resize_keyboard=True)


# Создаем инлайн кнопки для главного меню
btn_train: InlineKeyboardButton = InlineKeyboardButton(text=LEXICON_RU['MAIN_MENU']['choice_train'],
                                                       callback_data='choice_train_pressed')
btn_redact: InlineKeyboardButton = InlineKeyboardButton(text=LEXICON_RU['MAIN_MENU']['choice_redact'],
                                                        callback_data='choice_redact_pressed')
btn_progress: InlineKeyboardButton = InlineKeyboardButton(text=LEXICON_RU['MAIN_MENU']['redact_progress'],
                                                          callback_data='choice_progress_pressed')

# Создаем игровую клавиатуру для выбора количества повторений
main_kb: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[[btn_train], [btn_redact], [btn_progress]],
                                                     resize_keyboard=True)
# Создаем кнопки тренировки
bnt_return: InlineKeyboardButton = InlineKeyboardButton(text=LEXICON_RU['MAIN_MENU']['choice_return'],
                                                        callback_data='train_return_pressed')
bnt_train_done: InlineKeyboardButton = InlineKeyboardButton(text=LEXICON_RU['MAIN_MENU']['choice_train_done'],
                                                            callback_data='train_done_pressed')
# Создаём клавиатуру тренировки
train_kb_before: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[[bnt_train_done], [bnt_return]],
                                                             resize_keyboard=True)

train_kb_after: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[[bnt_return]],
                                                            resize_keyboard=True)

# Создаем кнопки редактирования упражнений
btn_redact_menu: InlineKeyboardButton = InlineKeyboardButton(text=LEXICON_RU['MAIN_MENU']['choice_return'],
                                                             callback_data='redact_return_pressed')
btn_new_exercise: InlineKeyboardButton = InlineKeyboardButton(text=LEXICON_RU['REDACT']['choice_new_exercise'],
                                                              callback_data='redact_new_exercise_pressed')

# Создаём клавиатуру редактирования упражнений
redact_kb: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[[btn_new_exercise], [btn_redact_menu]],
                                                       resize_keyboard=True)

# Создаем кнопки прогресса занятий
btn_progress_menu: InlineKeyboardButton = InlineKeyboardButton(text=LEXICON_RU['MAIN_MENU']['choice_return'],
                                                               callback_data='progress_return_pressed')
# Создаём клавиатуру редактирования упражнений
progress_kb: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[[btn_progress_menu]], resize_keyboard=True)
