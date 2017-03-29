"""
Use for testing on sqlite3...

$ ./manage.py test
"""
import os
PROJECT_NAME = 'flat-content'
PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/tmp/test.db',
        'USER': PROJECT_NAME,
        'PASSWORD': PROJECT_NAME,
        'HOST': '',
    }
}
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'flatcontent',
    'django_nose',
    'import_export',
    'django_markup',
)
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'testproject.urls'
SECRET_KEY = 's%(r1=t8io(=flnk%!si__eh-nhhazlou!p-+0^fnp)8o(mn&y'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_PATH, 'templates')],
        'OPTIONS': {
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
        },
    },
]
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = [
    '--detailed-errors',
    '--logging-clear-handlers',
    '-s',
]
