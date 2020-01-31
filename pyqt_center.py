# pyqt_draft4

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, qApp, QDesktopWidget
from PyQt5.QtGui import QIcon

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        exitAction = QAction(QIcon('exit.png'), 'EXIT', self)  # exit action 생성(icon)
        exitAction.setShortcut('Ctrl+Q')  # action 단축키 설정
        exitAction.setStatusTip('Exit this application')  # statustip 설정
        exitAction.triggered.connect(qApp.quit)  # triggered signal->quit() method call

        self.statusBar()  # statusbar 생성

        self.toolbar = self.addToolBar('EXIT')  # toolbar 생성
        self.toolbar.addAction(exitAction)  # toolbar-action 추가

        self.setWindowTitle('name of this Application')
        self.resize(500, 350)
        self.center() #method call

    def center(self): #중심에 나타나게 하는 method
        qr = self.frameGeometry() #창 위치, 크기정보 가져오기
        cp = QDesktopWidget().availableGeometry().center() #화면 중심 파악
        qr.moveCenter(cp) #현재 창의 중심 위치를 화면의 중심으로
        self.move(qr.topLeft()) #이동

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myapp = MyApp()
    myapp.show()
    sys.exit(app.exec_())