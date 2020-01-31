#pyqt draft

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QToolTip
from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtGui import QIcon, QFont

class Form(QWidget): #기본 form
    def __init__(self): #생성자
        QWidget.__init__(self, flags=Qt.Widget)
        self.init_widget() #위젯 생성 함수 호출

    def init_widget(self):
        QToolTip.setFont(QFont('SansSerif', 10)) #font 설정
        self.setToolTip('<b>Qwidget</b> widget.') #tooltip 설정

        quit_btn = QPushButton('QUIT', self) #Pushbutton 생성
        quit_btn.setToolTip('<b>QPushButton</b> widget.') #tooltip 텍스트 설정
        quit_btn.move(220,0)
        quit_btn.resize(quit_btn.sizeHint())
        quit_btn.clicked.connect(QCoreApplication.instance().quit) #clicked signal->quit() method call

        self.setWindowTitle('POS by brilliantOh') #application 이름 설정
        self.setWindowIcon(QIcon('image_icon.jpg')) #icon 불러오기
        self.setGeometry(300,300,300,200) #move, resize 통합

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec_())
