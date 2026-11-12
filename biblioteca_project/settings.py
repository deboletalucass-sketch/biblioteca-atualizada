"""
Configurações do projeto Biblioteca.
Banco de dados: PostgreSQL hospedado no Neon (https://neon.tech).
"""

import os
from pathlib import Path

from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY", default="django-insecure-troque-esta-chave")
DEBUG = config("DEBUG", default=True, cast=bool)
ALLOWED_HOSTS = [
    h.strip() for h in config("ALLOWED_HOSTS", default="127.0.0.1,localhost").split(",") if h.strip()
]
CSRF_TRUSTED_ORIGINS = [
    o.strip() for o in config("CSRF_TRUSTED_ORIGINS", default="").split(",") if o.strip()
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_filters",
    "biblioteca",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # serve estáticos no App Engine
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "biblioteca_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "biblioteca" / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "biblioteca_project.wsgi.application"

# ---------------------------------------------------------------------------
# Banco de dados — Neon (PostgreSQL serverless)
# Defina a string de conexão na variável de ambiente DATABASE_URL, no
# formato: postgresql://usuario:senha@host.neon.tech/dbname?sslmode=require
# ---------------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("PGDATABASE", default="biblioteca"),
        "USER": config("PGUSER", default=""),
        "PASSWORD": config("PGPASSWORD", default=""),
        "HOST": config("PGHOST", default=""),
        "PORT": config("PGPORT", default="5432"),
        "OPTIONS": {"sslmode": "require"},
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"  # destino do collectstatic (deploy)

# Pasta static/ dentro do app "biblioteca" (biblioteca/static/) já é
# encontrada automaticamente pelo APP_DIRS do STATICFILES_FINDERS,
# então não é necessário declarar STATICFILES_DIRS aqui.

# ---------------------------------------------------------------------------
# Arquivos de mídia (uploads dos usuários, ex.: capas dos livros)
# ---------------------------------------------------------------------------
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

# ---------------------------------------------------------------------------
# Armazenamento. No App Engine o disco é somente leitura/efêmero, então os
# uploads (capas) precisam ir para um bucket do Google Cloud Storage.
# Defina GS_BUCKET_NAME para ativar; sem ele, usa o disco local (dev).
# ---------------------------------------------------------------------------
GS_BUCKET_NAME = config("GS_BUCKET_NAME", default="")

STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedStaticFilesStorage"},
}
if GS_BUCKET_NAME:
    STORAGES["default"] = {"BACKEND": "storages.backends.gcloud.GoogleCloudStorage"}
    GS_DEFAULT_ACL = None  # bucket com acesso uniforme; leitura pública via IAM

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---------------------------------------------------------------------------
# E-mail (recuperação de senha e de usuário)
# Em desenvolvimento os e-mails aparecem no terminal (backend "console").
# Em produção defina EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
# e as credenciais SMTP no ambiente.
# ---------------------------------------------------------------------------
EMAIL_BACKEND = config(
    "EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend"
)
EMAIL_HOST = config("EMAIL_HOST", default="smtp.gmail.com")
EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
DEFAULT_FROM_EMAIL = config(
    "DEFAULT_FROM_EMAIL", default=EMAIL_HOST_USER or "biblioteca@localhost"
)
PASSWORD_RESET_TIMEOUT = 60 * 60 * 24  # link de redefinição válido por 24h

# ---------------------------------------------------------------------------
# Segurança em produção (App Engine termina o HTTPS no proxy)
# ---------------------------------------------------------------------------
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# ---------------------------------------------------------------------------
# Autenticação: para onde redirecionar quem não está logado (LoginRequiredMixin)
# e para onde ir após o login/logout.
# ---------------------------------------------------------------------------
LOGIN_URL = "biblioteca:login"
LOGIN_REDIRECT_URL = "biblioteca:livro_list"
LOGOUT_REDIRECT_URL = "biblioteca:login"
