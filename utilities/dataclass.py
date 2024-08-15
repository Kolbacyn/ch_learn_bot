from dataclasses import dataclass, field


@dataclass
class Answer:
    """"""
    text: str
    is_correct: bool = False


@dataclass
class Question:
    """"""
    text: str
    answers: list[Answer]
    correct_answer: str = field(init=False)

    def __post_init__(self):
        self.correct_answer = next(answer.text for answer in self.answers
                                   if answer.is_correct)


@dataclass
class FlashCard:
    """"""
    front_side: str
    back_side: str
    hint: str
