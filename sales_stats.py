'''
sales_stats.py
=========================
statistics module of POS_packages
'''
from datetime import date, timedelta
import pandas as pd


class POS_statistics:
    '''
    POS의 매출집계를 하는 클래스입니다.
    '''
    def __init__(self):
        self.stats_cols_list = ['매출일시', '매출건수', '매출수량', '매출총액', '현금매출', '카드매출']
        self.stats_df = pd.DataFrame(columns=self.stats_cols_list)

    def stats_period_sales(self, start_date, end_date):
        '''
        :explain: 입력한 시작일부터 종료일까지 기간의 매출집계

        :param date start_date: 시작일
        :param date end_date: 종료일
        :return dataframe: stats_df 기간별 매출집계
        '''
        self.stats_df = pd.DataFrame(columns=self.stats_cols_list)

        details_df = pd.read_excel(r'C:\Users\JH\POS_packages\order_history.xlsx', sheet_name='receipt')
        summary_df = pd.read_excel(r'C:\Users\JH\POS_packages\order_history.xlsx', sheet_name='summary')
        period_int = (end_date - start_date).days

        for i in range(period_int + 1):
            order_date_str = (start_date + timedelta(days=i)).strftime('%Y-%m-%d')
            date_summary_df = summary_df.loc[(summary_df['주문일시'].str.contains(order_date_str)), :]
            date_details_df = details_df.loc[(details_df['주문일시'].str.contains(order_date_str)), :]
            cash_df = date_details_df.loc[(date_details_df['지불수단'] == '현금'), :]
            card_df = date_details_df.loc[(date_details_df['지불수단'] == '카드'), :]

            count_int = len(date_summary_df['주문일시'])
            quantity_int = sum(date_details_df['수량'])
            amount_int = sum(date_details_df['금액'])
            cash_int = sum(cash_df['금액'])
            card_int = sum(card_df['금액'])

            stats_list = [order_date_str, count_int, quantity_int, amount_int, cash_int, card_int]
            self.stats_df = self.stats_df.append(pd.DataFrame([stats_list], columns=self.stats_cols_list),
                                                 ignore_index=True)

        return self.stats_df


stats = POS_statistics()