import os
from dotenv import load_dotenv

# 加载.env文件中的环境变量
load_dotenv()

# MySQL配置
mysql_config = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'port': int(os.getenv('MYSQL_PORT', 3306)),
    'user': os.getenv('MYSQL_USER', 'your_username'),
    'password': os.getenv('MYSQL_PASSWORD', 'your_password'),
    'database': os.getenv('MYSQL_DATABASE', 'dataengineer')
}

# MongoDB配置
mongodb_config = {
    'host': os.getenv('MONGODB_HOST', 'localhost'),
    'port': int(os.getenv('MONGODB_PORT', 27017)),
    'database': os.getenv('MONGODB_DATABASE', 'wikidata'),
    'username': os.getenv('MONGODB_USERNAME', ''),
    'password': os.getenv('MONGODB_PASSWORD', '')
}

# 大语言模型API配置
llm_config = {
    'api_url': os.getenv('LLM_API_URL', 'your_api_url'),
    'api_key': os.getenv('LLM_API_KEY', 'your_api_key'),
    'model_name': os.getenv('LLM_MODEL_NAME', 'your_model_name')
} 