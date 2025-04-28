import requests
import json
import time
import os

def get_wikidata_items(query, limit=300):
    """
    使用SPARQL查询从Wikidata获取数据
    """
    url = "https://query.wikidata.org/sparql"
    headers = {
        'User-Agent': 'Wikidata-Example-Python/1.0',
        'Accept': 'application/json'
    }
    params = {
        'query': query,
        'format': 'json'
    }
    
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"查询失败: {response.status_code}")
        print(response.text)
        return None

def save_to_json(data, filename):
    """保存数据到JSON文件"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"数据已保存到 {filename}")

# 定义我们想要获取的几个不同领域的中文数据
# 1. 中国的城市
def get_chinese_cities():
    query = """
    SELECT ?city ?cityLabel ?population ?area ?latitude ?longitude ?inception WHERE {
      ?city wdt:P31/wdt:P279* wd:Q515 .  # 实例为城市
      ?city wdt:P17 wd:Q148 .           # 位于中国
      OPTIONAL { ?city wdt:P1082 ?population . }  # 人口
      OPTIONAL { ?city wdt:P2046 ?area . }        # 面积
      OPTIONAL { ?city wdt:P625 ?coordinates . }  # 坐标
      OPTIONAL { 
        ?city p:P625 ?coord .
        ?coord psv:P625 ?coord_node .
        ?coord_node wikibase:geoLatitude ?latitude .
        ?coord_node wikibase:geoLongitude ?longitude .
      }
      OPTIONAL { ?city wdt:P571 ?inception . }    # 成立日期
      SERVICE wikibase:label { bd:serviceParam wikibase:language "zh" . }
    }
    LIMIT 300
    """
    return get_wikidata_items(query)

# 2. 中国的著名人物
def get_chinese_famous_people():
    query = """
    SELECT ?person ?personLabel ?birth ?death ?occupation ?occupationLabel ?award ?awardLabel WHERE {
      ?person wdt:P27 wd:Q148 .         # 国籍为中国
      ?person wdt:P31 wd:Q5 .           # 实例为人
      OPTIONAL { ?person wdt:P569 ?birth . }      # 出生日期
      OPTIONAL { ?person wdt:P570 ?death . }      # 死亡日期
      OPTIONAL { 
        ?person wdt:P106 ?occupation .            # 职业
        ?occupation rdfs:label ?occupationLabel filter (lang(?occupationLabel) = "zh").
      }
      OPTIONAL { 
        ?person wdt:P166 ?award .                 # 奖项
        ?award rdfs:label ?awardLabel filter (lang(?awardLabel) = "zh").
      }
      SERVICE wikibase:label { bd:serviceParam wikibase:language "zh" . }
    }
    LIMIT 300
    """
    return get_wikidata_items(query)

# 3. 中国的高等教育机构
def get_chinese_universities():
    query = """
    SELECT ?university ?universityLabel ?inception ?location ?locationLabel ?students ?website WHERE {
      ?university wdt:P31/wdt:P279* wd:Q3918 .  # 实例为大学
      ?university wdt:P17 wd:Q148 .            # 位于中国
      OPTIONAL { ?university wdt:P571 ?inception . }     # 成立日期
      OPTIONAL { 
        ?university wdt:P276 ?location .               # 位置
        ?location rdfs:label ?locationLabel filter (lang(?locationLabel) = "zh").
      }
      OPTIONAL { ?university wdt:P2196 ?students . }    # 学生数量
      OPTIONAL { ?university wdt:P856 ?website . }      # 网站
      SERVICE wikibase:label { bd:serviceParam wikibase:language "zh" . }
    }
    LIMIT 300
    """
    return get_wikidata_items(query)

# 4. 中国的电影作品
def get_chinese_movies():
    query = """
    SELECT ?movie ?movieLabel ?director ?directorLabel ?releaseDate ?genre ?genreLabel ?cast ?castLabel WHERE {
      ?movie wdt:P31/wdt:P279* wd:Q11424 .  # 实例为电影
      ?movie wdt:P495 wd:Q148 .            # 制作国为中国
      OPTIONAL { 
        ?movie wdt:P57 ?director .          # 导演
        ?director rdfs:label ?directorLabel filter (lang(?directorLabel) = "zh").
      }
      OPTIONAL { ?movie wdt:P577 ?releaseDate . }  # 发行日期
      OPTIONAL { 
        ?movie wdt:P136 ?genre .            # 类型
        ?genre rdfs:label ?genreLabel filter (lang(?genreLabel) = "zh").
      }
      OPTIONAL { 
        ?movie wdt:P161 ?cast .             # 演员
        ?cast rdfs:label ?castLabel filter (lang(?castLabel) = "zh").
      }
      SERVICE wikibase:label { bd:serviceParam wikibase:language "zh" . }
    }
    LIMIT 300
    """
    return get_wikidata_items(query)

# 主函数
def main():
    # 创建数据目录
    if not os.path.exists('data'):
        os.makedirs('data')
    
    # 获取并保存中国城市数据
    print("正在获取中国城市数据...")
    cities_data = get_chinese_cities()
    if cities_data:
        save_to_json(cities_data, 'data/chinese_cities.json')
    time.sleep(1)  # 避免过快发送请求
    
    # 获取并保存中国著名人物数据
    print("正在获取中国著名人物数据...")
    people_data = get_chinese_famous_people()
    if people_data:
        save_to_json(people_data, 'data/chinese_people.json')
    time.sleep(1)
    
    # 获取并保存中国大学数据
    print("正在获取中国大学数据...")
    universities_data = get_chinese_universities()
    if universities_data:
        save_to_json(universities_data, 'data/chinese_universities.json')
    time.sleep(1)
    
    # 获取并保存中国电影数据
    print("正在获取中国电影数据...")
    movies_data = get_chinese_movies()
    if movies_data:
        save_to_json(movies_data, 'data/chinese_movies.json')
    
    print("所有数据获取完成！")

if __name__ == "__main__":
    main() 