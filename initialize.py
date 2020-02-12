#initialize

#menu_excel load
import pandas as pd
filepath = './menu_excel.xlsx'
menu_excel = pd.read_excel(filepath)

#menu class
class Menu:
    def __init__(self, idx):
        self.name = menu_excel['메뉴명'][idx] #이름 변수
        self.cost = menu_excel['가격'][idx] #가격 변수
        self.qt = 0 #수량 변수
        self.tot = 0 #금액 변수
        Menu.totsum = 0

    def qt_changed(self, num): #수량 변경 함수 #int만 받도록 수정 필요?
        if self.qt + num < 0:
            self.qt = 0 #수량이 0보다 작아지면 0이 되도록
        else:
            self.qt += num

        return self.qt

    def qt_canceled(self):
        self.qt = 0

        return self.qt

    def menu_tot(self): #메뉴별 금액 계산 함수
        self.tot = self.qt * self.cost

        return self.tot

    @classmethod #인스턴스 없이 호출 가능한 클래스 메서드
    def tot_sum(cls): #총액 계산 함수
        #이 클래스의 인스턴스의 tot 속성을 모두 합하는 기능
        return Menu.totsum

#menu instance
americano = Menu(0)
latte = Menu(1)
iceamericano = Menu(2)
icelatte = Menu(3)