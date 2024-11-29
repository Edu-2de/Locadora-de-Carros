from pathlib import Path
import os

# Caminho base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Diretório de arquivos de mídia (imagens enviadas pelo usuário)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Configurações de segurança
SECRET_KEY = 'django-insecure-u7c71d6@ggxwechm4nv@pk^h7tug)m1@z$fd#9(4uoip8(4pu)'
DEBUG = True
ALLOWED_HOSTS = []

# Aplicativos instalados
INSTALLED_APPS = [
    # Removemos 'django.contrib.admin' e 'django.contrib.auth'
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'locadora.apps.LocadoraConfig',  # App principal
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'locadora.middleware.CheckUserLoginMiddleware',  # Verificação personalizada
]
# Configuração do banco de dados
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'locadora',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

# Configurações de localização
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Configurações de arquivos estáticos
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "locadora/static",
]

# Configuração do diretório de templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'locadora/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Configurações de sessão
SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # ou 'cache' para desempenho otimizado
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_NAME = 'sessionid'
SESSION_COOKIE_AGE = 86400  # Tempo de duração da sessão em segundos (aqui, 1 dia)
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # A sessão não fecha ao fechar o navegador


# Configuração da chave primária padrão
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuração da raiz de URLs
ROOT_URLCONF = 'locadora_project.urls'
