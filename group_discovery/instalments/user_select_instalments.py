import pandas as pd
from clickhouse_driver import Client
from collections import namedtuple
import csv



host = "192.168.1.101"
port = 9099
user = "sjjc"
password = "taosan506"
database = "dm"
send_receive_timeout = 10
client = Client(host=host, port=port, user=user, password=password, database=database,
                send_receive_timeout=send_receive_timeout)


# %%
def exec_eql_and_concat(data, sql, attr_list, default_na):
    # 执行sql
    data_list = client.execute(sql)
    # 转为df
    new_data_df = pd.DataFrame(columns=attr_list, data=data_list)
    # 按uid拼接
    new_data_df.set_index("uid", inplace=True)
    data1 = data.join(new_data_df, how='left', sort=False)
    # 补全空缺值
    data1.fillna(default_na, inplace=True)
    # 返回
    return data1

if __name__ == '__main__':
    # csv_data = pd.read_csv('result.csv', encoding='utf-8')
    # month_shop_times_sql = """select uid, count(*) as month_shop_avg from dm.dm_v_tr_shop_mx group by uid order by uid;
    # """
    # csv_data = exec_eql_and_concat(csv_data, month_shop_times_sql, ['uid', 'month_shop_avg'], {'month_shop_avg': 0.0})
    # csv_data.to_csv('data.csv', encoding='utf-8', index=False)
    list = []

    with open('data.csv') as f:
        f_csv = csv.reader(f)
        Row = namedtuple('Row', next(f_csv))
        for row in f_csv:
            row_info = Row(*row)
            point = 0
            if row_info.birthday > '19920101':
                point += 1
            if row_info.is_black == 1:
                point += 1
            if float(row_info.month_shop_avg) > 90:
                point += 1
            if float(row_info.tran_amt_gzdf) > 0:
                point += 1
            if float(row_info.tran_amt_gzdf) > 0 and float(row_info.tran_amt_gzdf) < 10000:
                point += 1
            if (float(row_info.djk_mx_sum) + float(row_info.djkfq_total_amt)) > (float(row_info.tran_amt_gzdf) / 12):
                point += 1

            if point >= 3:
                list.append(row_info)

    res = pd.DataFrame(list)
    res.to_csv('instalments.csv', encoding='utf-8', index=False)
    print(res.describe())
    print(len(list))



