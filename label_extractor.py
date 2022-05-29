#!/opt/anaconda3/bin/python
# -*- coding: UTF-8 -*-
"""
@Author: njuselhx
@Time: 2022/5/29 上午11:51
@File: label_extractor.py
@Software: PyCharm
"""
from clickhouse_driver import Client
import pandas as pd


def connect_db():
    host = '192.168.1.101'
    port = 9099
    user = 'sjjc'
    password = 'taosan506'
    database = 'dm'
    client = Client(host=host, port=port, user=user, password=password, database=database)
    return client


def find_max_pay_term(item_list, uid):
    index = -1
    max_pay_term = -1
    for idx, item in enumerate(item_list):
        if item[0] != uid:
            continue
        if max_pay_term < item[1]:
            index = idx
            max_pay_term = item[1]
    return index, max_pay_term


def from_dm_v_tr_huanx_mx(client):
    # 每个用户每笔还息交易利率
    sql = "select uid, intr from dm_v_tr_huanx_mx"
    df = pd.DataFrame(columns=['uid', 'intr'], data=client.execute(sql))
    df = df.drop_duplicates()
    df.reset_index(drop=True, inplace=True)
    df.to_csv('from_dm_v_tr_huanx_mx/intr.csv', index=False)
    # 每个用户每笔还息交易本金
    sql = "select uid, cac_intc_pr from dm_v_tr_huanx_mx"
    df = pd.DataFrame(columns=['uid', 'cac_intc_pr'], data=client.execute(sql))
    df = df.drop_duplicates()
    df.reset_index(drop=True, inplace=True)
    df.to_csv('from_dm_v_tr_huanx_mx/cac_intc_pr.csv', index=False)
    # 每个用户还息所遇到的最大期数
    sql = "select uid, pay_term from dm_v_tr_huanx_mx"
    df = pd.DataFrame(columns=['uid', 'pay_term'], data=client.execute(sql))
    df = df.drop_duplicates()
    df.reset_index(drop=True, inplace=True)
    uid_list = []
    item_list = []
    for idx, data in df.iterrows():
        if data['uid'] not in uid_list:
            uid_list.append(data['uid'])
            item_list.append([data['uid'], data['pay_term']])
        else:
            item_list_index, max_pay_term = find_max_pay_term(item_list, data['uid'])
            if data['pay_term'] > max_pay_term:
                item_list[item_list_index] = [data['uid'], data['pay_term']]
    df = pd.DataFrame(columns=['uid', 'pay_term'], data=item_list)
    df.to_csv('from_dm_v_tr_huanx_mx/max_pay_term.csv', index=False)


def monthly_sum_and_count_amt(client):
    # 每个用户每月还息次数和总额
    sql = "select distinct uid from dm_v_tr_huanx_mx"
    df = pd.DataFrame(columns=['uid'], data=client.execute(sql))
    # 一个item_list的元素是一个长度为23的列表，分别为uid, 1-11月还息总数额，1-11月还息次数
    item_list = []
    for idx, data in df.iterrows():
        item_list.append([data['uid']] + [0] * 22)
    for idx, data in df.iterrows():
        sql = "select tran_date, tran_amt from dm_v_tr_huanx_mx where uid = '" + item_list[idx][0] + "'"
        df_in_uid = pd.DataFrame(columns=['tran_date', 'tran_amt'], data=client.execute(sql))
        for idx_in_data, data_in_uid in df_in_uid.iterrows():
            month = int(data_in_uid['tran_date'][4:6])
            item_list[idx][month] += data_in_uid['tran_amt']
            item_list[idx][month + 11] += 1
    df = pd.DataFrame(columns=['uid', 'sum_amt_1', 'sum_amt_2', 'sum_amt_3', 'sum_amt_4',
                               'sum_amt_5', 'sum_amt_6', 'sum_amt_7', 'sum_amt_8',
                               'sum_amt_9', 'sum_amt_10', 'sum_amt_11', 'count_amt_1',
                               'count_amt_2', 'count_amt_3', 'count_amt_4', 'count_amt_5',
                               'count_amt_6', 'count_amt_7', 'count_amt_8', 'count_amt_9',
                               'count_amt_10', 'count_amt_11'], data=item_list)
    df.to_csv('from_dm_v_tr_huanx_mx/monthly_sum_and_count_amt.csv', index=False)


def monthly_sum_and_count_cr_and_dr_amt(client):
    # 每个用户每月活期借入和借出总额
    sql = "select distinct uid from dm_v_tr_huanx_mx"
    df = pd.DataFrame(columns=['uid'], data=client.execute(sql))
    # 一个item_list的元素是一个长度为57的列表，分别为uid, 1-14月作为贷方总数额、次数，1-14月作为借方总数额、次数
    item_list = []
    for idx, data in df.iterrows():
        item_list.append([data['uid']] + [0] * 56)
    for idx, data in df.iterrows():
        sql = "select cr_amt, tran_amt, dr_amt, tran_date from dm_v_tr_sa_mx where uid = '" + item_list[idx][0] + "'"
        df_in_uid = pd.DataFrame(columns=['cr_amt', 'tran_amt', 'dr_amt', 'tran_date'], data=client.execute(sql))
        for idx_in_data, data_in_uid in df_in_uid.iterrows():
            month = int(data_in_uid['tran_date'][4:6])
            if data_in_uid['tran_date'][3] == '2':
                month += 12
            if month > 14:
                continue
            # 说明是贷方
            if data_in_uid['cr_amt'] > 0:
                item_list[idx][month] += data_in_uid['tran_amt']
                item_list[idx][month + 14] += 1
            # 说明是借方
            else:
                item_list[idx][month + 28] += data_in_uid['tran_amt']
                item_list[idx][month + 42] += 1
    df = pd.DataFrame(columns=['uid', 'sum_cr_amt_1', 'sum_cr_amt__2', 'sum_cr_amt_3', 'sum_cr_amt_4',
                               'sum_cr_amt_5', 'sum_cr_amt_6', 'sum_cr_amt_7', 'sum_cr_amt_8',
                               'sum_cr_amt_9', 'sum_cr_amt_10', 'sum_cr_amt_11', 'sum_cr_amt_12',
                               'sum_cr_amt_13', 'sum_cr_amt_14', 'count_cr_amt_1', 'count_cr_amt_2',
                               'count_cr_amt_3', 'count_cr_amt_4', 'count_cr_amt_5', 'count_cr_amt_6',
                               'count_cr_amt_7', 'count_cr_amt_8', 'count_cr_amt_9', 'count_cr_amt_10',
                               'count_cr_amt_11', 'count_cr_amt_12', 'count_cr_amt_13', 'count_cr_amt_14',
                               'sum_dr_amt_1', 'sum_dr_amt_2', 'sum_dr_amt_3', 'sum_dr_amt_4',
                               'sum_dr_amt_5', 'sum_dr_amt_6', 'sum_dr_amt_7', 'sum_dr_amt_8',
                               'sum_dr_amt_9', 'sum_dr_amt_10', 'sum_dr_amt_11', 'sum_dr_amt_12',
                               'sum_dr_amt_13', 'sum_dr_amt_14', 'count_dr_amt_1', 'count_dr_amt_2',
                               'count_dr_amt_3', 'count_dr_amt_4', 'count_dr_amt_5', 'count_dr_amt_6',
                               'count_dr_amt_7', 'count_dr_amt_8', 'count_dr_amt_9', 'count_dr_amt_10',
                               'count_dr_amt_11', 'count_dr_amt_12', 'count_dr_amt_13', 'count_dr_amt_14'],
                      data=item_list)
    df.to_csv('from_dm_v_tr_sa_mx/monthly_sum_and_count_cr_and_dr_amt.csv', index=False)


def sbyb_amt_fen(client):
    sql = "select distinct uid from dm_v_tr_sbyb_mx"
    df = pd.DataFrame(columns=['uid'], data=client.execute(sql))
    # 一个item_list的元素是一个长度为29的列表，分别为uid, 1-14月医保社保交易数额、次数
    item_list = []
    for idx, data in df.iterrows():
        item_list.append([data['uid']] + [0] * 28)
    for idx, data in df.iterrows():
        sql = "select tran_date, tran_amt_fen from dm_v_tr_sbyb_mx where uid = '" + item_list[idx][0] + "'"
        df_in_uid = pd.DataFrame(columns=['tran_date', 'tran_amt_fen'], data=client.execute(sql))
        for idx_in_data, data_in_uid in df_in_uid.iterrows():
            month = int(data_in_uid['tran_date'][4:6])
            if data_in_uid['tran_date'][3] == '2':
                month += 12
            if month > 14:
                continue
            item_list[idx][month] += data_in_uid['tran_amt_fen']
            item_list[idx][month + 14] += 1
    df = pd.DataFrame(columns=['uid', 'sum_sbyb_amt_1', 'sum_sbyb_amt_2', 'sum_sbyb_amt_3', 'sum_sbyb_amt_4',
                               'sum_sbyb_amt_5', 'sum_sbyb_amt_6', 'sum_sbyb_amt_7', 'sum_sbyb_amt_8',
                               'sum_sbyb_amt_9', 'sum_sbyb_amt_10', 'sum_sbyb_amt_11', 'sum_sbyb_amt_12',
                               'sum_sbyb_amt_13', 'sum_sbyb_amt_14', 'count_sbyb_amt_1', 'count_sbyb_amt_2',
                               'count_sbyb_amt_3', 'count_sbyb_amt_4', 'count_sbyb_amt_5', 'count_sbyb_amt_6',
                               'count_sbyb_amt_7', 'count_sbyb_amt_8', 'count_sbyb_amt_9', 'count_sbyb_amt_10',
                               'count_sbyb_amt_11', 'count_sbyb_amt_12', 'count_sbyb_amt_13', 'count_sbyb_amt_14'],
                      data=item_list)
    df.to_csv('from_dm_v_tr_sbyb_mx/monthly_sum_and_count_sbyb_amt.csv', index=False)


def sdrq_amt_fen(client):
    sql = "select distinct uid from dm_v_tr_sdrq_mx"
    df = pd.DataFrame(columns=['uid'], data=client.execute(sql))
    # 一个item_list的元素是一个长度为29的列表，分别为uid, 1-14月医保社保交易数额、次数
    item_list = []
    for idx, data in df.iterrows():
        item_list.append([data['uid']] + [0] * 28)
    for idx, data in df.iterrows():
        sql = "select tran_date, tran_amt_fen from dm_v_tr_sdrq_mx where uid = '" + item_list[idx][0] + "'"
        df_in_uid = pd.DataFrame(columns=['tran_date', 'tran_amt_fen'], data=client.execute(sql))
        for idx_in_data, data_in_uid in df_in_uid.iterrows():
            month = int(data_in_uid['tran_date'][4:6])
            if data_in_uid['tran_date'][3] == '2':
                month += 12
            if month > 14:
                continue
            item_list[idx][month] += data_in_uid['tran_amt_fen']
            item_list[idx][month + 14] += 1
    df = pd.DataFrame(columns=['uid', 'sum_sdrq_amt_1', 'sum_sdrq_amt_2', 'sum_sdrq_amt_3', 'sum_sdrq_amt_4',
                               'sum_sdrq_amt_5', 'sum_sdrq_amt_6', 'sum_sdrq_amt_7', 'sum_sdrq_amt_8',
                               'sum_sdrq_amt_9', 'sum_sdrq_amt_10', 'sum_sdrq_amt_11', 'sum_sdrq_amt_12',
                               'sum_sdrq_amt_13', 'sum_sdrq_amt_14', 'count_sdrq_amt_1', 'count_sdrq_amt_2',
                               'count_sdrq_amt_3', 'count_sdrq_amt_4', 'count_sdrq_amt_5', 'count_sdrq_amt_6',
                               'count_sdrq_amt_7', 'count_sdrq_amt_8', 'count_sdrq_amt_9', 'count_sdrq_amt_10',
                               'count_sdrq_amt_11', 'count_sdrq_amt_12', 'count_sdrq_amt_13', 'count_sdrq_amt_14'],
                      data=item_list)
    df.to_csv('from_dm_v_tr_sdrq_mx/monthly_sum_and_count_sdrq_amt.csv', index=False)


def shop_amt(client):
    sql = "select distinct uid from dm_v_tr_shop_mx"
    df = pd.DataFrame(columns=['uid'], data=client.execute(sql))
    # 一个item_list的元素是一个长度为23的列表，分别为uid, 1-11月还息商户交易额，1-11月商户交易次数
    item_list = []
    for idx, data in df.iterrows():
        item_list.append([data['uid']] + [0] * 22)
    for idx, data in df.iterrows():
        sql = "select tran_date, tran_amt from dm_v_tr_shop_mx where uid = '" + item_list[idx][0] + "'"
        df_in_uid = pd.DataFrame(columns=['tran_date', 'tran_amt'], data=client.execute(sql))
        for idx_in_data, data_in_uid in df_in_uid.iterrows():
            month = int(data_in_uid['tran_date'][5:7])
            if month == 12:
                continue
            item_list[idx][month] += data_in_uid['tran_amt']
            item_list[idx][month + 11] += 1
    df = pd.DataFrame(columns=['uid', 'sum_shop_amt_1', 'sum_shop_amt_2', 'sum_shop_amt_3', 'sum_shop_amt_4',
                               'sum_shop_amt_5', 'sum_shop_amt_6', 'sum_shop_amt_7', 'sum_shop_amt_8',
                               'sum_shop_amt_9', 'sum_shop_amt_10', 'sum_shop_amt_11', 'count_shop_amt_1',
                               'count_shop_amt_2', 'count_shop_amt_3', 'count_shop_amt_4', 'count_shop_amt_5',
                               'count_shop_amt_6', 'count_shop_amt_7', 'count_shop_amt_8', 'count_shop_amt_9',
                               'count_shop_amt_10', 'count_shop_amt_11'], data=item_list)
    df.to_csv('from_dm_v_tr_shop_mx/monthly_sum_and_count_shop_amt.csv', index=False)


if __name__ == '__main__':
    ch_client = connect_db()
    # from_dm_v_tr_huanx_mx(ch_client)
    # monthly_sum_and_count_amt(ch_client)
    # monthly_sum_and_count_cr_and_dr_amt(ch_client)
    # sdrq_amt_fen(ch_client)
    shop_amt(ch_client)
