#pyqt_tab

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTabWidget, QVBoxLayout

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        tab1 = QWidget()
        tab2 = QWidget()

        tabs = QTabWidget()
        tabs.addTab(tab1, 'HOT음료')
        tabs.addTab(tab2, 'ICE음료')

        vbox = QVBoxLayout()
        vbox.addWidget(tabs)

        self.setLayout(vbox)

        self.setWindowTitle('POS')
        self.setGeometry(300,300,300,200)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MyApp()
    form.show()
    sys.exit(app.exec_())