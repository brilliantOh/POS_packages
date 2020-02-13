#initialize

# menu_excel load
import pandas as pd
filepath = './menu_excel.xlsx'
menu_excel = pd.read_excel(filepath)

# menu class
class Menu:
    def __init__(self, idx):
        # instance attribute 정의
        self.name = menu_excel['메뉴명'][idx]
        self.cost = menu_excel['가격'][idx]
        self.qt = 0
        self.tot = 0

    # 수량 변경
    def qt_changed(self, num):
        # 음수 처리
        if self.qt + num < 0:
            self.qt = 0
        # 수량 취소
        elif num == 0:
            self.qt = 0
        else:
            self.qt += num

        return self.qt

    # 메뉴 금액 계산
    def menu_tot(self):
        self.tot = self.qt * self.cost

        return self.tot

# menu class instance
americano = Menu(0)
latte = Menu(1)
iceamericano = Menu(2)
icelatte = Menu(3)