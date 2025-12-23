import os
from pathlib import Path
from decouple import config
import dj_database_url

# BASE_DIR يشير إلى المجلد الرئيسي للمشروع
BASE_DIR = Path(__file__).resolve().parent.parent

# --- إعدادات الأمان الأساسية ---
SECRET_KEY = config('SECRET_KEY', default='django-insecure-default-key')
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1,localhost').split(',')

# --- التطبيقات المسجلة ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'contracts.apps.ContractsConfig',
]

# --- الميدل وير ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
     'whitenoise.middleware.WhiteNoiseMiddleware'
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

# --- التعديل الجوهري هنا لحل مشكلة المجلدات ---
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # تأكد من هذا السطر تحديداً
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
WSGI_APPLICATION = 'core.wsgi.application'

# --- قاعدة البيانات ---
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600
    )
}

# --- الإعدادات الإقليمية ---
LANGUAGE_CODE = 'ar'
TIME_ZONE = 'Africa/Cairo'
USE_I18N = True
USE_TZ = True

# --- إعدادات الحسابات ---
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'

# --- الملفات الثابتة والمرفوعات ---
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# ملاحظة: تم تعطيل ManifestStorage مؤقتاً لتجنب مشاكل الـ CSS أثناء التطوير المحلي
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# --- إعدادات Stripe & OpenAI (تأكد من وضع القيم الحقيقية في ملف .env) ---
STRIPE_PUBLIC_KEY = config('STRIPE_PUBLIC_KEY', default='pk_test_...')
STRIPE_SECRET_KEY = config('STRIPE_SECRET_KEY', default='sk_test_...')
OPENAI_API_KEY = config('OPENAI_API_KEY', default='')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- إعدادات البريد الإلكتروني ---
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# لاحظ إضافة الـ default هنا لمنع الخطأ
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='sayedhemdan69@gmail.com')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='S123456&s')

DEFAULT_FROM_EMAIL = 'المنصة القانونية التقنية <sayedhemdan69@gmail.com>'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # المجلد الذي سيجمع فيه السيرفر الصور
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'