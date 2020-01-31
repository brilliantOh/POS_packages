#pyqt_messagebox

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('POS of brilliantOh')
        self.setGeometry(300,300,300,200)
        self.show()

    def closeEvent(self, event): #종료 이벤트
        reply = QMessageBox.question(self, 'Quit', 'POS를 종료합니까?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        #창 이름, 표시할 텍스트, 디폴트 선택 버튼

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = MyApp()
   sys.exit(app.exec_())