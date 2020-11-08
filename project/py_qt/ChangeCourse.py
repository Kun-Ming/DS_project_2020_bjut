from PySide2.QtCore import Slot, Signal
from PySide2.QtWidgets import (QApplication, QLabel, QPushButton, QVBoxLayout, QWidget,
                               QGroupBox, QCheckBox, QGridLayout, QComboBox, )
import sys


class ChangeCourse(QWidget):
    change_course_signal = Signal(dict)

    def __init__(self, candidate_course, all_candidate_course, candidate_course_semester, parent=None):
        super(ChangeCourse, self).__init__(parent)

        self.course_info = dict()

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
        for i in range(0, len(candidate_course)-1):
            cb = QComboBox(self)
            # cb.addItem('')
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
        self.checkBox = []
        for i in candidate_course:
            if i[0] == '-':
                checkbox = QCheckBox(i[1:])
                checkbox.stateChanged.connect(self.checkbox_func)
                self.checkBox.append(checkbox)

        # Optional course combobox
        self.cb = []
        for i in range(0, len(self.checkBox)):
            cb = QComboBox(self)
            # cb.addItem('')
            for k in range(candidate_course_semester[self.checkBox[i].text()], 8):
                self.course_info[self.checkBox[i].text()] = candidate_course_semester[self.checkBox[i].text()]
                cb.addItem(str(k))
            cb.currentIndexChanged.connect(self.get_info)
            self.cb.append(cb)

        # Add label and combobox to GridLayout
        i = 0
        j = 0
        self.optional_layout = QGridLayout()
        for obj in range(len(self.checkBox)) :
            self.optional_layout.addWidget(self.checkBox[obj], j, i)
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

    @Slot()
    # Get info about order of course choose by user
    def get_info(self):
        cb = self.sender()
        if cb:
            if self.required_layout.indexOf(cb) != -1:
                pos = list(self.required_layout.getItemPosition(self.required_layout.indexOf(cb)))
                self.course_info[
                    self.required_layout.itemAtPosition(pos[0], pos[1] - 1).widget().text()] = cb.currentText()
            else:
                pos = list(self.optional_layout.getItemPosition(self.optional_layout.indexOf(cb)))
                if cb.currentText():
                    self.optional_layout.itemAtPosition(pos[0], pos[1] - 1).widget().setChecked(True)
                    self.course_info[
                        self.optional_layout.itemAtPosition(pos[0], pos[1] - 1).widget().text()] = cb.currentText()

    @Slot()
    def checkbox_func(self):
        box = self.sender()
        if box:
            pos = list(self.optional_layout.getItemPosition(self.optional_layout.indexOf(box)))
            combobox = self.optional_layout.itemAtPosition(pos[0], pos[1] + 1).widget()
            if box.checkState() == 0:
                combobox.setCurrentText('')
                del self.course_info[
                    self.optional_layout.itemAtPosition(pos[0], pos[1]).widget().text()]
            else:
                self.course_info[
                    self.optional_layout.itemAtPosition(pos[0], pos[1]).widget().text()] = combobox.currentText()

    @Slot()
    def return_info(self):
        self.close()
        self.change_course_signal.emit(self.course_info)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ChangeCourse(['a','b','c'])
    window.show()
    sys.exit(app.exec_())
