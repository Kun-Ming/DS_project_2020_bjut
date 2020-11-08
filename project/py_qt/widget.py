from PySide2.QtCore import Qt, Slot
from PySide2.QtGui import QPainter
from PySide2.QtWidgets import (QAction, QApplication, QHeaderView, QHBoxLayout, QLabel,
							   QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
							   QVBoxLayout, QWidget, QMessageBox)
from PySide2.QtCharts import QtCharts

import file


class Widget(QWidget):
	def __init__(self):
		QWidget.__init__(self)
		self.items = 0

		# Left of window
		self.table = QTableWidget()
		self.table.setColumnCount(3)
		self.table.setHorizontalHeaderLabels(["课程名", "计划学期", "学分"])
		self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

		self.table.setContextMenuPolicy(Qt.ActionsContextMenu)
		send_option1 = QAction(self.table)
		send_option1.setText("移动")
		# send_option1.triggered.connect(self.show_modify_dialog)
		send_option2 = QAction(self.table)
		send_option2.setText("删除")
		self.table.addAction(send_option1)
		self.table.addAction(send_option2)

		# Chart
		self.chart_view = QtCharts.QChartView()
		self.chart_view.setRenderHint(QPainter.Antialiasing)

		# Right
		self.CourseName = QLineEdit()
		self.Pre = QLineEdit()
		self.Point = QLineEdit()
		self.add = QPushButton("Add")
		self.clear = QPushButton("Clear")
		self.quit = QPushButton("Quit")
		self.plot = QPushButton("Plot")

		# Disabling 'Add' button
		self.add.setEnabled(False)

		self.right = QVBoxLayout()
		self.right.setMargin(10)
		self.right.addWidget(QLabel("课程名"))
		self.right.addWidget(self.CourseName)
		self.right.addWidget(QLabel("先修课程"))
		self.right.addWidget(self.Pre)
		self.right.addWidget(QLabel("学分"))
		self.right.addWidget(self.Point)

		self.right.addWidget(self.add)
		self.right.addWidget(self.plot)
		self.right.addWidget(self.chart_view)
		self.right.addWidget(self.clear)
		self.right.addWidget(self.quit)

		# QWidget Layout
		self.layout = QHBoxLayout()

		# self.table_view.setSizePolicy(size)
		self.layout.addWidget(self.table)
		self.layout.addLayout(self.right)

		# Set the layout to the QWidget
		self.setLayout(self.layout)

		# Signals and Slots
		self.add.clicked.connect(self.add_element)
		self.quit.clicked.connect(self.quit_application)
		self.plot.clicked.connect(self.plot_data)
		self.clear.clicked.connect(self.clear_table)
		self.CourseName.textChanged[str].connect(self.check_disable)
		self.Pre.textChanged[str].connect(self.check_disable)
		self.Point.textChanged[str].connect(self.check_disable)

		# Fill table
		self.data = file.get_course_info()[0]
		self.clear_table()
		self.fill_table()

		# reader = file.read_course()
		# if reader.read('../data/course_private.txt')[0]:
		# 	res = reader.target + reader.base
		# 	res_point = reader.target_point + reader.base_point
		# 	data = dict()
		# 	for i in range(0, len(res)):
		# 		data[str(res[i])] = [0, res_point[i]]
		# 	self.data = data
		# 	self.clear_table()
		# 	self.fill_table()
		#
		# else:
		# 	message = QMessageBox()
		# 	message.critical(self, 'Import error', reader.read('../data/course_private.txt')[1])
		# 	message.show()

	@Slot()
	def add_element(self):
		name = self.CourseName.text()
		pre = self.Pre.text()
		Point = self.Point.text()
		pre = pre.split(' ')

		#write into file
		writer = file.read_course()
		if pre[0] != '':
			writer.write(target=name, target_point=Point, base='', base_point='', pre=pre)
		else:
			writer.write(target='', target_point='', base=name, base_point=Point, pre='')

		self.CourseName.setText('')
		self.Pre.setText('')
		self.Point.setText('')

		# Reload from file to widget
		reader = file.read_course()
		if reader.read()[0]:
			res = reader.target + reader.base
			res_point = reader.target_point + reader.base_point
			data = dict()
			for i in range(0, len(res)):
				data[str(res[i])] = [0, res_point[i]]
			self.data = data
			self.clear_table()
			self.fill_table()
		else:
			# Raise error
			message = QMessageBox()
			message.critical(self, 'Import error', reader.read()[1])
			message.show()

			# delete wrong course
			if pre:  # target course
				reader.del_target()
			else:
				reader.del_base()

	@Slot()
	def check_disable(self, s):
		if (self.CourseName.text() and self.Point.text()) or (
				self.Pre.text() and self.CourseName.text() and self.Point.text()):
			self.add.setEnabled(True)
		else:
			self.add.setEnabled(False)

	@Slot()
	def plot_data(self):
		# Get table information
		series = QtCharts.QPieSeries()
		number = dict()
		for i in range(self.table.rowCount()):
			if str(self.table.item(i, 1).text()) in number:
				number[str(self.table.item(i, 1).text())] = \
					number[str(self.table.item(i, 1).text())] + float(self.table.item(i, 2).text())
			else:
				number[str(self.table.item(i, 1).text())] = float(self.table.item(i, 2).text())
		for i in number:
			text = "第" + str(i) + "学期"
			series.append(text, number[str(i)])

		chart = QtCharts.QChart()
		chart.addSeries(series)
		chart.legend().setAlignment(Qt.AlignLeft)
		self.chart_view.setChart(chart)

	@Slot()
	def quit_application(self):
		QApplication.quit()

	def fill_table(self, data=None):
		data = self.data
		for course, info in data.items():
			course = course.replace('-', '')
			course_item = QTableWidgetItem(course)
			semester_item = QTableWidgetItem("{:d}".format(info[0]))
			point_item = QTableWidgetItem("{:.1f}".format(info[1]))

			course_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
			semester_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
			point_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

			semester_item.setTextAlignment(Qt.AlignCenter)
			point_item.setTextAlignment(Qt.AlignCenter)

			self.table.insertRow(self.items)
			self.table.setItem(self.items, 0, course_item)
			self.table.setItem(self.items, 1, semester_item)
			self.table.setItem(self.items, 2, point_item)
			self.items += 1

	@Slot()
	def clear_table(self):
		self.table.setRowCount(0)
		self.items = 0
