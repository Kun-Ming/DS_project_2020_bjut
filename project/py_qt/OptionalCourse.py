from PySide2.QtCore import Slot, Signal
from PySide2.QtWidgets import (QApplication, QPushButton, QVBoxLayout, QWidget,
							   QGroupBox, QCheckBox, QGridLayout)
import sys


class OptionalCourse(QWidget):
	choose_course_signal = Signal(dict)

	def __init__(self, all_course_info, parent=None):
		super(OptionalCourse, self).__init__(parent)

		self.course_info = []

		# Create optional course GroupBox
		optional_course = QGroupBox("选修")
		optional_course.setFlat(False)

		# Optional course checkbox
		self.checkBox = []
		for i in all_course_info:
			if i[0] == '-':
				checkbox = QCheckBox(i[1:])
				checkbox.stateChanged.connect(self.checkbox_func)
				self.checkBox.append(checkbox)

		# Add label and combobox to GridLayout
		i = 0
		j = 0
		self.optional_layout = QGridLayout()
		for obj in range(len(self.checkBox)):
			self.optional_layout.addWidget(self.checkBox[obj], j, i)
			if i == 4:
				j = j + 1
				i = 0
			else:
				i = i + 2

		optional_course.setLayout(self.optional_layout)
		button = QPushButton("确定", self)
		button.clicked.connect(self.return_info)

		mainLayout = QVBoxLayout()
		mainLayout.addWidget(optional_course)
		mainLayout.addWidget(button)

		self.setLayout(mainLayout)
		self.setWindowTitle("选修课")


	@Slot()
	def checkbox_func(self):
		box = self.sender()

		if box:
			pos = list(self.optional_layout.getItemPosition(self.optional_layout.indexOf(box)))
			self.course_info.append(self.optional_layout.itemAtPosition(pos[0], pos[1]).widget().text())

	@Slot()
	def return_info(self):
		self.close()
		self.choose_course_signal.emit(self.course_info)


if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = OptionalCourse(['-a', '-b', '-c'])
	window.show()
	sys.exit(app.exec_())
