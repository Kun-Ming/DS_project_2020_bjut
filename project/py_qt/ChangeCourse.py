from PySide2.QtCore import Slot, Signal
from PySide2.QtWidgets import (QApplication, QLabel, QPushButton, QVBoxLayout, QWidget,
                               QGroupBox, QCheckBox, QGridLayout, QComboBox, )
import sys


class ChangeCourse(QWidget):
    change_course_signal = Signal(dict)

    def __init__(self, candidate_course, all_candidate_course,
                 candidate_course_semester, pre2post, parent=None):
        super(ChangeCourse, self).__init__(parent)

        self.course_info = dict()
        self.pre2post = pre2post
        self.candidate_course_semester = candidate_course_semester

        # Create required course GroupBox
        required_course = QGroupBox("必修")
        required_course.setFlat(False)

        # Course Label
        self.checkBox = []
        for i in candidate_course:
            if i[0] != '-':
                self.course_info[i] = ''
                label = QLabel(i)
                self.checkBox.append(label)

        # Course combobox
        self.cb = []
        for i in range(0, len(candidate_course)):
            if candidate_course[i][0] != '-':
                cb = QComboBox(self)
                for k in range(candidate_course_semester[all_candidate_course[i]], 8):
                    self.course_info[all_candidate_course[i]] = candidate_course_semester[all_candidate_course[i]]
                    cb.addItem(str(k))
                cb.currentIndexChanged.connect(self.get_info)
                self.cb.append(cb)

        # Add label and combobox to GridLayout
        i = 0
        j = 0
        self.required_layout = QGridLayout()
        for obj in range(len(self.checkBox)):
            self.required_layout.addWidget(self.checkBox[obj], j, i)
            self.required_layout.addWidget(self.cb[obj], j, i+1)
            if i == 4:
                j = j + 1
                i = 0
            else:
                i = i + 2

        required_course.setLayout(self.required_layout)

        # Create optional course GroupBox
        optional_course = QGroupBox("选修")
        optional_course.setFlat(False)

        # Optional course checkbox
        self.checkBox_optional = []
        for i in candidate_course:
            if i[0] == '-':
                checkbox = QLabel(i[1:])
                # checkbox.stateChanged.connect(self.checkbox_func)
                self.checkBox_optional.append(checkbox)

        # Optional course combobox
        self.cb = []
        for i in range(0, len(self.checkBox_optional)):
            cb = QComboBox(self)
            # cb.addItem('')
            for k in range(candidate_course_semester[self.checkBox_optional[i].text()], 8):
                self.course_info[self.checkBox_optional[i].text()] = candidate_course_semester[self.checkBox_optional[i].text()]
                cb.addItem(str(k))
            cb.currentIndexChanged.connect(self.get_info)
            self.cb.append(cb)

        # Add label and combobox to GridLayout
        i = 0
        j = 0
        self.optional_layout = QGridLayout()
        for obj in range(len(self.checkBox_optional)) :
            self.optional_layout.addWidget(self.checkBox_optional[obj], j, i)
            self.optional_layout.addWidget(self.cb[obj], j, i + 1)
            if i == 4:
                j = j + 1
                i = 0
            else:
                i = i + 2

        optional_course.setLayout(self.optional_layout)
        button = QPushButton("确定", self)
        button.clicked.connect(self.return_info)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(required_course)
        mainLayout.addWidget(optional_course)
        mainLayout.addWidget(button)

        self.setLayout(mainLayout)
        self.setWindowTitle("高级排课选项")


    # Aborted function
    def defer_post_course(self, post_course, grid, pre_semester):
        i = 0;
        j = 0
        print(type(pre_semester))
        pre_semester = int(pre_semester)
        for course in post_course:
            if grid == 'required':
                i = 0;
                j = 0
                for a in range(len(self.checkBox_optional)):
                    if self.optional_layout.itemAtPosition(i, j).widget().text() == course[1:]:
                        self.optional_layout.itemAtPosition(i, j + 1).widget().clear()
                        for index in range(pre_semester, 8):
                            self.optional_layout.itemAtPosition(i, j + 1).widget().addItem(str(index))
                            self.optional_layout.itemAtPosition(i, j + 1).widget().currentIndexChanged.connect(
                                self.get_info)

                    if i == 4:
                        j = j + 1
                        i = 0
                    else:
                        i = i + 2

            else:
                i = 0;
                j = 0
                for a in range(len(self.checkBox)):
                    if self.required_layout.itemAtPosition(i, j).widget().text() == course:
                        self.required_layout.itemAtPosition(i, j + 1).widget().clear()
                        for index in range(pre_semester, 8):
                            self.required_layout.itemAtPosition(i, j + 1).widget().addItem(str(index))
                            self.required_layout.itemAtPosition(i, j + 1).widget().currentIndexChanged.connect(
                                self.get_info)

                    if j == 4:
                        i = i + 1
                        j = 0
                    else:
                        j = j + 2

    @Slot()
    # Get info about order of course choose by user
    def get_info(self):
        # str2num = {'1':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8}
        cb = self.sender()
        if cb:

            if self.required_layout.indexOf(cb) != -1:
                pos = list(self.required_layout.getItemPosition(self.required_layout.indexOf(cb)))
                self.course_info[
                    self.required_layout.itemAtPosition(pos[0], pos[1] - 1).widget().text()] = cb.currentText()
                post_course = self.pre2post[self.required_layout.itemAtPosition(pos[0], pos[1] - 1).widget().text()]
                # self.defer_post_course(post_course, "rquired", cb.currentText())
                if len(cb.currentText()):
                    for course in post_course:
                        i = 0; j = 0
                        for a in range(len(self.checkBox)):
                            if self.required_layout.itemAtPosition(i, j).widget().text() == course:
                                self.required_layout.itemAtPosition(i, j + 1).widget().clear()

                                for index in range(self.candidate_course_semester[course] -
                                                   self.candidate_course_semester[self.required_layout.itemAtPosition(pos[0], pos[1] - 1).widget().text()]
                                                   + int(cb.currentText()), 9):
                                    self.required_layout.itemAtPosition(i, j + 1).widget().addItem(str(index))
                                    self.required_layout.itemAtPosition(i, j + 1).widget().currentIndexChanged.connect(
                                        self.get_info)
                            if j == 4:
                                i = i + 1
                                j = 0
                            else:
                                j = j + 2

                        i = 0; j = 0
                        for a in range(len(self.checkBox_optional)):
                            if self.optional_layout.itemAtPosition(i, j).widget().text() == course:
                                self.optional_layout.itemAtPosition(i, j + 1).widget().clear()

                                for index in range(self.candidate_course_semester[course] -
                                                   self.candidate_course_semester[self.required_layout.itemAtPosition(pos[0], pos[1] - 1).widget().text()]
                                                   + int(cb.currentText()), 9):
                                    self.optional_layout.itemAtPosition(i, j + 1).widget().addItem(str(index))
                                    self.optional_layout.itemAtPosition(i, j + 1).widget().currentIndexChanged.connect(
                                        self.get_info)
                            if j == 4:
                                i = i + 1
                                j = 0
                            else:
                                j = j + 2

            else:
                pos = list(self.optional_layout.getItemPosition(self.optional_layout.indexOf(cb)))
                if cb.currentText():
                    self.course_info[
                        self.optional_layout.itemAtPosition(pos[0], pos[1] - 1).widget().text()] = cb.currentText()
                post_course = self.pre2post[self.optional_layout.itemAtPosition(pos[0], pos[1] - 1).widget().text()]
                # self.defer_post_course(post_course, "optional", cb.currentText())
                for course in post_course:
                    i = 0; j = 0
                    for a in range(len(self.checkBox_optional)):
                        if self.optional_layout.itemAtPosition(i, j).widget().text() == course:
                            self.optional_layout.itemAtPosition(i, j + 1).widget().clear()
                            for index in range(self.candidate_course_semester[course] -
                                               self.candidate_course_semester[self.required_layout.itemAtPosition(pos[0], pos[1] - 1).widget().text()]
                                               + int(cb.currentText()), 9):
                                self.optional_layout.itemAtPosition(i, j + 1).widget().addItem(str(index))
                                self.optional_layout.itemAtPosition(i, j + 1).widget().currentIndexChanged.connect(
                                    self.get_info)

                        if j == 4:
                            i = i + 1
                            j = 0
                        else:
                            j = j + 2

    @Slot()
    def return_info(self):
        self.close()
        self.change_course_signal.emit(self.course_info)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ChangeCourse(['a','b','c'])
    window.show()
    sys.exit(app.exec_())
