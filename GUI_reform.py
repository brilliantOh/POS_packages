#GUI_reform

from initialize_reform import menu_names_list, Quantity_calculator
import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTabWidget, QTableWidget, QTableWidgetItem, \
    QPushButton, QLabel, QGroupBox, QInputDialog, QMessageBox, QHBoxLayout, QVBoxLayout, QGridLayout


# Main Window
class MyApp(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.title = 'POS_reform'
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(600, 300, 480, 320)

        widget = MyWidget(self)
        self.setCentralWidget(widget)

        self.show()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, '종료', 'POS를 종료합니까?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


# Central Widget
class MyWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        # TabWidget call
        tabs = QTabWidget()
        tabs.addTab(FirstTab(), '주문/계산')
        tabs.addTab(SecondTab(), '내역조회')

        vbox = QVBoxLayout()
        vbox.addWidget(tabs)

        self.setLayout(vbox)


# Tab Widget: 주문/계산
class FirstTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Groupbox call
        grid = QGridLayout()
        grid.addWidget(self.createGB0(), 0, 0)
        grid.addWidget(self.createGB1(), 0, 1)

        self.setLayout(grid)

    # Groupbox: 주문현황
    def create_groupbox_00(self):
        gbox = QGroupBox('주문현황')
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()

        # widget 정의
        self.table = QTableWidget()
        self.createTable()
        vbox.addWidget(self.table)
