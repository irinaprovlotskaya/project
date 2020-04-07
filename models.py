
class Question:
    def __init__(self, id=None, text='', answers='', correct_answer=''):
        self.id = id
        self.text = text
        self.answers = answers
        self.correct_answer = correct_answer

    # @property
    # def id(self):
    #     return self.__id
    #
    # @id.setter
    # def id(self, value):
    #     if type(value) == int:
    #         self.__id = value
    #     else:
    #         raise ValueError('Id should be int type')

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, value):
        if len(value) > 2:
            self.__text = value
        else:
            raise ValueError('Text should be minimum 5 chars len')

    @property
    def answers(self):
        return self.__answers

    @answers.setter
    def answers(self, value):
        self.__answers = value

    @property
    def correct_answer(self):
        return self.__correct_answer

    @correct_answer.setter
    def correct_answer(self, value):
        self.__correct_answer = value

    def __str__(self):
        return f'{self.__text} {self.__answers} {self.__correct_answer}'

    def __repr__(self):
        return f'{self.__class__}'

if __name__ == '__main__':
    q1 = Question('Сколько будет 5 + 7?', [43, 23, 12, 21], 12)
    print(q1.text)