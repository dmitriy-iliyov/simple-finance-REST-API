import os

PROPAGATE_EXCEPTIONS = True

FLASK_DEBUG = True

SQLALCHEMY_DATABASE_URI = f'postgresql://admin:root@localhost:5432/database'

# SQLALCHEMY_DATABASE_URI = f'postgresql://{os.environ["POSTGRES_USER"]}:{os.environ["POSTGRES_PASSWORD"]}@localhost:5432/{os.environ["POSTGRES_DB"]}'
SQLALCHEMY_TRACK_MODIFICATIONS = False

API_TITLE = "Finance REST API"

API_VERSION = "vi"

OPENAPI_VERSION = "3.9.3"

OPENAPI_URL_PREFIX = "/"

OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"

OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"