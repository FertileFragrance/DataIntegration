#!/opt/anaconda3/bin/python
# -*- coding: UTF-8 -*-
"""
@Author: njuselhx
@Time: 2022/5/29 下午5:21
@File: integration.py
@Software: PyCharm
"""
import pandas as pd


def merge_data(df):
    df_uid = pd.read_csv('../uid_label.csv')
    df_uid.set_index("uid", inplace=True)
    df.set_index("uid", inplace=True)
    res = df_uid.join(df, how='left', sort=False)
    res.fillna(0, inplace=True)
    res.to_csv('uid_label.csv')


def find_max(item_list, uid):
    index = -1
    max_pay_term = -1
    for idx, item in enumerate(item_list):
        if item[0] != uid:
            continue
        if max_pay_term < item[1]:
            index = idx
            max_pay_term = item[1]
    return index, max_pay_term


def max_cac_intc_pr():
    df = pd.read_csv('from_dm_v_tr_huanx_mx/cac_intc_pr.csv')
    uid_list = []
    item_list = []
    for idx, data in df.iterrows():
        if data['uid'] not in uid_list:
            uid_list.append(data['uid'])
            item_list.append([data['uid'], data['cac_intc_pr']])
        else:
            item_list_index, max_cac_intc_pr = find_max(item_list, data['uid'])
            if data['cac_intc_pr'] > max_cac_intc_pr:
                item_list[item_list_index] = [data['uid'], data['cac_intc_pr']]
    df = pd.DataFrame(columns=['uid', 'max_cac_intc_pr'], data=item_list)
    merge_data(df)


def max_intr():
    df = pd.read_csv('from_dm_v_tr_huanx_mx/intr.csv')
    uid_list = []
    item_list = []
    for idx, data in df.iterrows():
        if data['uid'] not in uid_list:
            uid_list.append(data['uid'])
            item_list.append([data['uid'], data['intr']])
        else:
            item_list_index, max_intr = find_max(item_list, data['uid'])
            if data['intr'] > max_intr:
                item_list[item_list_index] = [data['uid'], data['intr']]
    df = pd.DataFrame(columns=['uid', 'max_intr'], data=item_list)
    merge_data(df)


def max_pay_term():
    df = pd.read_csv('from_dm_v_tr_huanx_mx/max_pay_term.csv')
    merge_data(df)


def month_avg_huanx_amt():
    df_total = pd.read_csv('from_dm_v_tr_huanx_mx/monthly_sum_and_count_amt.csv')
    item_list = []
    for idx, data in df_total.iterrows():
        uid = data['uid']
        total_amt = 0
        for i in range(1, 12):
            total_amt += df_total.iloc[idx, i]
        avg_amt = total_amt / 11
        total_count = 0
        for i in range(12, 23):
            total_count += df_total.iloc[idx, i]
        avg_count = total_count / 11
        item_list.append([uid, avg_amt, avg_count])
    df = pd.DataFrame(columns=['uid', 'month_avg_huanx_amt', 'month_avg_huanx_count'], data=item_list)
    merge_data(df)


def month_avg_sbyb_amt():
    df_total = pd.read_csv('from_dm_v_tr_sbyb_mx/monthly_sum_and_count_sbyb_amt.csv')
    item_list = []
    for idx, data in df_total.iterrows():
        uid = data['uid']
        total_amt = 0
        for i in range(1, 15):
            total_amt += df_total.iloc[idx, i]
        avg_amt = total_amt / 14
        total_count = 0
        for i in range(15, 29):
            total_count += df_total.iloc[idx, i]
        avg_count = total_count / 14
        item_list.append([uid, avg_amt, avg_count])
    df = pd.DataFrame(columns=['uid', 'month_avg_sbyb_amt', 'month_avg_sbyb_count'], data=item_list)
    merge_data(df)


def month_avg_sdrq_amt():
    df_total = pd.read_csv('from_dm_v_tr_sdrq_mx/monthly_sum_and_count_sdrq_amt.csv')
    item_list = []
    for idx, data in df_total.iterrows():
        uid = data['uid']
        total_amt = 0
        for i in range(1, 15):
            total_amt += df_total.iloc[idx, i]
        avg_amt = total_amt / 14
        total_count = 0
        for i in range(15, 29):
            total_count += df_total.iloc[idx, i]
        avg_count = total_count / 14
        item_list.append([uid, avg_amt, avg_count])
    df = pd.DataFrame(columns=['uid', 'month_avg_sdrq_amt', 'month_avg_sdrq_count'], data=item_list)
    merge_data(df)


def month_avg_shop_amt():
    df_total = pd.read_csv('from_dm_v_tr_shop_mx/monthly_sum_and_count_shop_amt.csv')
    item_list = []
    for idx, data in df_total.iterrows():
        uid = data['uid']
        total_amt = 0
        for i in range(1, 12):
            total_amt += df_total.iloc[idx, i]
        avg_amt = total_amt / 11
        total_count = 0
        for i in range(12, 23):
            total_count += df_total.iloc[idx, i]
        avg_count = total_count / 11
        item_list.append([uid, avg_amt, avg_count])
    df = pd.DataFrame(columns=['uid', 'month_avg_shop_amt', 'month_avg_shop_count'], data=item_list)
    merge_data(df)


if __name__ == '__main__':
    # max_cac_intc_pr()
    # max_intr()
    # max_pay_term()
    # month_avg_huanx_amt()
    # month_avg_sbyb_amt()
    # month_avg_sdrq_amt()
    month_avg_shop_amt()
