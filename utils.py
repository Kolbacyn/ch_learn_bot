# from dataclass import Answer, Question
# from scrapy_hsk.models import Word

# from 

# def generate_question():
#     words = [get_word_from_database() for i in range(4)]
#     hanzi = words[0].word
#     text = f'Переведите на русский язык: {hanzi}'
#     translation = words[0].rus_translation
#     ans_one = words[1]
#     ans_two = words[2]
#     ans_three = words[3]
#     question = Question(
#         text=text,
#         answers=[
#             Answer(translation, is_correct=True),
#             Answer(ans_one.rus_translation),
#             Answer(ans_two.rus_translation),
#             Answer(ans_three.rus_translation)
#         ],
#         resize_keyboard=True
#     )
#     return question
