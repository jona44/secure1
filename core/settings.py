import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-g72dfo-0u@r#g3p4%k)yg448ixcy)mmkcxv=fku0a9vp#bau%-'
# SECRET_KEY = os.environ.get('SECRET_KEY')
#DEBUG = os.environ.get('DEBUG') ==True
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['ec2-13-245-169-243.af-south-1.compute.amazonaws.com','13.245.169.243','localhost','127.0.0.1']


# Application definition
INSTALLED_APPS = [
    'customadmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'whitenoise.runserver_nostatic',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'student',
    'teacher',
    'grading',
    'district',
    'customsettings',
    
    'django.contrib.sites',  # Required by Allauth
    'allauth',
    'allauth.account',  # For account management
    'allauth.socialaccount',
    
    'crispy_forms',
    "crispy_bootstrap5",
    'storages'
]
AUTH_USER_MODEL = 'customadmin.CustomUser'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',  # Allauth backend
   
]


MIDDLEWARE = [
    'allauth.account.middleware.AccountMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'district.middlewares.SetSchoolInSessionMiddleware',
    
]
import os


ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates'), os.path.join(BASE_DIR,'templates', 'accounts')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'customsettings.context_processors.school_profile',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

SITE_ID = 1
# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases


DATABASES = {
    'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': BASE_DIR / 'db.sqlite3',
  }
}



# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = BASE_DIR/'staticfiles'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

LOGIN_URL = '/login'
LOGOUT_URL = '/logout'

CRISPY_TEMPLATE_PACK = 'uni_form'
CRISPY_TEMPLATE_PACK = 'bootstrap5'

TEMPLATE_DIRS = [(BASE_DIR, 'templates')]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT', 587)
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

ACCOUNT_AUTHENTICATION_METHOD = 'email'  # Authenticate by email
ACCOUNT_EMAIL_REQUIRED = True  # Email is mandatory
ACCOUNT_USERNAME_REQUIRED = False  # Don't require a separate username
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'  # Require email confirmation 
ACCOUNT_SESSION_REMEMBER = False  # Remember the user for future sessions
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True # Ask for password twice for security
ACCOUNT_USER_MODEL_USERNAME_FIELD = None


