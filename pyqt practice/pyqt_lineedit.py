#pyqt_lineedit

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.label1 = QLabel(self)
        self.label1.move(60,40)

        qline = QLineEdit(self) #lineedit
        qline.move(60,100)
        qline.textChanged[str].connect(self.onChanged) #텍스트 편집시 call

        self.setWindowTitle('POS by brilliantOh')
        self.setGeometry(300,300,400,300)
        self.show()

    def onChanged(self, text):
        self.label1.setText(text) #텍스트 입력을 label로 변경
        self.label1.adjustSize()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())