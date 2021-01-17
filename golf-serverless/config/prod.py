from .settings import *

DEBUG = False
ADMIN_URL = env.str("DJANGO_ADMIN_URL")

# Use S3 for static content
AWS_ACCESS_KEY_ID = env.str('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env.str('AWS_SECRET_ACCESS_KEY')
AWS_S3_BUCKET_NAME = "golf-api-static-21sd3asfa"
AWS_S3_BUCKET_NAME_STATIC = AWS_S3_BUCKET_NAME
AWS_S3_KEY_PREFIX = "media"
AWS_S3_KEY_PREFIX_STATIC = "static"
AWS_REGION = env.str('AWS_REGION')
AWS_S3_CUSTOM_DOMAIN = f'{AWS_S3_BUCKET_NAME}.s3.amazonaws.com'
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
STATICFILES_STORAGE = 'django_s3_storage.storage.StaticS3Storage'
PUBLIC_MEDIA_LOCATION = 'media'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/'
DEFAULT_FILE_STORAGE = 'django_s3_storage.storage.S3Storage'

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': env.str('AURORA_DB'), # dbname
#         'USER': env.str('AURORA_ADMIN'), # master username
#         'PASSWORD': env.str('AURORA_PASSWORD'), # master password
#         'HOST': env.str('AURORA_ENDPOINT'), # Endpoint
#         'PORT': '3306',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env.str('AURORA_DB'),
        'USER': env.str('AURORA_ADMIN'),
        'PASSWORD': env.str('AURORA_PASSWORD'),
        'HOST': env.str('AURORA_ENDPOINT'),
        'PORT': 5432,
    },
}