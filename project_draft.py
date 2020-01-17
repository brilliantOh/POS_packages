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

#Class?
menu_list = ['아메리카노', '카페라떼'] #메뉴(리스트)
price_dic = {'아메리카노':4100, '카페라떼':4600} #메뉴-가격(딕셔너리)
quantity_dic = {'아메리카노':0, '카페라떼':0} #메뉴-수량(딕셔너리)

class Menu_Quantity:
    def __init__(self):


def quantity_input():
    pass

def price_mul_quantity():
    total_price = 0  # 주문합계
    for menu in menu_list: #문제: 수량변경 불가능
        total_price += quantity_dic[menu] * price_dic[menu]
    return total_price

price_mul_quantity()