from forge_symposia.server import env
from eve_sqlalchemy.config import DomainConfig, ResourceConfig
from forge_symposia.server.models import indexDB

RESOURCE_METHODS = ['GET']

DOMAIN = DomainConfig({
}).render()


JWT_SECRET_KEY = 'python-starter-secret-key'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + env.INDEX_DB


SQLALCHEMY_BINDS = {
    'app_db': "sqlite:///" + env.APP_DB
}