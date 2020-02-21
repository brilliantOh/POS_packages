#pyqt_combobox

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QComboBox

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.label1 = QLabel('메뉴를 선택하세요.', self) #label default 텍스트
        self.label1.move(50,150)

        cbox = QComboBox(self)
        cbox.addItem('메뉴를 선택하세요.')
        cbox.addItem('아메리카노(HOT)') #combobox option 추가
        cbox.addItem('카페라떼(HOT)')
        cbox.move(50,50)

        cbox.activated[str].connect(self.onActivated) #option 활성화될 때 call

        self.setWindowTitle('POS by brilliantOh')
        self.setGeometry(300,300,400,300)
        self.show()

    def onActivated(self, text):
        self.label1.setText(text) #option명으로 label 텍스트 변경
        self.label1.adjustSize() #크기 자동 조절

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())