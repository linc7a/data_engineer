import json
import os
import re
from datetime import datetime

def clean_value(value):
    """清理和标准化数据值"""
    if isinstance(value, str):
        # 移除URL中的部分
        value = re.sub(r'http://www\.wikidata\.org/entity/', '', value)
        # 移除时间字符串中的时区信息
        value = re.sub(r'T00:00:00Z', '', value)
    return value

def extract_id_from_uri(uri):
    """从URI中提取实体ID"""
    if not uri:
        return None
    match = re.search(r'Q\d+$', uri)
    if match:
        return match.group(0)
    return uri

def process_cities_data(input_file, output_dir):
    """处理城市数据"""
    # 读取JSON数据
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 提取绑定
    bindings = data.get('results', {}).get('bindings', [])
    
    # 准备实体和关系数据
    cities = []
    city_properties = []
    
    for item in bindings:
        city_id = extract_id_from_uri(item.get('city', {}).get('value', ''))
        if not city_id:
            continue
            
        city_name = item.get('cityLabel', {}).get('value', '')
        
        # 添加城市实体
        cities.append({
            'id': city_id,
            'name': city_name
        })
        
        # 处理人口数据
        if 'population' in item:
            population = item['population'].get('value', '')
            city_properties.append({
                'city_id': city_id,
                'property': 'population',
                'value': population
            })
        
        # 处理面积数据
        if 'area' in item:
            area = item['area'].get('value', '')
            city_properties.append({
                'city_id': city_id,
                'property': 'area',
                'value': area
            })
            
        # 处理经纬度数据
        if 'latitude' in item and 'longitude' in item:
            latitude = item['latitude'].get('value', '')
            longitude = item['longitude'].get('value', '')
            city_properties.append({
                'city_id': city_id,
                'property': 'coordinates',
                'value': f"{latitude},{longitude}"
            })
            
        # 处理成立日期数据
        if 'inception' in item:
            inception = clean_value(item['inception'].get('value', ''))
            city_properties.append({
                'city_id': city_id,
                'property': 'inception',
                'value': inception
            })
    
    # 保存处理后的数据
    with open(os.path.join(output_dir, 'cities.json'), 'w', encoding='utf-8') as f:
        json.dump(cities, f, ensure_ascii=False, indent=2)
        
    with open(os.path.join(output_dir, 'city_properties.json'), 'w', encoding='utf-8') as f:
        json.dump(city_properties, f, ensure_ascii=False, indent=2)
    
    return len(cities), len(city_properties)

def process_people_data(input_file, output_dir):
    """处理人物数据"""
    # 读取JSON数据
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 提取绑定
    bindings = data.get('results', {}).get('bindings', [])
    
    # 准备实体和关系数据
    people = []
    people_properties = []
    occupations = set()
    awards = set()
    person_occupation = []
    person_award = []
    
    for item in bindings:
        person_id = extract_id_from_uri(item.get('person', {}).get('value', ''))
        if not person_id:
            continue
            
        person_name = item.get('personLabel', {}).get('value', '')
        
        # 添加人物实体
        person_exists = any(p['id'] == person_id for p in people)
        if not person_exists:
            people.append({
                'id': person_id,
                'name': person_name
            })
        
        # 处理出生日期
        if 'birth' in item:
            birth = clean_value(item['birth'].get('value', ''))
            people_properties.append({
                'person_id': person_id,
                'property': 'birth',
                'value': birth
            })
        
        # 处理死亡日期
        if 'death' in item:
            death = clean_value(item['death'].get('value', ''))
            people_properties.append({
                'person_id': person_id,
                'property': 'death',
                'value': death
            })
            
        # 处理职业
        if 'occupation' in item and 'occupationLabel' in item:
            occupation_id = extract_id_from_uri(item['occupation'].get('value', ''))
            occupation_name = item['occupationLabel'].get('value', '')
            
            if occupation_id and occupation_name:
                occupations.add((occupation_id, occupation_name))
                
                # 人物-职业关系
                person_occupation.append({
                    'person_id': person_id,
                    'occupation_id': occupation_id
                })
        
        # 处理奖项
        if 'award' in item and 'awardLabel' in item:
            award_id = extract_id_from_uri(item['award'].get('value', ''))
            award_name = item['awardLabel'].get('value', '')
            
            if award_id and award_name:
                awards.add((award_id, award_name))
                
                # 人物-奖项关系
                person_award.append({
                    'person_id': person_id,
                    'award_id': award_id
                })
    
    # 转换集合为列表
    occupations_list = [{'id': o[0], 'name': o[1]} for o in occupations]
    awards_list = [{'id': a[0], 'name': a[1]} for a in awards]
    
    # 保存处理后的数据
    with open(os.path.join(output_dir, 'people.json'), 'w', encoding='utf-8') as f:
        json.dump(people, f, ensure_ascii=False, indent=2)
        
    with open(os.path.join(output_dir, 'people_properties.json'), 'w', encoding='utf-8') as f:
        json.dump(people_properties, f, ensure_ascii=False, indent=2)
        
    with open(os.path.join(output_dir, 'occupations.json'), 'w', encoding='utf-8') as f:
        json.dump(occupations_list, f, ensure_ascii=False, indent=2)
        
    with open(os.path.join(output_dir, 'awards.json'), 'w', encoding='utf-8') as f:
        json.dump(awards_list, f, ensure_ascii=False, indent=2)
        
    with open(os.path.join(output_dir, 'person_occupation.json'), 'w', encoding='utf-8') as f:
        json.dump(person_occupation, f, ensure_ascii=False, indent=2)
        
    with open(os.path.join(output_dir, 'person_award.json'), 'w', encoding='utf-8') as f:
        json.dump(person_award, f, ensure_ascii=False, indent=2)
    
    return len(people), len(occupations_list), len(awards_list)

def process_universities_data(input_file, output_dir):
    """处理大学数据"""
    # 读取JSON数据
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 提取绑定
    bindings = data.get('results', {}).get('bindings', [])
    
    # 准备实体和关系数据
    universities = []
    university_properties = []
    locations = set()
    university_location = []
    
    for item in bindings:
        university_id = extract_id_from_uri(item.get('university', {}).get('value', ''))
        if not university_id:
            continue
            
        university_name = item.get('universityLabel', {}).get('value', '')
        
        # 添加大学实体
        universities.append({
            'id': university_id,
            'name': university_name
        })
        
        # 处理成立日期
        if 'inception' in item:
            inception = clean_value(item['inception'].get('value', ''))
            university_properties.append({
                'university_id': university_id,
                'property': 'inception',
                'value': inception
            })
        
        # 处理位置
        if 'location' in item and 'locationLabel' in item:
            location_id = extract_id_from_uri(item['location'].get('value', ''))
            location_name = item['locationLabel'].get('value', '')
            
            if location_id and location_name:
                locations.add((location_id, location_name))
                
                # 大学-位置关系
                university_location.append({
                    'university_id': university_id,
                    'location_id': location_id
                })
                
        # 处理学生数量
        if 'students' in item:
            students = item['students'].get('value', '')
            university_properties.append({
                'university_id': university_id,
                'property': 'students',
                'value': students
            })
            
        # 处理网站
        if 'website' in item:
            website = item['website'].get('value', '')
            university_properties.append({
                'university_id': university_id,
                'property': 'website',
                'value': website
            })
    
    # 转换集合为列表
    locations_list = [{'id': l[0], 'name': l[1]} for l in locations]
    
    # 保存处理后的数据
    with open(os.path.join(output_dir, 'universities.json'), 'w', encoding='utf-8') as f:
        json.dump(universities, f, ensure_ascii=False, indent=2)
        
    with open(os.path.join(output_dir, 'university_properties.json'), 'w', encoding='utf-8') as f:
        json.dump(university_properties, f, ensure_ascii=False, indent=2)
        
    with open(os.path.join(output_dir, 'locations.json'), 'w', encoding='utf-8') as f:
        json.dump(locations_list, f, ensure_ascii=False, indent=2)
        
    with open(os.path.join(output_dir, 'university_location.json'), 'w', encoding='utf-8') as f:
        json.dump(university_location, f, ensure_ascii=False, indent=2)
    
    return len(universities), len(locations_list)

def process_movies_data(input_file, output_dir):
    """处理电影数据"""
    # 读取JSON数据
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 提取绑定
    bindings = data.get('results', {}).get('bindings', [])
    
    # 准备实体和关系数据
    movies = []
    movie_properties = []
    directors = set()
    genres = set()
    casts = set()
    movie_director = []
    movie_genre = []
    movie_cast = []
    
    for item in bindings:
        movie_id = extract_id_from_uri(item.get('movie', {}).get('value', ''))
        if not movie_id:
            continue
            
        movie_name = item.get('movieLabel', {}).get('value', '')
        
        # 添加电影实体
        movie_exists = any(m['id'] == movie_id for m in movies)
        if not movie_exists:
            movies.append({
                'id': movie_id,
                'name': movie_name
            })
        
        # 处理导演
        if 'director' in item and 'directorLabel' in item:
            director_id = extract_id_from_uri(item['director'].get('value', ''))
            director_name = item['directorLabel'].get('value', '')
            
            if director_id and director_name:
                directors.add((director_id, director_name))
                
                # 电影-导演关系
                movie_director.append({
                    'movie_id': movie_id,
                    'director_id': director_id
                })
        
        # 处理发行日期
        if 'releaseDate' in item:
            release_date = clean_value(item['releaseDate'].get('value', ''))
            movie_properties.append({
                'movie_id': movie_id,
                'property': 'releaseDate',
                'value': release_date
            })
            
        # 处理类型
        if 'genre' in item and 'genreLabel' in item:
            genre_id = extract_id_from_uri(item['genre'].get('value', ''))
            genre_name = item['genreLabel'].get('value', '')
            
            if genre_id and genre_name:
                genres.add((genre_id, genre_name))
                
                # 电影-类型关系
                movie_genre.append({
                    'movie_id': movie_id,
                    'genre_id': genre_id
                })
                
        # 处理演员
        if 'cast' in item and 'castLabel' in item:
            cast_id = extract_id_from_uri(item['cast'].get('value', ''))
            cast_name = item['castLabel'].get('value', '')
            
            if cast_id and cast_name:
                casts.add((cast_id, cast_name))
                
                # 电影-演员关系
                movie_cast.append({
                    'movie_id': movie_id,
                    'cast_id': cast_id
                })
    
    # 转换集合为列表
    directors_list = [{'id': d[0], 'name': d[1]} for d in directors]
    genres_list = [{'id': g[0], 'name': g[1]} for g in genres]
    casts_list = [{'id': c[0], 'name': c[1]} for c in casts]
    
    # 保存处理后的数据
    with open(os.path.join(output_dir, 'movies.json'), 'w', encoding='utf-8') as f:
        json.dump(movies, f, ensure_ascii=False, indent=2)
        
    with open(os.path.join(output_dir, 'movie_properties.json'), 'w', encoding='utf-8') as f:
        json.dump(movie_properties, f, ensure_ascii=False, indent=2)
        
    with open(os.path.join(output_dir, 'directors.json'), 'w', encoding='utf-8') as f:
        json.dump(directors_list, f, ensure_ascii=False, indent=2)
        
    with open(os.path.join(output_dir, 'genres.json'), 'w', encoding='utf-8') as f:
        json.dump(genres_list, f, ensure_ascii=False, indent=2)
        
    with open(os.path.join(output_dir, 'casts.json'), 'w', encoding='utf-8') as f:
        json.dump(casts_list, f, ensure_ascii=False, indent=2)
        
    with open(os.path.join(output_dir, 'movie_director.json'), 'w', encoding='utf-8') as f:
        json.dump(movie_director, f, ensure_ascii=False, indent=2)
        
    with open(os.path.join(output_dir, 'movie_genre.json'), 'w', encoding='utf-8') as f:
        json.dump(movie_genre, f, ensure_ascii=False, indent=2)
        
    with open(os.path.join(output_dir, 'movie_cast.json'), 'w', encoding='utf-8') as f:
        json.dump(movie_cast, f, ensure_ascii=False, indent=2)
    
    return len(movies), len(directors_list), len(genres_list), len(casts_list)

def main():
    # 创建处理后数据的目录
    processed_dir = 'processed_data'
    if not os.path.exists(processed_dir):
        os.makedirs(processed_dir)
    
    print("开始处理Wikidata数据...")
    
    # 处理城市数据
    print("\n处理城市数据...")
    cities_count, city_props_count = process_cities_data('data/chinese_cities.json', processed_dir)
    print(f"处理了 {cities_count} 个城市和 {city_props_count} 条属性")
    
    # 处理人物数据
    print("\n处理人物数据...")
    people_count, occupations_count, awards_count = process_people_data('data/chinese_people.json', processed_dir)
    print(f"处理了 {people_count} 个人物, {occupations_count} 种职业和 {awards_count} 个奖项")
    
    # 处理大学数据
    print("\n处理大学数据...")
    universities_count, locations_count = process_universities_data('data/chinese_universities.json', processed_dir)
    print(f"处理了 {universities_count} 所大学和 {locations_count} 个位置")
    
    # 处理电影数据
    print("\n处理电影数据...")
    movies_count, directors_count, genres_count, casts_count = process_movies_data('data/chinese_movies.json', processed_dir)
    print(f"处理了 {movies_count} 部电影, {directors_count} 位导演, {genres_count} 个类型和 {casts_count} 位演员")
    
    print("\n所有数据处理完成!")

if __name__ == "__main__":
    main() 