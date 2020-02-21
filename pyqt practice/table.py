import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem

# table
class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'test'
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(600, 300, 480, 320)

        self.table = QTableWidget()
        self.createTable()

    def createTable(self):
        self.table.setColumnCount(6)
        self.table.setRowCount(4)
        self.table.setHorizontalHeaderLabels(['메뉴', '수량', '증가', '감소', '직접입력', '취소'])

        self.tableSetItem()

    def tableSetItem(self):
        item = QTableWidgetItem(1)
        self.table.setItem(0, 0, item)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())