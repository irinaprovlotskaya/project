from design import Ui_MainWindow
from PyQt5 import QtWidgets
import sys
from dbmanager import DBManager
from models import Question

class EditorGui(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.db_manager = DBManager('questions.db')
        self.questions = []
        self.load_questions()
        self.bind_button_events()
        self.selected_question = None
        self.item_index = None

    def bind_button_events(self):
        self.pushButtonAdd.clicked.connect(self.on_add_button)
        self.listWidgetQuestions.clicked.connect(self.on_list_item)
        self.pushButtonDel.clicked.connect(self.on_del_button)
        self.pushButtonSave.clicked.connect(self.on_save_button)

    def load_questions(self):
        self.questions = []
        self.listWidgetQuestions.clear()
        loaded_questions = self.db_manager.select_questions()
        for question in loaded_questions:
            self.questions.append(question)
            self.listWidgetQuestions.addItem(question.text)


    def save_question(self):
        text = self.lineEditQuestionText.text()
        answer1 = self.lineEditAnswer1.text()
        answer2 = self.lineEditAnswer2.text()
        answer3 = self.lineEditAnswer3.text()
        answer4 = self.lineEditAnswer4.text()

        correct_answer = self.lineEditCorrectAnswer.text()

        question = Question(
            text=text,
            answers=[answer1, answer2, answer3, answer4],
            correct_answer=correct_answer
        )

        if self.selected_question:
            question.id = self.selected_question.id

        if question.id:
            self.db_manager.update_question(question)
        else:
            self.db_manager.insert_question(question)

    def clear_form(self):
        input_fields = [
            self.lineEditQuestionText,
            self.lineEditAnswer1,
            self.lineEditAnswer2,
            self.lineEditAnswer3,
            self.lineEditAnswer4,
            self.lineEditCorrectAnswer
        ]
        for field in input_fields:
            field.clear()

    def on_add_button(self):
        self.save_question()
        self.load_questions()
        self.clear_form()

    def active_edit_mode(self):
        self.pushButtonAdd.setEnabled(False)
        self.pushButtonDel.setEnabled(True)
        self.pushButtonSave.setEnabled(True)

    def deactivate_edit_mode(self):
        self.pushButtonAdd.setEnabled(True)
        self.pushButtonDel.setEnabled(False)
        self.pushButtonSave.setEnabled(False)

    def on_list_item(self, model_index):
        self.active_edit_mode()
        self.item_index = int(model_index.row())
        self.selected_question = self.questions[self.item_index]
        self.fill_question_form(self.selected_question)

    def on_del_button(self):
        if self.selected_question != None:
            question = self.selected_question
            self.db_manager.delete_question(question.id)
            self.listWidgetQuestions.takeItem(self.item_index)
            self.questions.remove(question)
            self.deactivate_edit_mode()

    def fill_question_form(self, question):
        self.lineEditQuestionText.setText(question.text)
        self.lineEditAnswer1.setText(question.answers[0])
        self.lineEditAnswer2.setText(question.answers[1])
        self.lineEditAnswer3.setText(question.answers[2])
        self.lineEditAnswer4.setText(question.answers[3])
        self.lineEditCorrectAnswer.setText(question.correct_answer)

    def on_save_button(self):
        if self.selected_question != None:
            self.save_question()
            self.deactivate_edit_mode()
            self.load_questions()
            # self.clear_form()?

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = EditorGui()
    window.show()
    app.exec_()

