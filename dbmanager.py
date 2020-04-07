import sqlite3
from models import Question

"""
1. Подключение к БД (создание БД)
2. Создать таблицу
3. Запись
4. Получение данных
5. Удаление данных
6. Изменение данных
"""

class DBManager:
    def __init__(self, db_path):
        self.con = sqlite3.connect(db_path)
        self.create_question_table()

    def create_question_table(self):
        query = 'CREATE TABLE "Question"(\
            "id" INTEGER PRIMARY KEY AUTOINCREMENT,\
            "text" TEXT,\
            "answers" TEXT,\
            "correct_answer" TEXT\
        );'
        try:
            self.con.execute(query)
        except sqlite3.OperationalError:
            print('Таблица уже создана')

    def insert_question(self, question):
        answers = ';'.join(question.answers)
        query = 'INSERT INTO Question (text, answers, correct_answer) VALUES (?, ?, ?)'
        self.con.execute(query, [question.text, answers, question.correct_answer])
        self.con.commit()

    def create_question_from_row(self, row):
        return Question(
                id=row[0],
                text=row[1],
                answers=row[2].split(';'),
                correct_answer=row[3]
            )

    def select_question(self, id):
        query = f'SELECT * FROM Question WHERE id == {id};'
        cursor = self.con.execute(query)
        rows = cursor.fetchall()
        if rows:
            return self.create_question_from_row(rows[0])
        return None

    def select_questions(self):
        query = f'SELECT * FROM Question;'
        cursor = self.con.execute(query)
        result = []
        for row in cursor:
            result.append(self.create_question_from_row(row))
        return result

    def delete_question(self, id):
        query = f'DELETE FROM Question WHERE id == {id}'
        self.con.execute(query)
        self.con.commit()

    def update_question(self, question):
        query = f'UPDATE Question ' \
                f'SET ' \
                f'  text = "{question.text}", ' \
                f'  answers = "{";".join(question.answers)}", ' \
                f'  correct_answer="{question.correct_answer}" ' \
                f'WHERE id == {question.id}'
        self.con.execute(query)
        self.con.commit()

    def __del__(self):
        self.con.close()

if __name__ == '__main__':
    manager = DBManager('questions.db')
    # q1 = Question('Сколько будет 5 + 7?', ['43', '23', '12', '21'], 12)
    # manager.insert_question(q1)
    question = manager.select_question(3)
    question.text = 'How much will be 5+7?'
    question.correct_answer = '22'
    manager.update_question(question)


