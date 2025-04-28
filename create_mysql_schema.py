import mysql.connector
import json
import os

# MySQL连接配置
config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'de_work',
    'password': 'data_engneer',
    'database': 'dataengineer'
}

def create_tables(cursor):
    """创建所有表"""
    
    # 创建实体表
    
    # 城市表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cities (
        id VARCHAR(20) PRIMARY KEY,
        name VARCHAR(255) NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    ''')
    
    # 城市属性表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS city_properties (
        id INT AUTO_INCREMENT PRIMARY KEY,
        city_id VARCHAR(20) NOT NULL,
        property VARCHAR(50) NOT NULL,
        value TEXT,
        FOREIGN KEY (city_id) REFERENCES cities(id) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    ''')
    
    # 人物表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS people (
        id VARCHAR(20) PRIMARY KEY,
        name VARCHAR(255) NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    ''')
    
    # 人物属性表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS people_properties (
        id INT AUTO_INCREMENT PRIMARY KEY,
        person_id VARCHAR(20) NOT NULL,
        property VARCHAR(50) NOT NULL,
        value TEXT,
        FOREIGN KEY (person_id) REFERENCES people(id) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    ''')
    
    # 职业表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS occupations (
        id VARCHAR(20) PRIMARY KEY,
        name VARCHAR(255) NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    ''')
    
    # 奖项表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS awards (
        id VARCHAR(20) PRIMARY KEY,
        name VARCHAR(255) NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    ''')
    
    # 人物-职业关系表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS person_occupation (
        id INT AUTO_INCREMENT PRIMARY KEY,
        person_id VARCHAR(20) NOT NULL,
        occupation_id VARCHAR(20) NOT NULL,
        FOREIGN KEY (person_id) REFERENCES people(id) ON DELETE CASCADE,
        FOREIGN KEY (occupation_id) REFERENCES occupations(id) ON DELETE CASCADE,
        UNIQUE KEY (person_id, occupation_id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    ''')
    
    # 人物-奖项关系表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS person_award (
        id INT AUTO_INCREMENT PRIMARY KEY,
        person_id VARCHAR(20) NOT NULL,
        award_id VARCHAR(20) NOT NULL,
        FOREIGN KEY (person_id) REFERENCES people(id) ON DELETE CASCADE,
        FOREIGN KEY (award_id) REFERENCES awards(id) ON DELETE CASCADE,
        UNIQUE KEY (person_id, award_id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    ''')
    
    # 大学表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS universities (
        id VARCHAR(20) PRIMARY KEY,
        name VARCHAR(255) NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    ''')
    
    # 大学属性表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS university_properties (
        id INT AUTO_INCREMENT PRIMARY KEY,
        university_id VARCHAR(20) NOT NULL,
        property VARCHAR(50) NOT NULL,
        value TEXT,
        FOREIGN KEY (university_id) REFERENCES universities(id) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    ''')
    
    # 位置表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS locations (
        id VARCHAR(20) PRIMARY KEY,
        name VARCHAR(255) NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    ''')
    
    # 大学-位置关系表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS university_location (
        id INT AUTO_INCREMENT PRIMARY KEY,
        university_id VARCHAR(20) NOT NULL,
        location_id VARCHAR(20) NOT NULL,
        FOREIGN KEY (university_id) REFERENCES universities(id) ON DELETE CASCADE,
        FOREIGN KEY (location_id) REFERENCES locations(id) ON DELETE CASCADE,
        UNIQUE KEY (university_id, location_id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    ''')
    
    # 电影表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS movies (
        id VARCHAR(20) PRIMARY KEY,
        name VARCHAR(255) NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    ''')
    
    # 电影属性表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS movie_properties (
        id INT AUTO_INCREMENT PRIMARY KEY,
        movie_id VARCHAR(20) NOT NULL,
        property VARCHAR(50) NOT NULL,
        value TEXT,
        FOREIGN KEY (movie_id) REFERENCES movies(id) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    ''')
    
    # 导演表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS directors (
        id VARCHAR(20) PRIMARY KEY,
        name VARCHAR(255) NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    ''')
    
    # 电影类型表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS genres (
        id VARCHAR(20) PRIMARY KEY,
        name VARCHAR(255) NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    ''')
    
    # 演员表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS casts (
        id VARCHAR(20) PRIMARY KEY,
        name VARCHAR(255) NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    ''')
    
    # 电影-导演关系表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS movie_director (
        id INT AUTO_INCREMENT PRIMARY KEY,
        movie_id VARCHAR(20) NOT NULL,
        director_id VARCHAR(20) NOT NULL,
        FOREIGN KEY (movie_id) REFERENCES movies(id) ON DELETE CASCADE,
        FOREIGN KEY (director_id) REFERENCES directors(id) ON DELETE CASCADE,
        UNIQUE KEY (movie_id, director_id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    ''')
    
    # 电影-类型关系表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS movie_genre (
        id INT AUTO_INCREMENT PRIMARY KEY,
        movie_id VARCHAR(20) NOT NULL,
        genre_id VARCHAR(20) NOT NULL,
        FOREIGN KEY (movie_id) REFERENCES movies(id) ON DELETE CASCADE,
        FOREIGN KEY (genre_id) REFERENCES genres(id) ON DELETE CASCADE,
        UNIQUE KEY (movie_id, genre_id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    ''')
    
    # 电影-演员关系表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS movie_cast (
        id INT AUTO_INCREMENT PRIMARY KEY,
        movie_id VARCHAR(20) NOT NULL,
        cast_id VARCHAR(20) NOT NULL,
        FOREIGN KEY (movie_id) REFERENCES movies(id) ON DELETE CASCADE,
        FOREIGN KEY (cast_id) REFERENCES casts(id) ON DELETE CASCADE,
        UNIQUE KEY (movie_id, cast_id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    ''')
    
    print("所有表创建完成")

def main():
    try:
        # 连接到MySQL
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        
        print("成功连接到MySQL")
        
        # 创建表结构
        create_tables(cursor)
        
        # 提交事务并关闭连接
        conn.commit()
        cursor.close()
        conn.close()
        print("MySQL连接已关闭")
        
    except mysql.connector.Error as err:
        print(f"MySQL错误: {err}")

if __name__ == "__main__":
    main() 