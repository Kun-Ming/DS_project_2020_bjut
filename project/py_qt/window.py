import sys
from PySide2.QtCore import Qt, Slot
from PySide2.QtGui import QPainter
from PySide2.QtWidgets import (QAction, QApplication, QHeaderView, QHBoxLayout, QLabel, QLineEdit,
                               QMainWindow, QPushButton, QTableWidget, QTableWidgetItem,
                               QVBoxLayout, QWidget, QFileDialog, QGroupBox, QCheckBox, QGridLayout,
                               QComboBox, QMessageBox)

import file
import widget as widget
import ChangeCourse
import OptionalCourse
import c___part
import os

os.environ['QT_MAC_WANTS_LAYER'] = '1'
class MainWindow(QMainWindow):
    def __init__(self, widget):
        QMainWindow.__init__(self)
        self.widget = widget
        self.setWindowTitle("辅助选课系统")

        # Menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")
        self.sort_menu = self.menu.addMenu("Sort")
        self.menu.setNativeMenuBar(False)

        # Exit QAction
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.exit_app)

        # Import QAction
        Import = QAction("导入", self)
        Import.setShortcut("Ctrl+I")
        Import.triggered.connect(self.importDialog)

        # Save QAction
        # Save = QAction("保存课程表", self)
        # Save.setShortcut("Ctrl+S")
        # Save.triggered.connect(self.saveDialog)

        # Choose_course QAction
        Choose_course = QAction("选修", self)
        Choose_course.setShortcut("Ctrl+C")
        Choose_course.triggered.connect(self.choose_course)

        # Normal_sort QAction
        Normal_sort = QAction("生成课表", self)
        Normal_sort.setShortcut("Ctrl+R")
        Normal_sort.triggered.connect(self.cpp_sort)

        # Advanced_sort QAction
        Advanced_sort = QAction("生成课表 高级选项", self)
        Advanced_sort.setShortcut("Ctrl+Shift+R")
        Advanced_sort.triggered.connect(self.advanced_sort)

        # Add menu
        self.file_menu.addAction(exit_action)
        self.file_menu.addAction(Import)
        # self.file_menu.addAction(Save)

        self.sort_menu.addAction(Choose_course)
        self.sort_menu.addAction(Normal_sort)
        self.sort_menu.addAction(Advanced_sort)
        self.setCentralWidget(widget)

        self.choose_course_info = []

    @Slot()
    def cpp_sort(self):
        reader = file.read_course()
        reader.read('../data/course_private.txt')
        target = []
        for i in reader.target:
            if i[0] == '-':
                target.append(i[1:])
            else:
                target.append(i)
        res = c___part.normal_sort_cxx(target, reader.pre, reader.target_point,
                                  reader.base, reader.base_point)
        # Sort table
        for course in res:
            item = self.widget.table.findItems(course, Qt.MatchExactly)
            self.widget.table.item(item[0].row(), 1).setText(str(res[course]))
        self.widget.table.sortItems(1, Qt.AscendingOrder)



    @Slot()
    def exit_app(self, checked):
        QApplication.quit()

    @Slot()
    # Dialog of importing course information
    def importDialog(self):
        fname = QFileDialog.getOpenFileName(self, "open file", "../", 'Text files (*.txt)')
        if fname[0]:
            try:
                f = open(fname[0], 'r')
                with f:
                    data = f.read()
            except:
                message = QMessageBox()
                message.critical(self, 'Import error', 'fail to open')
                message.show()

        reader = file.read_course()
        if reader.read(fname[0])[0]:
            res = reader.target + reader.base
            res_point = reader.target_point + reader.base_point
            data = dict()
            for i in range(0, len(res)):
                data[str(res[i])] = [0, res_point[i]]
            widget.data = data
            widget.clear_table()
            widget.fill_table()
        else:
            message = QMessageBox()
            message.critical(self, 'Import error', reader.read(fname[0])[1])
            message.show()

    # @Slot()
    # # Dialog of saving sorted course information
    # def saveDialog(self):
    #     dir_path = QFileDialog.getExistingDirectory(self, "choose directory", "./")
    #     if dir_path[0]:
    #         print(dir_path)
    #     # some operation
    #     #save the schedule

    def search(self, course_name, choose_course_info):
        for i in choose_course_info:
            if course_name == '-' + i:
                return True
        return False

    @Slot()
    def advanced_sort(self):
        a, target, target_point, base, base_point, pre = file.get_course_info()

        for i in range(len(target)-1,-1,-1):
            if target[i][0] == '-':
                if not self.search(target[i], self.choose_course_info):
                    target.remove(target[i])
                    target_point.remove(target_point[i])
                    pre.remove(pre[i])

        for i in range(0, len(base)):
            if base[i][0] == '-':
                if not self.search(base[i], self.choose_course_info):
                    base.remove(target[i])
                    base_point.remove(target_point[i])

        self.target = target
        self.target_point = target_point
        self.base = base
        self.base_point = base_point
        self.pre = pre

        target = []
        for i in self.target:
            if i[0] == '-':
                target.append(i[1:])
            else:
                target.append(i)

        res = c___part.normal_sort_cxx(target, self.pre, self.target_point,
                                  self.base, self.base_point)
        pre2post = c___part.pre2post_cxx(target, self.pre, self.target_point,
                                  self.base, self.base_point)
        self.subwindow = ChangeCourse.ChangeCourse(candidate_course=self.target + self.base,
                                                   candidate_course_semester=res,
                                                   all_candidate_course=target+self.base,
                                                   pre2post=pre2post)
        self.subwindow.show()
        self.subwindow.change_course_signal.connect(self.advanced_sort_get_info)

    @Slot()
    def choose_course(self):
        self.choose_course_window = OptionalCourse.OptionalCourse(file.get_course_info()[0], self.choose_course_info)
        self.choose_course_window.show()
        self.choose_course_window.choose_course_signal.connect(self.choose_course_get_info)

    @Slot()
    def choose_course_get_info(self, info):
        self.choose_course_info = info
        print(self.choose_course_info)

    @Slot()
    def advanced_sort_get_info(self, info):
        self.ad_course_info = info
        # print(self.ad_course_info)
        self.widget.fill_table()
        for course in info:
            item = self.widget.table.findItems(course, Qt.MatchExactly)
            self.widget.table.item(item[0].row(), 1).setText(str(info[course]))

        item = self.widget.table.findItems("0", Qt.MatchExactly)
        for obj in item:
            self.widget.table.removeRow(self.widget.table.indexFromItem(obj).row())

        self.widget.table.sortItems(1, Qt.AscendingOrder)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = widget.Widget()
    window = MainWindow(widget)
    window.resize(800, 600)
    window.show()

    sys.exit(app.exec_())