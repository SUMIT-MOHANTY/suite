from .base import *
DEBUG = False
ALLOWED_HOSTS = ['*']  # ECS Fargate
import dj_database_url
DATABASES['default'] = dj_database_url.config(conn_max_age=600)
