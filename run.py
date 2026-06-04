import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# LEER EL PUERTO DESDE EL ARCHIVO .ENV
port = os.getenv('API_PORT', '8000')

# INICIAR EL SERVIDOR DE DESARROLLO DE DJANGO EN EL PUERTO LEIDO
os.system(f'python manage.py runserver {port}')
