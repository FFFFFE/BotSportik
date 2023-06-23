LEXICON_RU: dict[str, dict[str, str]] = {
    'MENU': {
        '/start': '<b>Привет! Я бот спортик</b>🤖\n'
                  'Помогу тебе выработать привычку к спорту 🦾\n'
                  'Не раз хотел начать заниматься, но бросал или даже не начинал?\n'
                  'Всё потому, что главное это привычка',
        'start_continuous': 'Это легче, чем можно подумать!\n'
                            'Мы будем заниматься совсем по чуть-чуть, но <u>регулярно</u>\n\n'
                            '<b>Выбери упражнение, которое сделает тебя сильнее:</b>',
        'other_answer': 'Извини, увы, это сообщение мне непонятно...'},

    'MAIN_MENU': {'train': 'choice_train',
                  'redact': 'choice_redact',
                  'progress': 'redact_progress',
                  'menu_intro': 'Привет, боец\nКуда пойдём?',
                  'choice_train': 'Тренироваться',
                  'choice_redact': 'Редактировать упражнения',
                  'redact_progress': 'Прогресс занятий',
                  'choice_return': 'Вернуться в главное меню',
                  'choice_train_done': 'Упражнение выполнил',
                  'choice_redact_menu': 'Редактировать'},
    'REDACT': {
        'choice_new_exercise': 'Добавить новое упражнение',
    },

    'MESSAGES': {
        'msg_wrong_repeats': 'Выбрано недопустимое количество повторений',
        'msg_train_complete': 'Ты всё сделал, красава',
        'msg_redact_state': 'Ты в меню редактирования упражнений',
        'msg_train_state': 'Ты в режиме тренировки\nТвоя программа:\n',
        'msg_progress_state': 'Ты в меню прогресса занятий\n'
    },

    'EXERCISES': {
        'pushups': 'Отжимания',
        'situps': 'Приседания',
        # 'press': 'Пресс',
        # 'another_exercise': 'Свой вариант',
        'pushups_error': 'В вашей тренировке уже есть отжимания. Выбери другое упражнение',
        'situps_error': 'В вашей тренировке уже есть приседания. Выбери другое упражнение',
        'press_error': 'В вашей тренировке уже есть пресс. Выбери другое упражнение',
        # 'other_answer': 'Извини, увы, это сообщение мне непонятно...',
        'choice_pushups': 'Ты выбрал отжимания',
        'choice_situps': 'Ты выбрал приседания',
        # 'choice_press': 'Ты выбрал пресс',
        # 'choice_another': 'Ты выбрал свой вариант упражнений',
        'repeats_choice': 'Выбери комфортное для тебя число повторений\n\n'
                          '<b>Сколько повторений ты точно сможешь сделать и не свалиться без сил?</b>'
    },

    'REPEATS': {
        'exercise_cnt_5': '5 Повторений',
        'exercise_cnt_10': '10 Повторений',
        # 'exercise_cnt_15': '15 Повторений',
        # 'exercise_cnt_20': '20 Повторений',
        # 'exercise_cnt_30': '30 Повторений',
        # 'exercise_ctn_another': 'Задать самому',
        'choice_cnt_5': 'Ты выбрал 5 повторений',
        'choice_cnt_10': 'Ты выбрал 10 повторений',
        # 'choice_cnt_15': 'Ты выбрал 15 повторений',
        # 'choice_cnt_20': 'Ты выбрал 20 повторений',
        # 'choice_cnt_30': 'Ты выбрал 30 повторений',
        # 'choice_cnt_another': 'Ты выбрал неведомое число повторений',
        'repeat_5': 5,
        'repeat_10': 10
    }
}
