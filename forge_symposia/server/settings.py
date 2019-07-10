from forge_symposia.server import env
from eve_sqlalchemy.config import DomainConfig, ResourceConfig
from forge_symposia.server.models import DBAssetState

RESOURCE_METHODS = ['GET']

DOMAIN = DomainConfig({
    'events': ResourceConfig(DBAssetState)
}).render()


JWT_SECRET_KEY = 'python-starter-secret-key'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + env.INDEX_DB
