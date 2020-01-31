#pyqt_draft3

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, qApp
from PyQt5.QtGui import QIcon

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        exitAction = QAction(QIcon('exit.png'), 'EXIT', self) #exit action 생성(icon)
        exitAction.setShortcut('Ctrl+Q') #action 단축키 설정
        exitAction.setStatusTip('Exit this application') #statustip 설정
        exitAction.triggered.connect(qApp.quit) #triggered signal->quit() method call

        self.statusBar() #statusbar 생성
        
        self.toolbar = self.addToolBar('EXIT') #toolbar 생성
        self.toolbar.addAction(exitAction) #toolbar-action 추가

        self.setWindowTitle('name of this Application')
        self.setGeometry(300,300,300,200)

"""        menubar = self.menuBar() #menubar 생성
        menubar.setNativeMenuBar(False)
        filemenu = menubar.addMenu('&File') #File menu 생성(단축키 Alt+F)
        filemenu.addAction(exitAction) #menu-action 추가"""


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myapp = MyApp()
    myapp.show()
    sys.exit(app.exec_())