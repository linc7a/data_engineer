#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import pymongo
from pymongo import MongoClient
from bson.son import SON
from pprint import pprint

# 连接到MongoDB
client = MongoClient('localhost', 27017)
db = client['db1']
s=time.time()
# 获取大学ID和名称的映射
university_names = {}
for university in db.universities.find():
    university_names[university['id']] = university['name']

# 创建管道进行聚合查询
pipeline = [
    # 筛选students属性
    {"$match": {"property": "students"}},
    # 按大学ID分组，取最大学生数量
    {"$group": {
        "_id": "$university_id",
        "students": {"$max": {"$toInt": "$value"}}
    }},
    # 按学生数量降序排序
    {"$sort": SON([("students", -1)])},
    # 只取前10条记录
    {"$limit": 10}
]

result = list(db.university_properties.aggregate(pipeline))

# 添加大学名称
for university in result:
    university['name'] = university_names.get(university['_id'], '未知大学')
e=time.time()
# 打印结果
print("\n中国最大的10所大学（按学生数量排序）：")
print("=" * 50)
print(f"{'排名':<5}{'大学名称':<25}{'学生数量':<10}")
print("-" * 50)

for i, university in enumerate(result, 1):
    print(f"{i:<5}{university['name']:<25}{university['students']:,}")

print("=" * 50) 
print(f"查询时间：{e-s}秒")