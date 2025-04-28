# 智能数据工程：数据查询比较

## 项目概述

本项目旨在比较不同数据存储和查询方式对于Wikidata数据的处理效率与准确性。系统实现了三种查询方式：
1. 关系型数据库（MySQL）
2. 非关系型数据库（MongoDB，Linux环境下实现）
3. 大语言模型（LLM）查询

通过对不同查询方法的比较，探索各种方式在处理半结构化知识图谱数据时的优缺点，为不同应用场景下的数据查询方式选择提供参考。

## 功能特性

- 支持从Wikidata获取和处理不同类型的数据（城市、人物、大学等）
- 提供数据导入MySQL和MongoDB的脚本
- 实现三种查询方法的比较：MySQL查询、MongoDB查询、大语言模型查询
- 提供查询效率和结果准确性的比较分析

## 系统要求

- Python 3.8+
- MySQL 8.0+
- MongoDB 4.4+（可选，仅Linux环境下实现）
- 大语言模型API访问权限

## 安装与配置

1. 克隆项目仓库：
```bash
git clone <repository-url>
cd wikidata-query-comparison
```

2. 安装所需依赖：
```bash
pip install -r requirements.txt
```

3. 配置数据库连接：
   - 修改`query_comparison.py`中的MySQL配置信息
   - 若运行MongoDB部分，需配置MongoDB连接信息

4. 配置大语言模型API：
   - 在`query_comparison.py`中添加您的API密钥和API地址

## 使用方法

### 运行查询比较

```bash
python query_comparison.py
```

此命令将执行预定义的查询比较，包括城市人口查询、演员作品查询和大学信息查询，并输出比较结果。

### 自定义查询

可以通过修改`query_comparison.py`中的`queries`列表添加自定义查询。每个查询需要包含：
- name: 查询名称
- sql: SQL查询语句
- llm: 发送给大语言模型的提示

## 文件结构

- `query_comparison.py`: 主要比较脚本，执行MySQL与大语言模型查询比较
- `load_data_to_mongodb.py`: 加载数据到MongoDB的脚本（Linux环境）
- `mongodb_queries.py`: MongoDB查询实现（Linux环境）
- `requirements.txt`: 项目依赖列表

## 注意事项

- MongoDB部分实现于Linux环境下，不在当前Windows环境中运行
- 需要在运行前配置正确的数据库连接信息和API密钥
- 查询比较结果受网络延迟、数据库负载等因素影响

