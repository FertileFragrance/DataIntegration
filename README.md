# DataIntegration

这是南京大学软件学院 数据集成 课程迭代三的代码仓库

本阶段的工作是提取数据特征并进行分析。

## 本阶段核心工作资料汇总

**代码资源**：见本仓库

**特征提取与字段说明**：https://docs.qq.com/sheet/DVXFVdXZ3c1dEa0JR

**特征提取结果**：https://just-cotested.oss-cn-shanghai.aliyuncs.com/file/result.csv

**credit_level预测结果:** 访问[链接](https://just-cotested.oss-cn-shanghai.aliyuncs.com/file/credit_level_result.csv)查看，同时也可参见[credit_level_result.csv](./ml_predict/credit_level_result.csv)

**实验报告：**https://docs.qq.com/doc/DQ3lRV09Hem5EQWVW

注：Moodle提交上提交文档的预测结果和特征提取结果链接有误，请以本文档以上链接为准，带来不便非常抱歉。

## 项目结构

```
├─feature_extract 特征提取
│  ├─from_dm_v_tr_huanx_mx huanx_mx表
│  ├─from_dm_v_tr_sa_mx sa_mx表
│  ├─from_dm_v_tr_sbyb_mx sbyb_mx表
│  ├─from_dm_v_tr_sdrq_mx sdrq_mx表
│  ├─from_dm_v_tr_shop_mx shop_mx表
│  └─feature_extract01_05.ipynb djk_info djkfq_info contract_mxdjk_mx dsf_mx五张表的特征提取
│
├─group_discovery 
│
├─log
│  └─high_level
└─ml_predict 使用机器学习方案预测credit与star level
	└─credit_level_result.csv 预测结果
```

```txt
├── feature_extract                 特征提取
│   ├── feature_extract01_05.ipynb  djk_info djkfq_info contract_mxdjk_mx dsf_mx五张表的特征提取
│   ├── feature_extract11_15.py     对11-15的5张表做特征提取
│   ├── from_dm_v_tr_huanx_mx       huanx_mx表
│   ├── from_dm_v_tr_sa_mx          sa_mx表
│   ├── from_dm_v_tr_sbyb_mx        sbyb_mx表
│   ├── from_dm_v_tr_sdrq_mx        sdrq_mx表
│   ├── from_dm_v_tr_shop_mx        shop_mx表
│   └── integration11_15.py         整合11-15张表的特征到标签
├── group_discovery                 发现不同的客户群体
│   ├── high_level_crowd.py         筛选高端资产客户
│   └── high_level.csv              高端资产客户结果表
├── log
│   └── high_level                  高端资产客户个人情况分布
├── ml_predict                      使用机器学习方案预测credit与star level
│   └── credit_level_result.csv     预测结果
├── README.md
└── uid_list.csv                    初始含有所有uid的表
```
