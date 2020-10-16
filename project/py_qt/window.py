import sys
from PySide2.QtCore import Qt, Slot
from PySide2.QtGui import QPainter
from PySide2.QtWidgets import (QAction, QApplication, QHeaderView, QHBoxLayout, QLabel, QLineEdit,
                               QMainWindow, QPushButton, QTableWidget, QTableWidgetItem,
                               QVBoxLayout, QWidget, QFileDialog, QGroupBox, QCheckBox, QGridLayout,
                               QComboBox, QMessageBox)

import file
import widget as widget
import subwindow as sw
import c___part


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
        Save = QAction("保存课程表", self)
        Save.setShortcut("Ctrl+S")
        Save.triggered.connect(self.saveDialog)

        # Normal_sort QAction
        Normal_sort = QAction("生成课表", self)
        Normal_sort.setShortcut("Ctrl+R")
        Normal_sort.triggered.connect(self.cpp_sort)

        # Advanced_sort QAction
        Advanced_sort = QAction("生成课表 高级选项", self)
        Advanced_sort.setShortcut("Ctrl+Shift+R")
        Advanced_sort.triggered.connect(self.advaced_sort)

        # add menu
        self.file_menu.addAction(exit_action)
        self.file_menu.addAction(Import)
        self.file_menu.addAction(Save)

        self.sort_menu.addAction(Normal_sort)
        self.sort_menu.addAction(Advanced_sort)
        self.setCentralWidget(widget)

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
        res = c___part.interface1(target, reader.pre, reader.target_point,
                                  reader.base, reader.base_point);
        # print(res)
        for course in res:
            item = self.widget.table.findItems(course, Qt.MatchExactly)
            self.widget.table.item(item[0].row(), 1).setText(str(res[course]))
        self.widget.table.sortItems(1, Qt.AscendingOrder)



    @Slot()
    def exit_app(self, checked):
        QApplication.quit()

    @Slot()
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

    @Slot()
    def saveDialog(self):
        dir_path = QFileDialog.getExistingDirectory(self, "choose directory", "./")
        if dir_path[0]:
            print(dir_path)
        # some operation
        #save the schedule

    @Slot()
    def advaced_sort(self):
        self.subwindow = sw.SubWindow(required_course_name=self.widget.data.keys())
        self.subwindow.show()
        self.subwindow.signal.connect(self.get_info)

    @Slot()
    def get_info(self, info):
        self.ad_course_info = info
        print(self.ad_course_info)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = widget.Widget()
    window = MainWindow(widget)
    window.resize(800, 600)
    window.show()

    sys.exit(app.exec_())