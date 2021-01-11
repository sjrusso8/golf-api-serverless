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

# Use S3 for SQLite database
DATABASES = {
     'default': {
         'ENGINE': 'django_s3_sqlite',
         'NAME': env.str('SQLITE_DB'),
         'BUCKET':  env.str('AWS_S3_SQLITE'),
     }
}