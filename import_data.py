#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import pymongo
from pymongo import MongoClient

# 连接到MongoDB
client = MongoClient('localhost', 27017)
db = client['db1']

# 指定数据目录
data_dir = '/mnt/d/Project/PythonProject/关系数据库/processed_data'

# 遍历目录中的所有文件
for filename in os.listdir(data_dir):
    if filename.endswith('.json'):
        collection_name = os.path.splitext(filename)[0]
        file_path = os.path.join(data_dir, filename)
        
        print(f"正在导入 {filename} 到集合 {collection_name}...")
        
        # 读取JSON文件
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # 如果集合已存在，先删除
        if collection_name in db.list_collection_names():
            db[collection_name].drop()
        
        # 插入数据
        if data:  # 确保数据不为空
            db[collection_name].insert_many(data)
            print(f"已成功导入 {len(data)} 条记录到 {collection_name}")
        else:
            print(f"警告: {filename} 中没有数据")

print("所有数据导入完成!") 