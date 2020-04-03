'''
calculator.py
=================================
calculation module of POS_packages
'''
import os
import pandas as pd

# load menu data by pandas
excel_path = r'C:\Users\JH\POS_packages'
excel_name = 'menu_excel.xlsx'
menu_excel = pd.read_excel(excel_path + os.sep + excel_name, index_col=None, header=0)


# calculate menu quantity
class POS_calculator:
    '''POS의 메뉴 추가/감소/취소 기능을 하는 클래스입니다.

    '''
    def __init__(self):
        self.cart_list = []

    def add_qty(self, menu_str):
        '''
        :explain: 입력한 메뉴를 장바구니에 한 번 추가합니다.

        :param string menu_str: 메뉴 이름
        :return list: 장바구니

        >>> cal.add_qty('아메리카노(ICE)')
        ['아메리카노(ICE)']
        >>> cal.add_qty('카페라떼(ICE)')
        ['아메리카노(ICE)', '카페라떼(ICE)']
        >>> cal.add_qty('카페라떼(ICE)')
        ['아메리카노(ICE)', '카페라떼(ICE)', '카페라떼(ICE)']

        '''

        self.cart_list.append(menu_str)
        return self.cart_list

    def minus_qty(self, menu_str):
        '''
        :explain: 입력한 메뉴가 장바구니에 있다면 한 번 제거합니다.

        :param string menu_str: 메뉴 이름
        :return list: 장바구니

        >>> cal.minus_qty('아메리카노(ICE)')
        ['카페라떼(ICE)', '카페라떼(ICE)']

        '''
        if self.cart_list.count(menu_str) != 0:
            self.cart_list.remove(menu_str)
            return self.cart_list

    def cancel_qty(self, menu_str):
        '''
        :explain: 입력한 메뉴가 장바구니에 있다면 모두 제거합니다.

        :param string menu_str: 메뉴 이름
        :return list: 장바구니

        >>> cal.cancel_qty('카페라떼(ICE)')
        []

        '''
        while self.cart_list.count(menu_str) != 0:
            self.cart_list.remove(menu_str)
        return self.cart_list

    def input_qty(self, menu_str, input_int):
        '''
        :explain: 입력한 메뉴가 입력값이 되도록 장바구니에 추가/제거합니다. 입력값보다 기존 수량이 작으면 더하고, 크면 줄입니다.

        :param string menu_str: 메뉴 이름
        :param int input_int: 메뉴 수량
        :return list: 장바구니

        >>> cal.input_qty('아메리카노(ICE)', 3)
        ['아메리카노(ICE)', '아메리카노(ICE)', '아메리카노(ICE)']

        '''
        while self.cart_list.count(menu_str) != input_int:
            if self.cart_list.count(menu_str) < input_int:
                self.cart_list.append(menu_str)
            elif self.cart_list.count(menu_str) > input_int:
                self.cart_list.remove(menu_str)
        return self.cart_list

    def cancel_all_qty(self):
        '''
        :explain: 장바구니를 비웁니다.

        :return list: 장바구니

        >>> cal.cancel_all_qty()
        []

        '''
        self.cart_list.clear()
        return self.cart_list

    def return_menu_qty(self, menu_str):
        '''
        :explain: 입력한 메뉴의 수량을 반환합니다.

        :param string menu_str: 메뉴 이름
        :return int: 메뉴 수량

        >>> cal.return_menu_qty('아메리카노(ICE)')
        0

        '''
        return self.cart_list.count(menu_str)

    def return_total_qty(self):
        '''
        :explain: 현재 장바구니에 있는 메뉴들의 수량을 합한 값을 반환합니다.

        :return int: 총 수량
        '''
        return len(self.cart_list)

    def return_menu_cost(self, menu_str):
        '''
        :explain: 입력한 메뉴의 단가를 반환합니다. 메뉴 정보가 있는 dataframe(menu_excel)에서 입력한 메뉴의 가격 col을 찾습니다.

        :param string menu_str: 메뉴 이름
        :return int: 메뉴 가격

        >>> cal.return_menu_cost('아메리카노(ICE)')
        4000

        '''
        for i in range(len(menu_excel['메뉴명'])):
            if menu_str == menu_excel['메뉴명'][i]:
                return menu_excel['가격'][i]

    def return_menu_amount(self, menu_str):
        '''
        :explain: 입력한 메뉴의 단가와 수량을 곱한 값을 반환합니다. 메뉴 정보가 있는 dataframe(menu_excel)에서 입력한 메뉴의 가격 col을 찾아 장바구니의 수량만큼 곱합니다.

        :param string menu_str: 메뉴 이름
        :return int: 메뉴 금액

        >>> cal.return_menu_qty('아메리카노(ICE)')
        2
        >>> cal.return_menu_amount('아메리카노(ICE)')
        8000

        '''
        for i in range(len(menu_excel['메뉴명'])):
            if menu_str == menu_excel['메뉴명'][i]:
                return self.cart_list.count(menu_str) * menu_excel['가격'][i]

    def return_total_amount(self):
        '''
        :explain: 현재 장바구니에 있는 메뉴들의 금액을 합한 값을 반환합니다.

        :return int: 총 금액

        >>> cal.cart_list
        ['아메리카노(ICE)', '카페라떼(ICE)']
        >>> cal.return_total_amount()
        8500
        '''
        total_amount_int = 0

        for i in range(len(set(self.cart_list))):
            total_amount_int += self.return_menu_amount(list(set(self.cart_list))[i])

        return total_amount_int


cal = POS_calculator()