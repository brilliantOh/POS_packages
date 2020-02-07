#project_draft.py

#list
total_amount = 0 #주문합계
menu_list = ['아메리카노', '카페라떼'] #메뉴(리스트)
quantity_list = [int(input('아메리카노 수량')), int(input('카페라떼 수량'))]
price_list = [4100, 4500]

for i in quantity_list:
    total_amount += quantity_list[i] * price_list[i]

total_amount

#dic
menu_list = ['아메리카노', '카페라떼'] #메뉴(리스트)
price_dic = {'아메리카노':4100, '카페라떼':4500} #메뉴-가격(딕셔너리)
quantity_dic = {'아메리카노':int(input('아메리카노 수량입력')), \
                     '카페라떼':int(input('카페라떼 수량입력'))} #메뉴-수량(딕셔너리)

def price_mul_quantity():
    total_amount = 0  # 주문합계
    for menu in menu_list: #문제: 수량변경 불가능
        total_amount += quantity_dic[menu] * price_dic[menu]
    return total_amount

price_mul_quantity()

#'menu_excel' load
import os
import pandas as pd

filepath = './menu_excel.xlsx'
menu_excel = pd.read_excel(filepath)
menu_excel

#주문정보 Class (모두 0일 때, 양수 값이 있을 때?)
#메뉴별 수량을 무슨 type으로 받아서 저장할까? list? dictionary?
class Menu_quantity:
    def __init__(self): #생성자: 전메뉴 수량 0 세팅
        quantity_list = [0,0,0,0]
        self.quantity_list = quantity_list
    def input_quantity(self, positive_list):
        if 1 in positive_list: #처음: 항상 1 값 하나가 들어옴
            quantity_list = positive_list
            return quantity_list
    def change_quantity(self, quantity_list, int_list): #수량 추가/변경/제거(int)
        for idx in range(len(int_list)):
            if int_list[idx] == 0:
                pass
            elif int_list[idx] != 0:
                quantity_list[idx] += int_list[idx]
        return quantity_list
        #수량 output=0일 때 주문현황에서 메뉴 제거
        #수량 output<0일 수 없음

test = Menu_quantity()
test.input_quantity([1,0,0,0]) #최초 입력
test.change_quantity([1,0,0,0], [-1,0,1,0]) #quantity_list를 자동으로 input할 수 없을까?


#최종금액 Class(수량 mul 가격)
class Total_amount:
    def __init__(self):
        pass #생성자: 0 세팅
    def calculate_total(self): #수량 정보가 input되면
        pass #메뉴별 수량x메뉴별 가격 sum
