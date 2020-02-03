#pyqt_checkbox

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QCheckBox
from PyQt5.QtCore import Qt

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        cbox1 = QCheckBox('아메리카노(HOT)', self) #메뉴 checkbox
        #cbox1.toggle() #항상 켜지게 토글
        cbox1.stateChanged.connect(self.changeTitle) #체크될 경우 call할 함수

        self.setWindowTitle('POS by brilliantOh')
        self.setGeometry(300,300,300,200)
        self.show()

    def changeTitle(self, state):
        if state == Qt.Checked: #체크될 경우 title 변경
            self.setWindowTitle('HOT Americano')
        else:
            self.setWindowTitle('POS by brilliantOh')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())