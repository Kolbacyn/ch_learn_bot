from enum import IntEnum, StrEnum


class Button(StrEnum):
    """Buttons"""
    HSK_1_BUTTON = 'hsk_buttons_1'
    ACCEPT = '✅ Подтвердить'
    CANCEL = '🔙 Назад'
    EXIT = '🚫 Выход'
    GO_TO_MENU = '🏠 В меню'
    REPEAT = '🔁 Повторить'
    CORRECT = '✅'
    WRONG = '❌'

    RUSSIAN = '🇷🇺 Русский'
    ENGLISH = '🇬🇧 English'
    SPANISH = '🇪🇸 Espanol'

    QUIZ = 'Викторина'
    FLASHCARDS = 'Карточки'
    CONSTRUCTOR = 'Конструктор'


class ButtonData(StrEnum):
    """Button data"""
    TRAIN_QUIZ = 'main_menu_btn_1'
    TRAIN_FLASHCARDS = 'main_menu_btn_2'
    TRAIN_CONSTRUCTOR = 'main_menu_btn_3'

    CONSTRUCT_AGAIN = 'construct_again'
    CONSTRUCT_BACK = 'construct_back'
    CONSTRUCT_CORRECT = 'construct_correct'
    CONSTRUCT_LEAVE = 'construct_leave'
    CONSTRUCT_REPEAT = 'construct_repeat'

    FLASHCARD_FRONT_SIDE = 'flashcard_front_side'
    FLASHCARD_CORRECT_ANSWER = 'flashcard_correct_answer'
    FLASHCARD_WRONG_ANSWER = 'flashcard_wrong_answer'
    FLASHCARD_LEAVE = 'flashcard_leave'

    LANGUAGE_RU = 'language_ru'
    LANGUAGE_EN = 'language_en'
    LANGUAGE_ES = 'language_es'


class Picture(StrEnum):
    """Pictures"""
    GREETING = 'pictures/hey_pic.png'
    FLASHCARD = 'pictures/biffer.png'

    FORMAT = 'PNG'
    FONT = 'Deng.ttf'
    B_COLOR = 'black'
    W_COLOR = 'white'
    ANCHOR = 'mm'
    PALLETE = 'RGB'


class CommonMessage(StrEnum):
    """Common messages:"""
    CANCEL = 'Тренировка отменена.'
    CHOOSE_HSK_LEVEL = 'Выбери уровень подготовки'
    CHOOSE_LANGUAGE = 'Выбери язык на котором тебе будет удобно общаться:'
    LANGUAGE_CHOSEN = 'Отлично! Язык выбран! Теперь выбери уровень подготовки:'
    HSK_CHOSEN = (
        'Отлично! Уровень подготовки выбран! Ты всегда можешь '
        'изменить эти настройки в личном кабинете.'
        )
    GAME_OVER = 'Игра окончена!'
    GOOD_JOB = 'Отлично! Тренировка окончена.'
    GREETING_NEW = (
        'Вижу, что ты здесь первый раз. Меня зовут Бо '
        'Ханью. Я буду помогать тебе в изучении китайского языка, '
        'узнавать новую и вспоминать забытую лексику.'
    )
    GREETING_OLD = (
        'Привет! Вижу, что ты здесь уже не впервые. Я буду помогать'
        ' тебе в изучении китайского языка, узнавать новую и вспоминать '
        'забытую лексику.'
        )
    HELP = 'Это бот-помощник в изучении китайского языка.'
    INSTRUCTIONS = 'Чтобы начать отправьте /start.'
    STARTING = 'Приступим!'
    STARTOVER = 'Начнем сначала!'
    WELCOME = 'Добро пожаловать в игру!'
    NIHAO = '你好'
    PROFILE = 'Профиль пользователя в разработке'


class ConstructMessage(StrEnum):
    """Construct messages"""
    CORRECT = 'Все верно!'
    INCORRECT = 'Неверно!\nПравильное предложение: '
    FINAL_ANSWER = 'Ваше предложение: '
    INTERIM_ANSWER = 'Вы выбрали: '
    INITIAL = 'Составьте предложение из следующих слов: '
    RETURN_TO_MENU = 'Возвращаемся в главное меню...'


class FlashcardMessage(StrEnum):
    """Flashcard messages"""
    INITIAL = 'Вот ваше первое слово: '


class QuizMessage(StrEnum):
    """Quiz messages"""
    INITIAL = 'Вот ваше первое слово: '


class Rules(StrEnum):
    """Rules"""
    CONSTRUCT_RULES = (
        'Правила:\n'
        'Тебе будет предложено  несколько слов.'
        'Твоя задача выбрать правильную последовательность слов,'
        'которая будет соответствовать граматически правильному предложению.\n'
        ''
        'Для того, чтобы выйти из тренировки нажми кнопку "🚫 Выход".'
        'Для того, чтобы отменить выбор и вернуться на шаг назад'
        'нажми кнопку "🔙 Назад".'
    )
    QUIZ_RULES = (
        'Правила:\n'
        'Тебе будет предложено ответить на 10 вопросов.'
        'На каждый вопрос дается четыре варианта ответа.'
        'Твоя задача выбрать правильный.\n'
        ' '
        'Для того, чтобы выйти из тренировки нажми кнопку "🚫 Выход".'
        'Для того, чтобы вернуться к предыдущему вопросу'
        'нажми кнопку "🔙 Назад".'
    )
    FLASHCARDS_RULES = (
        'Правила:\n'
        'Тебе будет предложено слово на китайском языке.'
        'Если знаешь перевод, то нажимай кнопку "✅".'
        'Если ты не знаешь перевод, то нажимай кнопку "❌".\n'
        ''
        'Если захочешь получить подсказку, то просто нажми кнопку со словом.'
        'Для того, чтобы закончить тренировку нажми кнопку "🚫 Выход".\n'
        ''
        'Отвечай честно, ведь я знаю все правильные ответы 🤓'
    )


class Numeric(IntEnum):
    """Numbers"""
    ZERO = 0
    ONE = 1
    TWO = 2
    FIVE = 5
    FOUR = 4
    SEVEN = 7
    LAST_ELEMENT = -1
    QUIZ_SLEEP = 5
    ADJUSTMENT = 2
    LANGUAGE = -2
    WIDTH = 300
    HEIGHT = 300
    FONT_SIZE = 62


class Database(StrEnum):
    """Database"""
    SQLITE = 'sqlite:///sqlite.db'
    ENCODING = 'utf-8'
