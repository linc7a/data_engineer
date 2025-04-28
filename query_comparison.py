import time
import json
import requests
from datetime import datetime
from config import mysql_config, llm_config

try:
    import mysql.connector
    from tabulate import tabulate
    MYSQL_AVAILABLE = True
except ImportError:
    MYSQL_AVAILABLE = False
    print("警告: MySQL连接器或tabulate模块未安装，MySQL查询功能将被禁用")
    
    def tabulate(data, headers, tablefmt="grid"):
        result = ""
        if not data:
            return result
        result += " | ".join(headers) + "\n"
        result += "-" * (sum(len(h) for h in headers) + 3 * (len(headers) - 1)) + "\n"
        for row in data:
            result += " | ".join(str(cell) for cell in row) + "\n"
        return result

def execute_sql_query(query):
    """执行SQL查询并返回结果"""
    if not MYSQL_AVAILABLE:
        return {
            'success': False,
            'error': "MySQL连接器未安装"
        }
    try:
        start_time = time.time()
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        column_names = [i[0] for i in cursor.description]
        cursor.close()
        conn.close()
        end_time = time.time()
        execution_time = end_time - start_time
        return {
            'success': True,
            'results': results,
            'column_names': column_names,
            'execution_time': execution_time,
            'row_count': len(results)
        }
    except Exception as err:
        return {
            'success': False,
            'error': str(err)
        }

def query_llm(prompt):
    """使用大语言模型进行查询"""
    try:
        start_time = time.time()
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {llm_config["api_key"]}'
        }
        data = {
            'model': llm_config['model_name'],
            'messages': [
                {'role': 'system', 'content': '你是一个知识图谱问答助手，请根据用户的问题提供准确的回答。'},
                {'role': 'user', 'content': prompt}
            ],
            'temperature': 0.7,
            'max_tokens': 1000
        }
        response = requests.post(
            llm_config['api_url'],
            headers=headers,
            json=data,
            timeout=30
        )
        if response.status_code != 200:
            return {
                'success': False,
                'error': f"API请求失败: {response.status_code} - {response.text}"
            }
        result = response.json()
        if 'choices' not in result or not result['choices']:
            return {
                'success': False,
                'error': "API响应格式错误"
            }
        answer = result['choices'][0]['message']['content']
        end_time = time.time()
        execution_time = end_time - start_time
        return {
            'success': True,
            'answer': answer,
            'execution_time': execution_time
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def format_mysql_results(result):
    if not result['success']:
        return f"查询失败: {result['error']}"
    if not result['results']:
        return "查询结果为空"
    return tabulate(
        result['results'],
        headers=result['column_names'],
        tablefmt="grid"
    )

def format_llm_results(result):
    if not result['success']:
        return f"查询失败: {result['error']}"
    return result['answer']

def compare_queries(query_name, sql_query, llm_prompt):
    print(f"\n=== {query_name} ===")
    print("\n--- SQL查询 ---")
    sql_result = execute_sql_query(sql_query)
    print(format_mysql_results(sql_result))
    if sql_result['success']:
        print(f"执行时间: {sql_result['execution_time']:.3f}秒")
        print(f"结果数量: {sql_result['row_count']}")
    print("\n--- 大语言模型查询 ---")
    llm_result = query_llm(llm_prompt)
    print(format_llm_results(llm_result))
    if llm_result['success']:
        print(f"执行时间: {llm_result['execution_time']:.3f}秒")
    print("\n" + "="*50)

def main():
    queries = [
        {
            'name': '中国城市人口查询',
            'sql': """
            SELECT c.name AS city_name, p.value AS population
            FROM cities c
            JOIN city_properties p ON c.id = p.city_id
            WHERE p.property = 'population'
            ORDER BY CAST(p.value AS UNSIGNED) DESC
            LIMIT 10;
            """,
            'llm': '请列出中国人口最多的10个城市及其人口数量。'
        },
        {
            'name': '中国著名演员查询',
            'sql': """
            SELECT p.name AS actor_name, GROUP_CONCAT(m.name SEPARATOR ', ') AS movies
            FROM people p
            JOIN movie_cast mc ON p.id = mc.cast_id
            JOIN movies m ON mc.movie_id = m.id
            GROUP BY p.id, p.name
            LIMIT 10;
            """,
            'llm': '请列出中国著名演员及其参演的电影。'
        },
        {
            'name': '中国大学查询',
            'sql': """
            SELECT u.name AS university_name, p.value AS students, l.name AS location
            FROM universities u
            JOIN university_properties p ON u.id = p.university_id
            LEFT JOIN university_location ul ON u.id = ul.university_id
            LEFT JOIN locations l ON ul.location_id = l.id
            WHERE p.property = 'students'
            ORDER BY CAST(p.value AS UNSIGNED) DESC
            LIMIT 10;
            """,
            'llm': '请列出中国著名大学及其学生数量和所在地。'
        }
    ]
    for query in queries:
        compare_queries(
            query['name'],
            query['sql'],
            query['llm']
        )

if __name__ == "__main__":
    main() 