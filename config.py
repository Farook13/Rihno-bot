import os
from os import environ  # Assuming environ is used as in the error

# Configuration class or direct variables
class Config:  # If using a class, ensure proper indentation
    BOT_TOKEN = environ.get('7857321740:AAEtcoE9BbLGCaF5TlkeGvhLZpXU36vco8E')
    API_ID = int(environ.get('API_ID', '12618934'))
    API_HASH = environ.get('49aacd0bc2f8924add29fb02e20c8a16')
    DATABASE_URI = environ.get('mongodb+srv://saidalimuhamed88:iladias2025@cluster0.qt4dv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
    DATABASE_NAME = environ.get('DATABASE_NAME', 'Cluster0')
    AUTH_CHANNEL = environ.get('-1002256041072')
    LOG_CHANNEL = environ.get('-1002467149516')
    OWNER_ID = int(environ.get('OWNER_ID', '5032034594'))
    AUTO_DELETE_TIME = int(environ.get('AUTO_DELETE_TIME', '60'))

# If not using a class, ensure no stray block starters
BOT_TOKEN = environ.get('7857321740:AAEtcoE9BbLGCaF5TlkeGvhLZpXU36vco8E')
API_ID = int(environ.get('API_ID', '12618934
API_HASH = environ.get('49aacd0bc2f8924add29fb02e20c8a16')
DATABASE_URI = environ.get('mongodb+srv://saidalimuhamed88:iladias2025@cluster0.qt4dv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
DATABASE_NAME = environ.get('DATABASE_NAME', 'Cluster0')
AUTH_CHANNEL = environ.get('-1002256041072')
LOG_CHANNEL = environ.get('-1002467149516')
OWNER_ID = int(environ.get('OWNER_ID', '5032034594'))
AUTO_DELETE_TIME = int(environ.get('AUTO_DELETE_TIME', '60'))
