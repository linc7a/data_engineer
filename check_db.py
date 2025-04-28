from pymongo import MongoClient

# 连接到本地 MongoDB
client = MongoClient('mongodb://localhost:27017/')

# 选择数据库
db = client['db1']

# 获取数据库统计信息
stats = db.command('dbstats')

# 打印结果
print("数据库统计信息:")
for key, value in stats.items():
    print(f"{key}: {value}")

# 列出所有集合
collections = db.list_collection_names()
print("\n集合列表:", collections)