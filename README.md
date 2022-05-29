# DataIntegration

这是南京大学软件学院 数据集成 课程迭代三的代码仓库

本阶段的工作是提取数据特征并进行分析。

## 本阶段核心工作资料汇总

**代码资源**：见本仓库

**特征提取与字段说明**：https://docs.qq.com/sheet/DVXFVdXZ3c1dEa0JR

**特征提取结果**：

**credit_level预测结果:** 访问链接查看，同时也可参见[credit_level_result.csv](./ml_predict/credit_level_result.csv)

**实验报告：**https://docs.qq.com/doc/DQ3lRV09Hem5EQWVW



## 项目结构

```
├─feature_extract 特征提取
│  ├─from_dm_v_tr_huanx_mx huanx_mx表
│  ├─from_dm_v_tr_sa_mx sa_mx表
│  ├─from_dm_v_tr_sbyb_mx sbyb_mx表
│  ├─from_dm_v_tr_sdrq_mx sdrq_mx表
│  ├─from_dm_v_tr_shop_mx shop_mx表
│  └─feature_extract01_05.ipynb djk_info djkfq_info contract_mxdjk_mx dsf_mx五张表的特征提取
├─log
│  └─highlevel
└─ml_predict 使用机器学习方案预测credit与star level
	└─credit_level_result.csv 预测结果
```

## 其他

