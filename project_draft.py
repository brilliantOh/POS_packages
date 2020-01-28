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

filepath = r'D:\Documents\GitHub\self-study\menu_excel.xlsx'
menu_excel = pd.read_excel(filepath)
menu_excel

#'menu_excel' -> dictionary
menu_dic = {}


#주문정보 Class (모두 0일 때, 양수 값이 있을 때?)
#메뉴별 수량을 무슨 type으로 받아서 저장할까? list? dictionary?
class Menu_Quantity:
    def __init__(self):
        pass #생성자: 전메뉴 수량 0 세팅
    def input_quantity(self):
        pass #수량(양수)
    def change_quantity(self):
        pass #수량 추가/변경/제거(int)
        #수량 output=0일 때 주문현황에서 메뉴 제거
        #수량 output<0일 수 없음

#최종금액 Class(수량 mul 가격)
class Total_amount:
    def __init__(self):
        pass #생성자: 0 세팅
    def calculate_total(self): #수량 정보가 input되면
        pass #메뉴별 수량x메뉴별 가격 sum
