import mysql.connector
import json
import os
from tqdm import tqdm

# MySQL连接配置
config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'de_work',
    'password': 'data_engneer',
    'database': 'dataengineer'
}

def load_json_data(file_path):
    """从JSON文件加载数据"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"文件不存在: {file_path}")
        return []
    except json.JSONDecodeError:
        print(f"JSON解析错误: {file_path}")
        return []

def insert_cities(cursor, data):
    """插入城市数据"""
    if not data:
        return 0
    
    sql = "INSERT IGNORE INTO cities (id, name) VALUES (%s, %s)"
    values = [(item['id'], item['name']) for item in data]
    
    cursor.executemany(sql, values)
    return cursor.rowcount

def insert_city_properties(cursor, data):
    """插入城市属性数据"""
    if not data:
        return 0
    
    sql = "INSERT IGNORE INTO city_properties (city_id, property, value) VALUES (%s, %s, %s)"
    values = [(item['city_id'], item['property'], item['value']) for item in data]
    
    cursor.executemany(sql, values)
    return cursor.rowcount

def insert_people(cursor, data):
    """插入人物数据"""
    if not data:
        return 0
    
    sql = "INSERT IGNORE INTO people (id, name) VALUES (%s, %s)"
    values = [(item['id'], item['name']) for item in data]
    
    cursor.executemany(sql, values)
    return cursor.rowcount

def insert_people_properties(cursor, data):
    """插入人物属性数据"""
    if not data:
        return 0
    
    sql = "INSERT IGNORE INTO people_properties (person_id, property, value) VALUES (%s, %s, %s)"
    values = [(item['person_id'], item['property'], item['value']) for item in data]
    
    cursor.executemany(sql, values)
    return cursor.rowcount

def insert_occupations(cursor, data):
    """插入职业数据"""
    if not data:
        return 0
    
    sql = "INSERT IGNORE INTO occupations (id, name) VALUES (%s, %s)"
    values = [(item['id'], item['name']) for item in data]
    
    cursor.executemany(sql, values)
    return cursor.rowcount

def insert_awards(cursor, data):
    """插入奖项数据"""
    if not data:
        return 0
    
    sql = "INSERT IGNORE INTO awards (id, name) VALUES (%s, %s)"
    values = [(item['id'], item['name']) for item in data]
    
    cursor.executemany(sql, values)
    return cursor.rowcount

def insert_person_occupation(cursor, data):
    """插入人物-职业关系数据"""
    if not data:
        return 0
    
    sql = "INSERT IGNORE INTO person_occupation (person_id, occupation_id) VALUES (%s, %s)"
    values = [(item['person_id'], item['occupation_id']) for item in data]
    
    cursor.executemany(sql, values)
    return cursor.rowcount

def insert_person_award(cursor, data):
    """插入人物-奖项关系数据"""
    if not data:
        return 0
    
    sql = "INSERT IGNORE INTO person_award (person_id, award_id) VALUES (%s, %s)"
    values = [(item['person_id'], item['award_id']) for item in data]
    
    cursor.executemany(sql, values)
    return cursor.rowcount

def insert_universities(cursor, data):
    """插入大学数据"""
    if not data:
        return 0
    
    sql = "INSERT IGNORE INTO universities (id, name) VALUES (%s, %s)"
    values = [(item['id'], item['name']) for item in data]
    
    cursor.executemany(sql, values)
    return cursor.rowcount

def insert_university_properties(cursor, data):
    """插入大学属性数据"""
    if not data:
        return 0
    
    sql = "INSERT IGNORE INTO university_properties (university_id, property, value) VALUES (%s, %s, %s)"
    values = [(item['university_id'], item['property'], item['value']) for item in data]
    
    cursor.executemany(sql, values)
    return cursor.rowcount

def insert_locations(cursor, data):
    """插入位置数据"""
    if not data:
        return 0
    
    sql = "INSERT IGNORE INTO locations (id, name) VALUES (%s, %s)"
    values = [(item['id'], item['name']) for item in data]
    
    cursor.executemany(sql, values)
    return cursor.rowcount

def insert_university_location(cursor, data):
    """插入大学-位置关系数据"""
    if not data:
        return 0
    
    sql = "INSERT IGNORE INTO university_location (university_id, location_id) VALUES (%s, %s)"
    values = [(item['university_id'], item['location_id']) for item in data]
    
    cursor.executemany(sql, values)
    return cursor.rowcount

def insert_movies(cursor, data):
    """插入电影数据"""
    if not data:
        return 0
    
    sql = "INSERT IGNORE INTO movies (id, name) VALUES (%s, %s)"
    values = [(item['id'], item['name']) for item in data]
    
    cursor.executemany(sql, values)
    return cursor.rowcount

def insert_movie_properties(cursor, data):
    """插入电影属性数据"""
    if not data:
        return 0
    
    sql = "INSERT IGNORE INTO movie_properties (movie_id, property, value) VALUES (%s, %s, %s)"
    values = [(item['movie_id'], item['property'], item['value']) for item in data]
    
    cursor.executemany(sql, values)
    return cursor.rowcount

def insert_directors(cursor, data):
    """插入导演数据"""
    if not data:
        return 0
    
    sql = "INSERT IGNORE INTO directors (id, name) VALUES (%s, %s)"
    values = [(item['id'], item['name']) for item in data]
    
    cursor.executemany(sql, values)
    return cursor.rowcount

def insert_genres(cursor, data):
    """插入电影类型数据"""
    if not data:
        return 0
    
    sql = "INSERT IGNORE INTO genres (id, name) VALUES (%s, %s)"
    values = [(item['id'], item['name']) for item in data]
    
    cursor.executemany(sql, values)
    return cursor.rowcount

def insert_casts(cursor, data):
    """插入演员数据"""
    if not data:
        return 0
    
    sql = "INSERT IGNORE INTO casts (id, name) VALUES (%s, %s)"
    values = [(item['id'], item['name']) for item in data]
    
    cursor.executemany(sql, values)
    return cursor.rowcount

def insert_movie_director(cursor, data):
    """插入电影-导演关系数据"""
    if not data:
        return 0
    
    sql = "INSERT IGNORE INTO movie_director (movie_id, director_id) VALUES (%s, %s)"
    values = [(item['movie_id'], item['director_id']) for item in data]
    
    cursor.executemany(sql, values)
    return cursor.rowcount

def insert_movie_genre(cursor, data):
    """插入电影-类型关系数据"""
    if not data:
        return 0
    
    sql = "INSERT IGNORE INTO movie_genre (movie_id, genre_id) VALUES (%s, %s)"
    values = [(item['movie_id'], item['genre_id']) for item in data]
    
    cursor.executemany(sql, values)
    return cursor.rowcount

def insert_movie_cast(cursor, data):
    """插入电影-演员关系数据"""
    if not data:
        return 0
    
    sql = "INSERT IGNORE INTO movie_cast (movie_id, cast_id) VALUES (%s, %s)"
    values = [(item['movie_id'], item['cast_id']) for item in data]
    
    cursor.executemany(sql, values)
    return cursor.rowcount

def main():
    processed_dir = 'processed_data'
    
    try:
        # 连接到MySQL
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        
        print("成功连接到MySQL")
        
        # 加载和插入城市相关数据
        print("\n加载城市数据...")
        cities_data = load_json_data(os.path.join(processed_dir, 'cities.json'))
        city_props_data = load_json_data(os.path.join(processed_dir, 'city_properties.json'))
        
        print(f"插入城市数据 ({len(cities_data)} 条记录)...")
        cities_inserted = insert_cities(cursor, cities_data)
        print(f"插入城市属性数据 ({len(city_props_data)} 条记录)...")
        city_props_inserted = insert_city_properties(cursor, city_props_data)
        
        # 加载和插入人物相关数据
        print("\n加载人物数据...")
        people_data = load_json_data(os.path.join(processed_dir, 'people.json'))
        people_props_data = load_json_data(os.path.join(processed_dir, 'people_properties.json'))
        occupations_data = load_json_data(os.path.join(processed_dir, 'occupations.json'))
        awards_data = load_json_data(os.path.join(processed_dir, 'awards.json'))
        person_occupation_data = load_json_data(os.path.join(processed_dir, 'person_occupation.json'))
        person_award_data = load_json_data(os.path.join(processed_dir, 'person_award.json'))
        
        print(f"插入人物数据 ({len(people_data)} 条记录)...")
        people_inserted = insert_people(cursor, people_data)
        print(f"插入人物属性数据 ({len(people_props_data)} 条记录)...")
        people_props_inserted = insert_people_properties(cursor, people_props_data)
        print(f"插入职业数据 ({len(occupations_data)} 条记录)...")
        occupations_inserted = insert_occupations(cursor, occupations_data)
        print(f"插入奖项数据 ({len(awards_data)} 条记录)...")
        awards_inserted = insert_awards(cursor, awards_data)
        print(f"插入人物-职业关系数据 ({len(person_occupation_data)} 条记录)...")
        person_occupation_inserted = insert_person_occupation(cursor, person_occupation_data)
        print(f"插入人物-奖项关系数据 ({len(person_award_data)} 条记录)...")
        person_award_inserted = insert_person_award(cursor, person_award_data)
        
        # 加载和插入大学相关数据
        print("\n加载大学数据...")
        universities_data = load_json_data(os.path.join(processed_dir, 'universities.json'))
        university_props_data = load_json_data(os.path.join(processed_dir, 'university_properties.json'))
        locations_data = load_json_data(os.path.join(processed_dir, 'locations.json'))
        university_location_data = load_json_data(os.path.join(processed_dir, 'university_location.json'))
        
        print(f"插入大学数据 ({len(universities_data)} 条记录)...")
        universities_inserted = insert_universities(cursor, universities_data)
        print(f"插入大学属性数据 ({len(university_props_data)} 条记录)...")
        university_props_inserted = insert_university_properties(cursor, university_props_data)
        print(f"插入位置数据 ({len(locations_data)} 条记录)...")
        locations_inserted = insert_locations(cursor, locations_data)
        print(f"插入大学-位置关系数据 ({len(university_location_data)} 条记录)...")
        university_location_inserted = insert_university_location(cursor, university_location_data)
        
        # 加载和插入电影相关数据
        print("\n加载电影数据...")
        movies_data = load_json_data(os.path.join(processed_dir, 'movies.json'))
        movie_props_data = load_json_data(os.path.join(processed_dir, 'movie_properties.json'))
        directors_data = load_json_data(os.path.join(processed_dir, 'directors.json'))
        genres_data = load_json_data(os.path.join(processed_dir, 'genres.json'))
        casts_data = load_json_data(os.path.join(processed_dir, 'casts.json'))
        movie_director_data = load_json_data(os.path.join(processed_dir, 'movie_director.json'))
        movie_genre_data = load_json_data(os.path.join(processed_dir, 'movie_genre.json'))
        movie_cast_data = load_json_data(os.path.join(processed_dir, 'movie_cast.json'))
        
        print(f"插入电影数据 ({len(movies_data)} 条记录)...")
        movies_inserted = insert_movies(cursor, movies_data)
        print(f"插入电影属性数据 ({len(movie_props_data)} 条记录)...")
        movie_props_inserted = insert_movie_properties(cursor, movie_props_data)
        print(f"插入导演数据 ({len(directors_data)} 条记录)...")
        directors_inserted = insert_directors(cursor, directors_data)
        print(f"插入电影类型数据 ({len(genres_data)} 条记录)...")
        genres_inserted = insert_genres(cursor, genres_data)
        print(f"插入演员数据 ({len(casts_data)} 条记录)...")
        casts_inserted = insert_casts(cursor, casts_data)
        print(f"插入电影-导演关系数据 ({len(movie_director_data)} 条记录)...")
        movie_director_inserted = insert_movie_director(cursor, movie_director_data)
        print(f"插入电影-类型关系数据 ({len(movie_genre_data)} 条记录)...")
        movie_genre_inserted = insert_movie_genre(cursor, movie_genre_data)
        print(f"插入电影-演员关系数据 ({len(movie_cast_data)} 条记录)...")
        movie_cast_inserted = insert_movie_cast(cursor, movie_cast_data)
        
        # 提交事务并关闭连接
        conn.commit()
        cursor.close()
        conn.close()
        print("\n所有数据成功导入到MySQL!")
        
    except mysql.connector.Error as err:
        print(f"MySQL错误: {err}")
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    main() 