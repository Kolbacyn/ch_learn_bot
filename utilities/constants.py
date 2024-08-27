from enum import Enum


class Button(str, Enum):
    """Buttons"""
    HSK_1_BUTTON = 'hsk_buttons_1'
    ACCEPT = '✅ Подтвердить'
    CANCEL = '🔙 Назад'
    EXIT = '🚫 Выход'
    GO_TO_MENU = '🏠 В меню'
    REPEAT = '🔁 Повторить'
    CORRECT = '✅'
    WRONG = '❌'


class ButtonData(str, Enum):
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


class Picture(str, Enum):
    """Pictures"""
    GREETING = 'hey_pic.png'
    FLASHCARD = 'biffer.png'


class CommonMessage(str, Enum):
    """Common messages:"""
    CANCEL = 'Тренировка отменена.'
    CHOOSE_HSK_LEVEL = 'Выбери уровень подготовки'
    CHOOSE_LANGUAGE = 'Выбери язык, на котором будет удобно общаться'
    GAME_OVER = 'Игра окончена!'
    GOOD_JOB = 'Отлично! Тренировка окончена.'
    GREETING = 'Меня зовут Ханью, я твой помощник в изучении китайского'
    HELP = 'Это бот-помощник в изучении китайского языка.'
    INSTRUCTIONS = 'Чтобы начать отправьте /start.'
    INTRODUCING = 'Для начала давай определимся с некоторыми моментами!'
    STARTING = 'Отлично! Чтобы начать, выберите из списка:'
    STARTOVER = 'Начнем сначала!'
    WELCOME = 'Добро пожаловать в игру!'
    NIHAO = '你好'


class ConstructMessage(str, Enum):
    """Construct messages"""
    CORRECT = 'Все верно!'
    INCORRECT = 'Неверно!\nПравильное предложение: '
    FINAL_ANSWER = 'Ваше предложение: '
    INTERIM_ANSWER = 'Вы выбрали: '
    INITIAL = 'Составьте предложение из следующих слов: '
    RETURN_TO_MENU = 'Возвращаемся в главное меню...'


class FlashcardMessage(str, Enum):
    """Flashcard messages"""
    INITIAL = 'Вот ваше первое слово: '
    START_FLASHCARDS = 'Приступим!'


class QuizMessage(str, Enum):
    """Quiz messages"""
    INITIAL = 'Вот ваше первое слово: '


class Rules(str, Enum):
    """Rules"""
    CONSTRUCT_RULES = '''
        Правила:
        Вам будет предложено составить предложение из нескольких слов.
        Ваша задача выбрать правильную последовательность слов,
        которая будет соответствовать граматически правильному предложению.

        Для того, чтобы выйти из тренировки нажмите кнопку "🚫 Выход".
        Для того, чтобы отменить выбор и вернуться на шаг назад
        нажмите кнопку "🔙 Назад".
        '''
    QUIZ_RULES = '''
        Правила:
        Вам будет предложено ответить на 10 вопросов.
        На каждый вопрос дается четыре варианта ответа.
        Ваша задача выбрать правильный.

        Для того, чтобы выйти из тренировки нажмите кнопку "🚫 Выход".
        Для того, чтобы вернуться к предыдущему вопросу
        нажмите кнопку "🔙 Назад".
        '''
    FLASHCARDS_RULES = '''
        Правила:
        Вам будет предложено слово на китайском языке.
        Если вы знаете перевод, то нажимайте кнопку "✅".
        Если вы не знаете перевод, то нажимайте кнопку "❌".

        Если захотите получить подсказку, то просто нажмите кнопку со словом.
        Для того, чтобы закончить тренировку нажмите кнопку "🚫 Выход".

        Отвечайте честно, ведь я знаю все правильные ответы 🤓
        '''


class Numeric(int, Enum):
    """Numbers"""
    ZERO = 0
    ONE = 1
    LAST_ELEMENT = -1
    QUIZ_SLEEP = 5
    ADJUSTMENT = 2
