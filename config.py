import os
from dotenv import load_dotenv

load_dotenv()  # Cargar variables de entorno desde el archivo .env

def config():
    database_url = os.getenv('DATABASE_URL')
    print(f"DATABASE_URL: {database_url}")  # Mensaje de depuración
    return {
        'database_url': database_url
    }



