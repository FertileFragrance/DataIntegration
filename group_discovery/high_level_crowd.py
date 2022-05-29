#!/opt/anaconda3/bin/python
# -*- coding: UTF-8 -*-
"""
@Author: njuselhx
@Time: 2022/5/29 下午7:52
@File: group_discovery.py
@Software: PyCharm
"""
import pandas as pd


def discover_high_level():
    df = pd.read_csv('../result.csv')
    print(df['tran_amt_gzdf'].describe())
    # 一年大于60w算作高端资产，大概100-200人
    print(df['tran_amt_gzdf'].nlargest(100, keep='all'))
    print(df['base_all_bal'].describe())
    # 余额超过80w算作高端资产，大概500多人
    print(df['base_all_bal'].nlargest(600, keep='all'))
    print(df['month_avg_sbyb_amt'].describe())
    # 医保社保每月超过1w算作高端资产，大概3000多人
    print(df['month_avg_sbyb_amt'].nlargest(3000, keep='all'))
    print(df['month_avg_sdrq_amt'].describe())
    # 水电燃气每月500以上算作高端小区，大概几十人
    print(df['month_avg_sdrq_amt'].nlargest(100, keep='all'))
    df = df.drop(df[(df['tran_amt_gzdf'] < 600000) & (df['base_all_bal'] < 800000) &
                    (df['month_avg_sbyb_amt'] < 10000) & (df['month_avg_sdrq_amt'] < 500)].index)
    # 经过第一次筛选有13886人
    print(df)
    df = df.drop(df[(df['owed_int_times_90l'] > 0) | (df['owed_int_times_90g'] > 0) |
                    (df['overdue_times_90l'] > 0) | (df['overdue_times_90g'] > 0) | (df['is_black'] == 1)].index)
    # 经过第二次筛选有13593人
    print(df)
    print(df['djk_mx_expense_sum'].describe())
    print(df['djk_mx_expense_sum'].nlargest(2000, keep='all'))
    print(df['max_cac_intc_pr'].describe())
    print(df['max_cac_intc_pr'].nlargest(1000, keep='all'))
    df = df.drop(df[(df['max_cac_intc_pr'] == 0) & (df['base_sumloan_amt'] == 0)].index)
    # 经过第三次筛选有1602人
    print(df)
    df.to_csv('high_level.csv')

    print(df['birthday'].describe())
    print(df['marrige'].describe())
    print(df['sex'].describe())
    print(df['education'].describe())


if __name__ == '__main__':
    discover_high_level()
