#pyqt

import sys
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import pyqtSlot

class Button(QPushButton):
    def __init__(self):
        QPushButton.__init__(self, '0')
        self.setFixedSize(100,100)
        self.click_cnt = 0
        self.pressed.connect(self._pressed)

    @pyqtSlot()
    def _pressed(self):
        self.click_cnt += 1
        self.setText(str(self.click_cnt))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Button()
    form.show()
    exit(app.exec_())