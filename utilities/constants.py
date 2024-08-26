from enum import Enum


class Button(str, Enum):
    """Buttons"""
    QUIZ = 'main_menu_btn_1'
    FLASHCARDS = 'main_menu_btn_2'
    CONSTRUCTOR = 'main_menu_btn_3'
    HSK_1_BUTTON = 'hsk_buttons_1'
    CANCEL = '🔙 Назад'
    EXIT = '🚫 Выход'
    CORRECT = '✅'
    WRONG = '❌'


class Picture(str, Enum):
    """Pictures:"""
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
    STARTING = 'Ну что же, приступим!'
    STARTOVER = 'Начнем сначала!'
    WELCOME = 'Добро пожаловать в игру!'


class ConstructMessage(str, Enum):
    """Construct messages"""
    INITIAL = 'Составьте предложение из следующих слов: '


class FlashcardMessage(str, Enum):
    """Flashcard messages"""
    INITIAL = 'Вот ваше первое слово: '
    START_FLASHCARDS = 'Приступим!'


class QuizMessage(str, Enum):
    """Quiz messages"""
    INITIAL = 'Вот ваше первое слово: '


class Rules(str, Enum):
    """Rules"""
    CONSTRUCT_RULES = ''''''
    QUIZ_RULES = '''
        Правила:
        Вам будет предложено ответить на 10 вопросов.
        На каждый вопрос дается четыре варианта ответа.
        Ваша задача выбрать правильный.

        Для того, чтобы выйти из тренировки нажмите кнопку "🚫 Выход".
        Для того, чтобы вернуться к предыдущему вопросу нажмите кнопку "🔙 Назад".
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
